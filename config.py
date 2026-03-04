# config.py
import os

# ===== KONFIGURASI =====
BOT_TOKEN = "8300850049:AAFyVQOoiO58G0piaU84JPfIUEHzIPb8vPc"  # Ganti dengan token bot lo
DOWNLOAD_DIR = "downloads"

# Buat folder download jika belum ada
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

# Database sederhana (akan diinisialisasi di main.py)
# user_downloads = {}  # pindah ke main biar gak di-import terus