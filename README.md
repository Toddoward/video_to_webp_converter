# 🎬 MP4 to WebP Converter

🌍
[![English](https://img.shields.io/badge/lang-English-blue)](README.md)
[![Korean](https://img.shields.io/badge/lang-한국어-red)](README.ko.md)

A high-performance web-based tool for converting MP4 videos to WebP animations with advanced customization options.

## ✨ Features

- 🎥 **MP4 → WebP Conversion**: Generate high-quality animated WebP files
- 🎨 **Dark/Light Theme**: Auto-detect system preference with manual toggle
- 🌐 **Multi-language Support**: Auto-detect Korean/English with manual switching
- 📐 **Size Control**: Resize based on width or height with custom dimensions
- 🎚️ **Quality Settings**: Lossless/lossy compression options
- 📁 **Folder Management**: Web-based output folder selection
- 🔌 **One-click Shutdown**: Safe server shutdown from web interface

## 🚀 Quick Start

### Automatic Installation & Launch (Recommended)

1. **Download all files to a single folder**
2. **Double-click `start.bat`**
3. **Everything installs and runs automatically!**

### Manual Installation

```bash
# 1. Verify Python 3.8+ installation
python --version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server
python app.py

# 4. Open browser
# http://localhost:5000
```

## 📁 Project Structure

```
MP4-to-WebP-Converter/
├── start.bat              # Auto-installer and launcher script
├── app.py                 # Flask backend server
├── requirements.txt       # Python package dependencies
├── templates/
│   └── index.html        # Web frontend interface
├── uploads/              # Uploaded MP4 files (auto-created)
├── outputs/              # Converted WebP files (auto-created)
└── venv/                 # Virtual environment (auto-created)
```

## 🔧 System Requirements

- **Python 3.8+**
- **Windows 10/11** (works on other OS but batch file is Windows-only)
- **Minimum 4GB RAM** (Recommended: 8GB+)
- **OpenCV-compatible system**

## 📋 Dependencies

- `Flask` - Web server framework
- `opencv-python` - Video processing
- `Pillow` - Image processing and WebP generation
- `psutil` - System resource monitoring
- `Werkzeug` - Flask utilities
- `numpy` - Numerical computations

## 🎯 Usage

1. **Upload Files**: Drag & drop MP4 files or use file selector
2. **Adjust Settings**: Quality, compression, FPS, size, etc.
3. **Select Output Folder**: Choose where to save converted files
4. **Start Conversion**: Click "Start Conversion" button
5. **Download Results**: Download files after conversion completes

## 🌟 Advanced Features

### Theme Switching
- 🌙/☀️ button to toggle dark/light mode
- Auto-detect system preference

### Language Switching  
- 🌐 button to toggle Korean/English
- Auto-detect browser language

### Server Shutdown
- 🔌 button for safe server shutdown
- Closes both web interface and server

## 🛠️ Troubleshooting

### Python Not Installed
- Download from [Python Official Site](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation

### Package Installation Failed
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Run as administrator
# Or use virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Port Conflict
```python
# Edit last line in app.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### Browser Doesn't Open Automatically
- Manually navigate to `http://localhost:5000`
- Check Windows Firewall settings
- Try different browser

## 📜 License

This project is distributed under the MIT License.

## 🤝 Contributing

Bug reports, feature requests, and pull requests are welcome!

## 📞 Support

If you encounter issues, please create an issue or contact us.

## 🎉 Acknowledgments

- Built with Flask and OpenCV
- Uses Pillow for WebP generation
- Inspired by modern web design principles

---

💡 **Tip**: Create a desktop shortcut to `start.bat` for quick access!