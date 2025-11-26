# 🎧 LOCAL YouTube MP3 Downloader (320kbps) 

Welcome to the **LOCAL YouTube MP3 Downloader 320kbps** 

Made with ❤️ by ''**<SamXode/>**.''

---

## 🚀 Features You’ll Actually Care About

* ✔️ Download MP3 in **locked 320kbps CBR** 
* ✔️ Automatic audio quality verification using **ffprobe**
* ✔️ Supports single & batch downloads
* ✔️ Smart file duplicate checker
* ✔️ Full **cookies.txt** support (for age-restricted or premium videos)
* ✔️ Terminal aesthetic: hacker vibes only 😎

---

## 🧩 Installation Guide (Read This or Cry Later)

### 1️⃣ Install Python

Make sure you have **Python 3.8+** installed:

```
python --version
```

If not installed: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### 2️⃣ Install `yt-dlp`

```
pip install yt-dlp
```

### 3️⃣ Install FFmpeg + FFprobe (SUPER IMPORTANT)

This script **will not run** without FFmpeg.

Download FFmpeg:

* Windows: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
* macOS: `brew install ffmpeg`
* Linux: `sudo apt install ffmpeg`

Check installation:

```
ffmpeg -version
ffprobe -version
```

---

### 4️⃣ Prepare `cookies.txt` (Avoid YouTube Restrictions)

Without cookies, YouTube will gatekeep your downloads.

How to export:

1. Install Chrome extension: **Get cookies.txt LOCALLY**
2. Log in to YouTube
3. Open the extension → click **Export**
4. Save as `cookies.txt`
5. Place `cookies.txt` in the same folder as the script

Done.

---

## ▶️ How to Run the Script

1. Download the `.py` file
2. Make sure `cookies.txt` is in the same directory
3. Run:

```
python your_script_name.py
```

You’ll see a menu:

* **1 — Single Download**: One video at a time
* **2 — Multiple Download**: Download multiple URLs at once (comma-separated)
* **3 — Exit**: Bye 😭

---

## 📚 Usage

### Single Download

Enter a single YouTube URL → script downloads the MP3 → done.

### Multiple Download

Example input:

```
https://youtu.be/link1, https://youtu.be/link2, https://youtu.be/link3
```

The script will process them one by one.

---

## 🤝 Credits

Created by ''**<SamXode/>**'', designed to make your workflow smooth.

If you like this repo, smash that ⭐ star button on GitHub — it genuinely helps!

---

## 💬 NOTE

This tool is **free**, **clean**, and **open-source**. If you get errors, it’s almost always because your cookies expired — just re-export them.

Happy downloading! 🎶🔥
