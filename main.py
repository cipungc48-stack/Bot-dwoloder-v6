# main.py
import time
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN
from handlers import start, mystats, handle_url, button_handler, user_downloads

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mystats", mystats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("="*60)
    print("🎵 TIKTOK DOWNLOADER BOT - FULL FEATURES")
    print("="*60)
    print("✅ 2 API Cadangan")
    print("✅ Fake User Agent")
    print("✅ Statistik Lengkap")
    print("✅ Auto Delete Pesan")
    print("✅ Statistik Pengguna")
    print("="*60)
    print("🤖 Bot started... Press Ctrl+C to stop")
    print("="*60)

    app.run_polling(timeout=30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        time.sleep(5)
        main()