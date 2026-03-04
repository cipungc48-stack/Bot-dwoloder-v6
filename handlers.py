# handlers.py
import os
from uuid import uuid4
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import DOWNLOAD_DIR, get_text
from utils import get_tiktok_data, download_file, convert_to_mp3, build_caption, get_file_duration

# Database sederhana (user_id: download_count)
user_downloads = {}

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan pilihan bahasa saat pertama start"""
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]  # 'lang_id' atau 'lang_en'
    context.user_data['lang'] = lang
    await query.edit_message_text(
        get_text('welcome', lang),
        parse_mode='Markdown'
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /start - cek apakah sudah pilih bahasa"""
    if 'lang' not in context.user_data:
        keyboard = [
            [InlineKeyboardButton(get_text('lang_id', 'id'), callback_data='lang_id')],
            [InlineKeyboardButton(get_text('lang_en', 'en'), callback_data='lang_en')]
        ]
        await update.message.reply_text(
            get_text('choose_lang', 'id'),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        lang = context.user_data['lang']
        await update.message.reply_text(
            get_text('welcome', lang),
            parse_mode='Markdown'
        )

async def mystats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = user_downloads.get(user_id, 0)
    lang = context.user_data.get('lang', 'id')
    await update.message.reply_text(
        get_text('stats', lang).format(count),
        parse_mode='Markdown'
    )

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    lang = context.user_data.get('lang', 'id')

    if not any(x in url for x in ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']):
        await update.message.reply_text(get_text('invalid_url', lang))
        return

    context.user_data['url'] = url

    keyboard = [[
        InlineKeyboardButton(get_text('mp4', lang), callback_data='mp4'),
        InlineKeyboardButton(get_text('mp3', lang), callback_data='mp3')
    ]]

    msg = await update.message.reply_text(
        get_text('choose_format', lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    # Auto delete pesan pilihan setelah 30 detik
    context.job_queue.run_once(
        lambda ctx: ctx.bot.delete_message(chat_id=update.effective_chat.id, message_id=msg.message_id),
        30
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    global user_downloads
    user_downloads[user_id] = user_downloads.get(user_id, 0) + 1

    lang = context.user_data.get('lang', 'id')
    url = context.user_data.get('url')
    if not url:
        await query.edit_message_text(get_text('invalid_url', lang))
        return

    await query.edit_message_text(get_text('processing', lang), parse_mode='Markdown')
    data = get_tiktok_data(url)

    if not data:
        await query.edit_message_text(get_text('failed', lang), parse_mode='Markdown')
        return

    try:
        if query.data == 'mp4':
            video_url = data.get('video')
            if not video_url:
                await query.edit_message_text(get_text('no_video', lang))
                return

            filename = f"{DOWNLOAD_DIR}/vid_{uuid4().hex[:8]}.mp4"
            await query.edit_message_text(get_text('downloading_video', lang), parse_mode='Markdown')

            if download_file(video_url, filename):
                actual_duration = get_file_duration(filename)
                caption = build_caption(data, format_type='video', actual_duration=actual_duration, lang=lang)
                with open(filename, 'rb') as f:
                    await query.message.reply_video(
                        video=f,
                        caption=caption,
                        parse_mode='Markdown',
                        supports_streaming=True
                    )
                os.remove(filename)
                await query.delete_message()
                # Auto delete pesan status setelah 10 detik
                context.job_queue.run_once(
                    lambda ctx: ctx.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id),
                    10
                )
            else:
                await query.edit_message_text(get_text('download_failed', lang))

        elif query.data == 'mp3':
            audio_url = data.get('audio') or data.get('video')
            if not audio_url:
                await query.edit_message_text(get_text('no_audio', lang))
                return

            video_file = f"{DOWNLOAD_DIR}/temp_{uuid4().hex[:8]}.mp4"
            audio_file = f"{DOWNLOAD_DIR}/audio_{uuid4().hex[:8]}.mp3"

            await query.edit_message_text(get_text('downloading_audio', lang), parse_mode='Markdown')

            if download_file(audio_url, video_file):
                await query.edit_message_text(get_text('converting', lang), parse_mode='Markdown')
                if convert_to_mp3(video_file, audio_file):
                    actual_duration = get_file_duration(audio_file)
                    caption = build_caption(data, format_type='audio', actual_duration=actual_duration, lang=lang)
                    with open(audio_file, 'rb') as f:
                        await query.message.reply_audio(
                            audio=f,
                            title=data.get('title', '')[:50],
                            performer=data.get('author', ''),
                            caption=caption,
                            parse_mode='Markdown'
                        )
                    os.remove(video_file)
                    os.remove(audio_file)
                    await query.delete_message()
                    context.job_queue.run_once(
                        lambda ctx: ctx.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id),
                        10
                    )
                else:
                    await query.edit_message_text(get_text('convert_failed', lang))
                    if os.path.exists(video_file):
                        os.remove(video_file)
            else:
                await query.edit_message_text(get_text('audio_failed', lang))

    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)[:100]}")