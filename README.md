# 🎤 Voice-Controlled File Manager

A Python-based desktop application that allows you to manage files and folders using voice commands. Instead of manually clicking through folders, simply speak your commands!

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### Core Functionality
- 🎙️ **Voice Recognition** - Speak commands naturally
- 🔊 **Text-to-Speech Feedback** - Audio responses for all actions
- 📂 **Folder Navigation** - Open common folders (Downloads, Documents, Desktop, etc.)
- 🔍 **File Search** - Find files across multiple directories
- 📋 **File Listing** - View contents of folders
- 🗑️ **Safe File Deletion** - Delete files with confirmation dialog

### User Interface
- 🖥️ **Modern GUI** - Clean, dark-themed interface built with Tkinter
- 📝 **Command Log** - Real-time display of all voice commands and responses
- 🎛️ **Control Panel** - Easy-to-use buttons for starting/stopping voice recognition
- ❓ **Built-in Help** - Comprehensive command reference

### Safety Features
- ⚠️ **Deletion Confirmation** - GUI popup prevents accidental file deletion
- 🔒 **Limited Search Scope** - Searches only in safe, common directories
- 📊 **Command History** - Track all executed commands

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Microphone for voice input
- Internet connection (for Google Speech Recognition)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SelvaUx/voice-file-manager.git
   cd voice-file-manager
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Platform-Specific Setup

#### Windows
```bash
# Install PyAudio wheel for Windows
pip install pipwin
pipwin install pyaudio
```

#### macOS
```bash
# Install PortAudio for PyAudio
brew install portaudio
pip install pyaudio
```

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pyaudio portaudio19-dev python3-pip
pip install pyaudio
```

## 🗣️ Voice Commands

### Folder Operations
- **"Open downloads folder"** - Opens your Downloads directory
- **"Open documents folder"** - Opens your Documents directory
- **"Open desktop folder"** - Opens your Desktop directory
- **"Open home folder"** - Opens your home directory

### File Search
- **"Search for report.pdf"** - Finds files matching "report.pdf"
- **"Find presentation.pptx"** - Locates PowerPoint files
- **"Search for budget"** - Finds files containing "budget" in the name

### File Listing
- **"List files in downloads"** - Shows contents of Downloads folder
- **"Show files in documents"** - Displays files in Documents folder
- **"List files"** - Shows files in current directory

### File Deletion
- **"Delete test.txt"** - Deletes specified file (with confirmation)
- **"Delete old_report.pdf"** - Removes the specified PDF file

### Help & Control
- **"Help"** - Shows available voice commands
- Use GUI buttons to start/stop listening and clear logs

## 🛠️ How It Works

### Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Microphone    │───▶│  Speech-to-Text  │───▶│ Command Parser  │
│     Input       │    │   (Google API)   │    │   & Processor   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│      GUI        │◀───│  Text-to-Speech  │◀───│  File System    │
│   Interface     │    │    (pyttsx3)     │    │   Operations    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Key Components

1. **Speech Recognition** (`speech_recognition` library)
   - Uses Google's speech-to-text API
   - Handles ambient noise calibration
   - Continuous listening with timeout handling

2. **Text-to-Speech** (`pyttsx3` library)
   - Provides audio feedback for all actions
   - Cross-platform voice synthesis
   - Configurable speech rate and volume

3. **File Operations** (`os`, `pathlib` modules)
   - Safe file system navigation
   - Cross-platform path handling
   - Search functionality across common directories

4. **GUI Interface** (`tkinter`)
   - Real-time command logging
   - Visual feedback for system status
   - Control buttons and help system

## 📁 Project Structure

```
voice-file-manager/
│
├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── README.md           # This file
│
├── /demo              # Screenshots and demo videos
│   ├── demo.gif
│   └── screenshot.png
│
└── /docs              # Additional documentation
    └── COMMANDS.md    # Detailed command reference
```

## 🎯 Usage Examples

### Example Session
```
[09:15:32] 🤖 Voice File Manager initialized!
[09:15:35] 🎤 Heard: 'open downloads folder'
[09:15:35] ✅ Opened downloads folder
[09:15:45] 🎤 Heard: 'search for report'
[09:15:45] 🔍 Found 3 file(s) matching 'report':
[09:15:45]    📄 /Users/john/Documents/annual_report.pdf
[09:15:45]    📄 /Users/john/Downloads/report_draft.docx
[09:15:45]    📄 /Users/john/Desktop/sales_report.xlsx
```

## 🔧 Configuration

### Customizing Voice Settings
Edit the TTS settings in `main.py`:
```python
self.tts_engine.setProperty('rate', 180)    # Speech speed
self.tts_engine.setProperty('volume', 0.8)  # Volume level
```

### Adding Custom Directories
Extend the `common_dirs` dictionary:
```python
self.common_dirs = {
    'downloads': str(Path.home() / 'Downloads'),
    'projects': '/path/to/your/projects',    # Custom directory
    'work': '/path/to/work/folder',          # Another custom directory
    # ... existing directories
}
```

## 🐛 Troubleshooting

### Common Issues

**"No module named 'pyaudio'"**
- Install PyAudio using platform-specific instructions above

**"Could not understand audio"**
- Check microphone permissions
- Ensure stable internet connection
- Try speaking more clearly and closer to microphone

**"Speech recognition error"**
- Verify internet connection (Google API requires online access)
- Check firewall settings
- Try restarting the application

**"Permission denied" when deleting files**
- Ensure file is not open in another application
- Check file permissions
- Run as administrator if necessary (Windows)

### Performance Tips
- Close other audio applications to avoid microphone conflicts
- Use in a quiet environment for better recognition accuracy
- Speak at normal pace with clear pronunciation
- Keep file names simple when using voice commands

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

### Wanted Features
- [ ] Offline speech recognition using `vosk`
- [ ] Custom voice commands configuration
- [ ] File preview functionality
- [ ] Integration with cloud storage (Google Drive, Dropbox)
- [ ] Advanced search filters (by date, size, type)
- [ ] Voice-controlled file renaming
- [ ] Batch operations support

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - For speech-to-text functionality
- [pyttsx3](https://pypi.org/project/pyttsx3/) - For text-to-speech conversion
- [Google Speech Recognition API](https://cloud.google.com/speech-to-text) - For accurate voice recognition

## 📈 Roadmap

### Version 2.0 (Planned)
- [ ] Plugin system for custom commands
- [ ] Multi-language support
- [ ] Voice training for better recognition
- [ ] File operation undo/redo
- [ ] Integration with system notifications

### Version 1.5 (In Progress)
- [ ] Improved error handling
- [ ] Better GUI with themes
- [ ] Command shortcuts and aliases
- [ ] File operation history

---

⭐ **Star this repository if you found it helpful!**

📧 **Questions?** Open an issue or contact [selva.ux@yahoo.com](mailto:selva.ux@yahoo.com)
