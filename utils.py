# utils.py
import os
import time
import random
import requests
from config import APIS, USER_AGENTS, DOWNLOAD_DIR
from datetime import datetime

def get_headers():
    """Return random user agent headers"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

def check_internet():
    """Cek koneksi internet"""
    try:
        requests.get('https://8.8.8.8', timeout=3)
        return True
    except:
        return False

def resolve_short_url(url):
    """Resolve short URL (vm.tiktok.com)"""
    if 'vm.tiktok.com' in url or 'vt.tiktok.com' in url:
        try:
            r = requests.get(url, timeout=15, allow_redirects=True)
            if r.status_code == 200:
                return r.url
        except:
            pass
    return url

def format_number(num):
    """Format angka ke K/M/B"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def get_tiktok_data(url):
    """Coba semua API sampai berhasil, ambil statistik lengkap"""
    if not check_internet():
        return None

    url = resolve_short_url(url)

    for api in APIS:
        try:
            print(f"🔄 Mencoba {api['name']}...")
            time.sleep(1)

            if api['type'] == 'post':
                data = {api['data_key']: url}
                response = requests.post(
                    api['url'],
                    data=data,
                    headers=get_headers(),
                    timeout=30
                )
            else:
                response = requests.get(
                    api['url'],
                    params={api['data_key']: url},
                    headers=get_headers(),
                    timeout=30
                )

            if response.status_code == 200:
                result = response.json()

                # Parse TikWM format
                if result.get('code') == 0:
                    d = result['data']
                    return {
                        'title': d.get('title', 'No Title'),
                        'author': d.get('author', {}).get('nickname', 'Unknown'),
                        'video': d.get('hdplay') or d.get('play', ''),
                        'audio': d.get('music', ''),
                        'cover': d.get('cover', ''),
                        'views': format_number(d.get('play_count', 0)),
                        'likes': format_number(d.get('digg_count', 0)),
                        'comments': format_number(d.get('comment_count', 0)),
                        'shares': format_number(d.get('share_count', 0)),
                        'saves': format_number(d.get('collect_count', 0)),
                        'duration': d.get('duration', 0),
                        'create_time': d.get('create_time', ''),
                        'region': d.get('region', '')
                    }

                # Parse TikMate format
                elif result.get('status'):
                    return {
                        'title': result.get('title', 'TikTok Video'),
                        'author': result.get('author', 'Unknown'),
                        'video': result.get('url', ''),
                        'audio': result.get('url', ''),
                        'cover': result.get('thumbnail', ''),
                        'views': format_number(result.get('play_count', 0)),
                        'likes': format_number(result.get('digg_count', 0)),
                        'comments': format_number(result.get('comment_count', 0)),
                        'shares': format_number(result.get('share_count', 0)),
                        'saves': '0',
                        'duration': result.get('duration', 0),
                        'create_time': '',
                        'region': ''
                    }

        except Exception as e:
            print(f"⚠️ {api['name']} error: {e}")
        continue

    return None

def download_file(url, filename):
    """Download file dengan retry 3x"""
    for attempt in range(3):
        try:
            r = requests.get(url, headers=get_headers(), timeout=60)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(r.content)
                return True
        except:
            time.sleep(2)
    return False

def convert_to_mp3(video_file, audio_file):
    """Convert video to MP3 using ffmpeg"""
    os.system(f'ffmpeg -i "{video_file}" -q:a 0 -map a "{audio_file}" -y > /dev/null 2>&1')
    return os.path.exists(audio_file)

def build_caption(data, format_type='video'):
    """Buat caption lengkap dengan statistik dan format"""
    title = data.get('title', 'No Title')[:100]
    author = data.get('author', 'Unknown')
    region = data.get('region', '🌍 Unknown')
    duration = data.get('duration', 0)
    create_time = data.get('create_time', '')
    views = data.get('views', '0')
    likes = data.get('likes', '0')
    comments = data.get('comments', '0')
    shares = data.get('shares', '0')
    saves = data.get('saves', '0')
    
    minutes = duration // 60
    seconds = duration % 60
    duration_str = f"{minutes}:{seconds:02d}"
    
    if create_time:
        try:
            upload_date = datetime.fromtimestamp(int(create_time)).strftime('%d %b %Y')
        except:
            upload_date = 'Unknown'
    else:
        upload_date = 'Unknown'
    
    hashtags = ' '.join([word for word in title.split() if word.startswith('#')][:3])
    
    caption = f"""
🎵 *{title}*

👤 **Author:** {author}
📍 **Region:** {region}
📅 **Upload:** {upload_date}
⏱️ **Durasi:** {duration_str}

📊 **STATISTIK VIDEO**
┌ 👀 Views: `{views}`
├ ❤️ Likes: `{likes}`
├ 💬 Comments: `{comments}`
├ 🔄 Shares: `{shares}`
└ 📌 Saves: `{saves}`

🔥 **Hashtag:** {hashtags if hashtags else 'Tidak ada'}
🎚️ **Format:** {'MP3 Audio' if format_type == 'audio' else 'MP4 Video'}
    """
    return caption