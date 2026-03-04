# config.py
import os

# ===== KONFIGURASI =====
BOT_TOKEN = "8300850049:AAFyVQOoiO58G0piaU84JPfIUEHzIPb8vPc"  # Ganti dengan token bot lo
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ===== 2 API TIKTOK CADANGAN =====
APIS = [
    {
        'name': 'TikWM',
        'url': 'https://tikwm.com/api/',
        'type': 'post',
        'data_key': 'url'
    },
    {
        'name': 'TikMate',
        'url': 'https://api.tikmate.cc/api/',
        'type': 'post',
        'data_key': 'url'
    }
]

# ===== FAKE USER AGENTS =====
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
]

# ===== MULTI LANGUAGE =====
LANGUAGES = {
    'id': {
        'welcome': (
            "🎵 *TikTok Downloader Bot*\n\n"
            "✨ *Fitur:*\n"
            "✅ 2 API Cadangan\n"
            "✅ Fake User Agent\n"
            "✅ Statistik Lengkap\n"
            "✅ Auto Delete Pesan\n"
            "✅ Statistik Pribadi (/mystats)\n"
            "✅ Download Video MP4 / Audio MP3\n\n"
            "📤 *Cara pakai:*\n"
            "1. Kirim link TikTok\n"
            "2. Pilih format (MP4 | MP3)\n"
            "3. Tunggu proses selesai\n\n"
            "💡 *Contoh link:*\n"
            "• https://vm.tiktok.com/xxxxx\n"
            "• https://www.tiktok.com/@user/video/1234567890"
        ),
        'choose_lang': "🌐 *Pilih bahasa:*",
        'lang_id': "🇮🇩 Indonesia",
        'lang_en': "🇬🇧 English",
        'choose_format': "📥 *Pilih format:*",
        'mp4': "🎬 Video MP4",
        'mp3': "🎧 Audio MP3",
        'invalid_url': "❌ Kirim link TikTok yang valid!",
        'processing': "⏳ *Mengambil data TikTok...*",
        'failed': "❌ *Gagal mengambil data*\n• Coba link lain\n• Atau nanti lagi",
        'no_video': "❌ Video tidak ditemukan.",
        'no_audio': "❌ Audio tidak ditemukan.",
        'downloading_video': "⏳ *Download video...*",
        'downloading_audio': "⏳ *Download audio...*",
        'converting': "⏳ *Konversi ke MP3...*",
        'download_failed': "❌ Gagal download video.",
        'audio_failed': "❌ Gagal download audio.",
        'convert_failed': "❌ Gagal konversi audio.",
        'stats': "📊 *Statistik Pribadi*\n\nTotal download: {}",
        'mystats_button': "📊 Statistik Saya",
        'author': 'Author',
        'region': 'Region',
        'upload': 'Upload',
        'duration': 'Durasi',
        'stats_title': 'STATISTIK VIDEO',
        'views': 'Views',
        'likes': 'Likes',
        'comments': 'Comments',
        'shares': 'Shares',
        'saves': 'Saves',
        'hashtag': 'Hashtag',
        'none': 'Tidak ada',
        'format': 'Format'
    },
    'en': {
        'welcome': (
            "🎵 *TikTok Downloader Bot*\n\n"
            "✨ *Features:*\n"
            "✅ 2 Backup APIs\n"
            "✅ Fake User Agent\n"
            "✅ Complete Stats\n"
            "✅ Auto Delete Messages\n"
            "✅ Personal Stats (/mystats)\n"
            "✅ Download Video MP4 / Audio MP3\n\n"
            "📤 *How to use:*\n"
            "1. Send TikTok link\n"
            "2. Choose format (MP4 | MP3)\n"
            "3. Wait for process\n\n"
            "💡 *Example link:*\n"
            "• https://vm.tiktok.com/xxxxx\n"
            "• https://www.tiktok.com/@user/video/1234567890"
        ),
        'choose_lang': "🌐 *Choose language:*",
        'lang_id': "🇮🇩 Indonesian",
        'lang_en': "🇬🇧 English",
        'choose_format': "📥 *Choose format:*",
        'mp4': "🎬 Video MP4",
        'mp3': "🎧 Audio MP3",
        'invalid_url': "❌ Send a valid TikTok link!",
        'processing': "⏳ *Fetching TikTok data...*",
        'failed': "❌ *Failed to fetch data*\n• Try another link\n• Or try again later",
        'no_video': "❌ Video not found.",
        'no_audio': "❌ Audio not found.",
        'downloading_video': "⏳ *Downloading video...*",
        'downloading_audio': "⏳ *Downloading audio...*",
        'converting': "⏳ *Converting to MP3...*",
        'download_failed': "❌ Failed to download video.",
        'audio_failed': "❌ Failed to download audio.",
        'convert_failed': "❌ Failed to convert audio.",
        'stats': "📊 *Personal Stats*\n\nTotal downloads: {}",
        'mystats_button': "📊 My Stats",
        'author': 'Author',
        'region': 'Region',
        'upload': 'Upload',
        'duration': 'Duration',
        'stats_title': 'VIDEO STATISTICS',
        'views': 'Views',
        'likes': 'Likes',
        'comments': 'Comments',
        'shares': 'Shares',
        'saves': 'Saves',
        'hashtag': 'Hashtag',
        'none': 'None',
        'format': 'Format'
    }
}

def get_text(key, lang='id'):
    """Ambil teks berdasarkan kunci dan bahasa"""
    return LANGUAGES.get(lang, LANGUAGES['id']).get(key, key)