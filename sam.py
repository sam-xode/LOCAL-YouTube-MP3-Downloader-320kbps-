import os
import yt_dlp
from pathlib import Path
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    banner = """
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║      YOUTUBE MP3 DOWNLOADER (320kbps)            ║
    ║              BY <SamXode/>                       ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
    """
    print(banner)

def create_download_folder():
    folder_name = "downloaded mp3"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"✓ Folder '{folder_name}' berhasil dibuat!\n")
    return folder_name

def check_cookies_file():
    """Cek apakah cookies.txt ada dan valid"""
    if os.path.exists('cookies.txt'):
        try:
            with open('cookies.txt', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'youtube.com' in content and len(content) > 100:
                    return True
        except:
            pass
    return False

def show_cookie_instructions():
    """Tampilkan instruksi cara export cookies"""
    print("\n" + "="*60)
    print("📋 CARA EXPORT COOKIES DARI CHROME:")
    print("="*60)
    print("1. Install Extension 'Get cookies.txt LOCALLY':")
    print("   https://chromewebstore.google.com/detail/cclelndahbckbenkjhflpdbgdldlbecc")
    print("\n2. Buka YouTube.com dan pastikan Anda SUDAH LOGIN")
    print("\n3. Klik icon extension (puzzle icon) → 'Get cookies.txt LOCALLY'")
    print("\n4. Klik 'Export' → Save file sebagai 'cookies.txt'")
    print("\n5. Letakkan file cookies.txt di folder yang SAMA dengan script ini")
    print("   Lokasi: " + os.getcwd())
    print("\n6. Jalankan script lagi")
    print("="*60 + "\n")

def check_file_exists(folder, url, use_cookies=False):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'cookies.txt' if use_cookies and os.path.exists('cookies.txt') else None,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = f"{info['title']}.mp3"
            filepath = os.path.join(folder, filename)
            return os.path.exists(filepath), filename
    except:
        return False, None

def verify_audio_quality(filepath):
    """Verifikasi kualitas audio menggunakan ffprobe"""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'stream=bit_rate,codec_name',
            '-of', 'default=noprint_wrappers=1',
            filepath
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        output = result.stdout
        
        # Ekstrak bitrate
        bitrate = None
        for line in output.split('\n'):
            if 'bit_rate=' in line:
                try:
                    bitrate = int(line.split('=')[1])
                    bitrate_kbps = bitrate // 1000
                    return bitrate_kbps
                except:
                    pass
        return None
    except:
        return None

def download_mp3(url, folder):
    try:
        print(f"\n{'='*50}")
        print(f"🔄 Memproses URL... klik CTRL + C UNTUK MELANJUTKAN")
        print(f"{'='*50}")
        
        # Cek apakah ada cookies.txt
        has_valid_cookies = check_cookies_file()
        
        if not has_valid_cookies:
            print("\n⚠️  cookies.txt tidak ditemukan atau tidak valid!")
            show_cookie_instructions()
            choice = input("Apakah Anda sudah meletakkan cookies.txt? (y/n): ").strip().lower()
            if choice != 'y':
                print("❌ Download dibatalkan. Export cookies dulu ya!\n")
                return False
        
        # Cek apakah file sudah ada
        exists, filename = check_file_exists(folder, url, use_cookies=True)
        
        if exists:
            print(f"\n⚠️  WARNING: File '{filename}' sudah ada!")
            choice = input("Tetap download? (y/n): ").strip().lower()
            if choice != 'y':
                print("⏭️  Download di-skip.\n")
                return True
        
        # Konfigurasi yt-dlp dengan LOCKED 320kbps CBR
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'cookiefile': 'cookies.txt',
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False,
            'writethumbnail': False,
            'embedthumbnail': False,
            # KUNCI: FFmpeg args untuk FORCE 320kbps CBR (bukan VBR)
            'postprocessor_args': [
                '-acodec', 'libmp3lame',   # Codec MP3 LAME
                '-b:a', '320k',             # Bitrate FIXED 320kbps
                '-ar', '48000',             # Sample rate 48kHz
                '-ac', '2',                 # Stereo 2 channels
                '-write_xing', '0',         # Disable VBR header
            ],
        }
        
        print(f"\n🍪 Menggunakan cookies.txt")
        print(f"🔽 Mendownload dari: {url}")
        print(f"🎵 Target: MP3 320kbps CBR\n")
        sys.stdout.flush()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info['title']
            print(f"📹 Judul: {video_title}")
            print(f"⏳ Mendownload...\n")
            sys.stdout.flush()
            ydl.download([url])
        
        # Verifikasi kualitas file yang didownload
        mp3_file = os.path.join(folder, f"{video_title}.mp3")
        if os.path.exists(mp3_file):
            print("\n🔍 Memverifikasi kualitas audio...")
            sys.stdout.flush()
            bitrate = verify_audio_quality(mp3_file)
            if bitrate:
                if bitrate >= 310:  # Toleransi kecil untuk CBR encoding
                    print(f"✓ Download berhasil! Bitrate: {bitrate}kbps ✓ 320kbps")
                else:
                    print(f"⚠️  Download berhasil, tapi bitrate: {bitrate}kbps (kurang dari 320kbps)")
                    print(f"   Source audio mungkin tidak tersedia dalam 320kbps")
            else:
                print("✓ Download berhasil! (Tidak bisa verifikasi bitrate)")
        
        print()
        sys.stdout.flush()
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error: {error_msg}\n")
        sys.stdout.flush()
        
        if 'sign in' in error_msg.lower() or 'cookie' in error_msg.lower():
            print("⚠️  Cookies tidak valid atau expired!")
            show_cookie_instructions()
        elif 'format' in error_msg.lower() or 'signature' in error_msg.lower():
            print("⚠️  Gagal mengekstrak format video.")
            print("💡 Coba solusi berikut:")
            print("   1. Update yt-dlp: pip install -U yt-dlp")
            print("   2. Refresh cookies.txt (export ulang dari browser)")
            print("   3. Pastikan video tidak private/age-restricted")
        
        return False

def single_download(folder):
    while True:
        try:
            print()  # Newline untuk spacing
            sys.stdout.flush()
            url = input("Masukkan URL YouTube: ").strip()
            
            if not url:
                print("❌ URL tidak boleh kosong!")
                continue
            
            # Langsung proses download
            download_mp3(url, folder)
            
            # Pastikan output buffer clear sebelum minta input lagi
            sys.stdout.flush()
            sys.stderr.flush()
            
            # Tanya user mau download lagi atau tidak
            while True:
                print()  # Newline untuk spacing
                sys.stdout.flush()
                again = input("Download lagi? (y/n): ").strip().lower()
                
                if again in ['y', 'n']:
                    break
                else:
                    print("❌ Input tidak valid! Masukkan 'y' atau 'n'")
            
            if again != 'y':
                print("📌 Kembali ke menu utama...\n")
                break
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Download dibatalkan oleh user.")
            break
        except EOFError:
            print("\n\n⚠️  Input error.")
            break

def multiple_download(folder):
    try:
        print()  # Newline untuk spacing
        sys.stdout.flush()
        urls_input = input("Masukkan URL YouTube (pisahkan dengan koma): ").strip()
        
        if not urls_input:
            print("❌ Input tidak boleh kosong!")
            return
        
        urls = [url.strip() for url in urls_input.split(',') if url.strip()]
        
        if not urls:
            print("❌ Tidak ada URL yang valid!")
            return
        
        print(f"\n📋 Total {len(urls)} video akan didownload\n")
        sys.stdout.flush()
        
        success_count = 0
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*50}")
            print(f"Download {i}/{len(urls)}")
            print(f"{'='*50}")
            sys.stdout.flush()
            
            if download_mp3(url, folder):
                success_count += 1
        
        print(f"\n{'='*50}")
        print(f"✓ Selesai! {success_count}/{len(urls)} berhasil didownload")
        print(f"{'='*50}\n")
        sys.stdout.flush()
        
        # Tanya user mau download lagi atau tidak
        while True:
            print()
            sys.stdout.flush()
            again = input("Download lagi? (y/n): ").strip().lower()
            
            if again in ['y', 'n']:
                break
            else:
                print("❌ Input tidak valid! Masukkan 'y' atau 'n'")
        
        if again == 'y':
            # Rekursif: panggil lagi multiple_download
            multiple_download(folder)
        else:
            print("📌 Kembali ke menu utama...\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Download dibatalkan oleh user.")
    except EOFError:
        print("\n\n⚠️  Input error.")

def main():
    try:
        clear_screen()
        show_banner()
        
        # Cek yt-dlp version
        try:
            result = os.popen('yt-dlp --version').read().strip()
            print(f"✓ yt-dlp version: {result}")
        except:
            print("⚠️  Tidak bisa cek versi yt-dlp")
        
        # Cek FFmpeg
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✓ FFmpeg terdeteksi")
            else:
                print("⚠️  FFmpeg tidak terdeteksi!")
                print("   Download dari: https://ffmpeg.org/download.html\n")
                return
        except:
            print("⚠️  FFmpeg tidak terdeteksi!")
            print("   Download dari: https://ffmpeg.org/download.html\n")
            return
        
        # Cek ffprobe (untuk verifikasi kualitas)
        try:
            result = subprocess.run(['ffprobe', '-version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✓ FFprobe terdeteksi (untuk verifikasi kualitas)")
        except:
            print("⚠️  FFprobe tidak terdeteksi (verifikasi kualitas tidak tersedia)")
        
        # Cek cookies
        if check_cookies_file():
            print("✓ cookies.txt ditemukan dan valid\n")
        else:
            print("⚠️  cookies.txt tidak ditemukan atau tidak valid")
            show_cookie_instructions()
            input("\nTekan ENTER setelah meletakkan cookies.txt...")
            
            if not check_cookies_file():
                print("\n❌ cookies.txt masih tidak valid. Script tidak bisa berjalan.")
                print("   Pastikan Anda sudah export cookies dengan benar!\n")
                return
            else:
                print("✓ cookies.txt valid!\n")
        
        folder = create_download_folder()
        
        while True:
            try:
                print("\n" + "="*50)
                print("PILIH OPSI:")
                print("="*50)
                print("1. Single Download")
                print("2. Multiple Download")
                print("3. Keluar")
                print("="*50)
                
                choice = input("\nPilih opsi (1/2/3): ").strip()
                sys.stdout.flush()
                
                if choice == '1':
                    single_download(folder)
                elif choice == '2':
                    multiple_download(folder)
                elif choice == '3':
                    print("\n👋 Terima kasih telah menggunakan YouTube MP3 Downloader!")
                    print("    Created by <SamXode/>\n")
                    break
                else:
                    print("❌ Pilihan tidak valid! Silakan pilih 1, 2, atau 3.")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Program dibatalkan oleh user.")
                print("👋 Terima kasih telah menggunakan YouTube MP3 Downloader!")
                print("    Created by <SamXode/>\n")
                break
            except EOFError:
                print("\n\n⚠️  Input error. Program dihentikan.")
                break
                
    except Exception as e:
        print(f"\n❌ Error tidak terduga: {e}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
