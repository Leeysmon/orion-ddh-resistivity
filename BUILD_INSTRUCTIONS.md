# Orion-DDH_v1 APK Build Instructions

## 🎯 Quick Summary
Your app code is **100% ready**. Choose one method below to build the APK.

---

## Option 1: Google Colab (Recommended - Easiest) ⭐

**Time:** 30-45 minutes | **Difficulty:** Easy

1. **Zip your project folder:**
   - Right-click on `ORION-DDH-RESISITIVITY` folder
   - Select "Compress to ZIP file"

2. **Open Google Colab:**
   - Go to [colab.research.google.com](https://colab.research.google.com)
   - Click **File → Upload notebook**
   - Upload `BUILD_APK_COLAB.ipynb` from this folder

3. **Run all cells:**
   - Click **Runtime → Run all**
   - When prompted, upload your ZIP file
   - Wait 30-45 minutes for build to complete
   - APK will automatically download when done

---

## Option 2: GitHub Actions (Automatic)

**Time:** 15-20 minutes | **Difficulty:** Easy

1. **Create GitHub repository:**
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/orion-ddh.git
   git push -u origin main
   ```

2. **The workflow runs automatically on push**
   - Go to your repo → Actions tab
   - Wait for build to complete
   - Download APK from "Artifacts"

---

## Option 3: Install WSL (Local Build)

**Time:** 1-2 hours first time | **Difficulty:** Medium

1. **Install WSL:**
   ```powershell
   wsl --install
   ```
   Restart computer when prompted.

2. **Open Ubuntu terminal and run:**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip build-essential git openjdk-17-jdk \
       autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
       libncursesw5-dev cmake libffi-dev libssl-dev

   pip3 install buildozer cython
   ```

3. **Navigate to project and build:**
   ```bash
   cd /mnt/c/Users/IRVGeo/Documents/13b-Python\ Project\ Files/Coding\ Projects\ -\ Apps/ORION-DDH-RESISITIVITY
   buildozer android debug
   ```

4. **APK will be in:** `bin/orion-ddh_v1-0.1-arm64-v8a_armeabi-v7a-debug.apk`

---

## 📱 Installing the APK on Android

1. Transfer APK to your phone (USB, email, Google Drive, etc.)
2. On phone: **Settings → Security → Allow unknown apps**
3. Navigate to the APK file and tap to install
4. Look for the Doraemon icon in your app drawer!

---

## ✅ Validation Status

| Check | Status |
|-------|--------|
| Python syntax | ✅ All files pass |
| Project structure | ✅ Complete |
| App icon (512x512) | ✅ Present |
| App icon (192x192) | ✅ Present |
| Buildozer spec | ✅ Configured |
| GitHub workflow | ✅ Ready |
| Colab notebook | ✅ Ready |

---

## 📝 App Features

- **Menu Screen:** Input New Data, HoleID, Settings with Doraemon mascot
- **HoleID Screen:** Configure hole parameters (ID, size, dates, project, logger)
- **Data Input:** Excel-style grid with auto-populated Date/Time
- **B → Blank:** Press B to instantly enter "Blank"
- **4th Blank Reminder:** Doraemon popup in Japanese (頑張って！)
- **Email Export:** Send CSV to registered email addresses
- **Delete Rows:** Individual delete buttons per entry

---

## 🆘 Troubleshooting

**Build fails with Java error:**
- Make sure Java 17 is installed
- Set `export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64`

**"NDK not found" error:**
- Buildozer will download NDK automatically on first run
- Requires ~2GB free space

**APK won't install:**
- Enable "Install unknown apps" in Android settings
- If still failing, try debug build first (as configured)

---

Built with ❤️ and Doraemon 🤖
