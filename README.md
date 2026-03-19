# Orion-DDH_v1

DDH Resistivity Data Logger Android Application built with Kivy.

## Features

- **Menu Screen**: Main navigation with options for Data Input, Hole ID setup, and Settings
- **Hole ID Screen**: Configure hole metadata (HoleID, HoleSize, StartDate, EndDate, Project, Logger)
- **Data Input Screen**: Excel-style table for entering resistivity measurements
  - Auto-timestamps Date and Time when data is entered
  - Auto-populates HoleID and HoleSize from Hole ID configuration
  - Columns: Date, HoleID, HoleSize, Box #, Time, V1[V], V2[mV], Comment
- **Settings Screen**: Configure app preferences and defaults
- **CSV Export**: Export measurement data to CSV files

## Data Columns

| Column | Type | Description |
|--------|------|-------------|
| Date | Auto | Automatically captured from device when Box # is entered |
| HoleID | Auto | Populated from Hole ID screen |
| HoleSize | Auto | Populated from Hole ID screen |
| Box # | Input | User input - categorical/numeric |
| Time | Auto | Automatically captured from device when Box # is entered |
| V1[V] | Input | Numeric voltage reading |
| V2[mV] | Input | Numeric millivolt reading |
| Comment | Input | Text comments |

## Running on Desktop (Testing)

1. Install Python 3.8+ and pip
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Building for Android

### Prerequisites

1. **Linux environment** (or WSL on Windows)
2. Install buildozer:
   ```bash
   pip install buildozer
   ```
3. Install system dependencies (Ubuntu/Debian):
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

### Build Commands

**Debug APK:**
```bash
buildozer android debug
```

**Release APK:**
```bash
buildozer android release
```

The APK will be created in the `bin/` directory.

### First Build

The first build will take a long time as it downloads Android SDK, NDK, and builds all dependencies.

## Installing on Android Device

1. Enable "Install from Unknown Sources" in Android settings
2. Transfer the APK to your device
3. Tap the APK file to install

Or use ADB:
```bash
buildozer android debug deploy run
```

## File Structure

```
ORION-DDH-RESISITIVITY/
├── main.py                 # Application entry point
├── buildozer.spec          # Android build configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── screens/               # UI screens
│   ├── __init__.py
│   ├── menu_screen.py     # Main menu
│   ├── holeid_screen.py   # Hole ID configuration
│   ├── data_input_screen.py # Data table input
│   └── settings_screen.py # App settings
└── data/                  # Data management
    ├── __init__.py
    └── data_manager.py    # Data storage & export
```

## Version

Version 1.3
