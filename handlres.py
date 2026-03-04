# handlers.py
import os
from uuid import uuid4
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import DOWNLOAD_DIR
from utils import get_tiktok_data, download_file, convert_to_mp3, build_caption

# user_downloads akan diisi dari main.py
user_downloads = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 *TikTok Downloader Bot*\n\n"
        "✨ *Fitur:*\n"
        "✅ 2 API Cadangan (otomatis pindah)\n"
        "✅ Fake User Agent (anti block)\n"
        "✅ Statistik Lengkap (Views, Likes, Comments, Shares, Saves)\n"
        "✅ Auto Delete Pesan (30 detik)\n"
        "✅ Statistik Pribadi (/mystats)\n"
        "✅ Download Video MP4 / Audio MP3\n\n"
        "📤 *Cara pakai:*\n"
        "1. Kirim link TikTok\n"
        "2. Pilih format (MP4 | MP3)\n"
        "3. Tunggu proses selesai\n\n"
        "💡 *Contoh link:*\n"
        "• https://vm.tiktok.com/xxxxx\n"
        "• https://www.tiktok.com/@user/video/1234567890",
        parse_mode='Markdown'
    )

async def mystats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    count = user_downloads.get(user_id, 0)
    await update.message.reply_text(
        f"📊 *Statistik Pribadi*\n\n"
        f"Total download: {count}",
        parse_mode='Markdown'
    )

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not any(x in url for x in ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']):
        await update.message.reply_text("❌ Kirim link TikTok yang valid!")
        return

    context.user_data['url'] = url

    keyboard = [[
        InlineKeyboardButton("🎬 Video MP4", callback_data='mp4'),
        InlineKeyboardButton("🎧 Audio MP3", callback_data='mp3')
    ]]

    msg = await update.message.reply_text(
        "📥 *Pilih format:*",
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

    # Update statistik user
    user_id = update.effective_user.id
    global user_downloads
    user_downloads[user_id] = user_downloads.get(user_id, 0) + 1

    url = context.user_data.get('url')
    if not url:
        await query.edit_message_text("❌ URL tidak ditemukan, kirim ulang.")
        return

    await query.edit_message_text("⏳ *Mengambil data TikTok...*", parse_mode='Markdown')

    data = get_tiktok_data(url)

    if not data:
        await query.edit_message_text(
            "❌ *Gagal mengambil data*\n"
            "• Coba link lain\n"
            "• Atau nanti lagi",
            parse_mode='Markdown'
        )
        return

    try:
        if query.data == 'mp4':
            video_url = data.get('video')
            if not video_url:
                await query.edit_message_text("❌ Video tidak ditemukan.")
                return

            filename = f"{DOWNLOAD_DIR}/vid_{uuid4().hex[:8]}.mp4"
            await query.edit_message_text("⏳ *Download video...*", parse_mode='Markdown')

            if download_file(video_url, filename):
                caption = build_caption(data, format_type='video')
                with open(filename, 'rb') as f:
                    await query.message.reply_video(
                        video=f,
                        caption=caption,
                        parse_mode='Markdown',
                        supports_streaming=True
                    )
                os.remove(filename)
                await query.delete_message()
                
                context.job_queue.run_once(
                    lambda ctx: ctx.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id),
                    10
                )
            else:
                await query.edit_message_text("❌ Gagal download video.")

        elif query.data == 'mp3':
            audio_url = data.get('audio') or data.get('video')
            if not audio_url:
                await query.edit_message_text("❌ Audio tidak ditemukan.")
                return

            video_file = f"{DOWNLOAD_DIR}/temp_{uuid4().hex[:8]}.mp4"
            audio_file = f"{DOWNLOAD_DIR}/audio_{uuid4().hex[:8]}.mp3"

            await query.edit_message_text("⏳ *Download audio...*", parse_mode='Markdown')

            if download_file(audio_url, video_file):
                await query.edit_message_text("⏳ *Konversi ke MP3...*", parse_mode='Markdown')

                if convert_to_mp3(video_file, audio_file):
                    caption = build_caption(data, format_type='audio')
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
                    await query.edit_message_text("❌ Gagal konversi audio.")
                    if os.path.exists(video_file):
                        os.remove(video_file)
            else:
                await query.edit_message_text("❌ Gagal download audio.")

    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)[:100]}")