import speech_recognition as sr
import pyttsx3
import os
import subprocess
import platform
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
import json
import time

class VoiceFileManager:
    def __init__(self):
        # Initialize speech recognition and text-to-speech
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.8)
        
        # State management
        self.is_listening = False
        self.command_history = []
        
        # Common directories
        self.common_dirs = {
            'downloads': str(Path.home() / 'Downloads'),
            'documents': str(Path.home() / 'Documents'),
            'desktop': str(Path.home() / 'Desktop'),
            'pictures': str(Path.home() / 'Pictures'),
            'music': str(Path.home() / 'Music'),
            'videos': str(Path.home() / 'Videos'),
            'home': str(Path.home())
        }
        
        # Setup GUI
        self.setup_gui()
        
        # Initialize microphone
        self.calibrate_microphone()
    
    def setup_gui(self):
        """Create the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Voice File Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🎤 Voice File Manager", 
                              font=('Arial', 20, 'bold'), 
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#2c3e50')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(status_frame, text="Ready to listen...", 
                                   font=('Arial', 12), 
                                   fg='#27ae60', bg='#2c3e50')
        self.status_label.pack(side=tk.LEFT)
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.listen_button = tk.Button(button_frame, text="🎤 Start Listening", 
                                     command=self.toggle_listening,
                                     font=('Arial', 12, 'bold'),
                                     bg='#27ae60', fg='white',
                                     relief=tk.FLAT, padx=20, pady=10)
        self.listen_button.pack(side=tk.LEFT, padx=(0, 10))
        
        help_button = tk.Button(button_frame, text="❓ Help", 
                               command=self.show_help,
                               font=('Arial', 12),
                               bg='#3498db', fg='white',
                               relief=tk.FLAT, padx=20, pady=10)
        help_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(button_frame, text="🗑️ Clear Log", 
                                command=self.clear_log,
                                font=('Arial', 12),
                                bg='#e74c3c', fg='white',
                                relief=tk.FLAT, padx=20, pady=10)
        clear_button.pack(side=tk.LEFT)
        
        # Log area
        log_label = tk.Label(main_frame, text="Command Log:", 
                           font=('Arial', 12, 'bold'), 
                           fg='#ecf0f1', bg='#2c3e50')
        log_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, 
                                                 height=15, 
                                                 font=('Consolas', 10),
                                                 bg='#34495e', fg='#ecf0f1',
                                                 insertbackground='white')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add some initial help text
        self.log_message("🤖 Voice File Manager initialized!")
        self.log_message("📋 Say commands like:")
        self.log_message("   • 'Open downloads folder'")
        self.log_message("   • 'Search for report.pdf'")
        self.log_message("   • 'Delete test.txt'")
        self.log_message("   • 'List files in documents'")
        self.log_message("🎤 Click 'Start Listening' to begin!")
    
    def calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.log_message("🎙️ Microphone calibrated successfully")
        except Exception as e:
            self.log_message(f"❌ Microphone calibration failed: {str(e)}")
    
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
    
    def speak(self, text):
        """Convert text to speech"""
        def tts_thread():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        threading.Thread(target=tts_thread, daemon=True).start()
    
    def toggle_listening(self):
        """Toggle voice listening on/off"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start continuous voice listening"""
        self.is_listening = True
        self.listen_button.config(text="🛑 Stop Listening", bg='#e74c3c')
        self.status_label.config(text="Listening for commands...", fg='#e74c3c')
        
        def listen_thread():
            while self.is_listening:
                try:
                    with self.microphone as source:
                        # Listen for audio with timeout
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Recognize speech
                    command = self.recognizer.recognize_google(audio).lower()
                    self.log_message(f"🎤 Heard: '{command}'")
                    self.process_command(command)
                    
                except sr.WaitTimeoutError:
                    # Timeout is normal, continue listening
                    pass
                except sr.UnknownValueError:
                    # Could not understand audio
                    pass
                except sr.RequestError as e:
                    self.log_message(f"❌ Speech recognition error: {e}")
                    break
                except Exception as e:
                    self.log_message(f"❌ Listening error: {e}")
                    break
        
        threading.Thread(target=listen_thread, daemon=True).start()
    
    def stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.listen_button.config(text="🎤 Start Listening", bg='#27ae60')
        self.status_label.config(text="Ready to listen...", fg='#27ae60')
    
    def process_command(self, command):
        """Process voice command"""
        self.command_history.append(command)
        
        try:
            if "open" in command and "folder" in command:
                self.handle_open_folder(command)
            elif "search" in command or "find" in command:
                self.handle_search_file(command)
            elif "delete" in command:
                self.handle_delete_file(command)
            elif "list" in command or "show" in command:
                self.handle_list_files(command)
            elif "help" in command:
                self.show_help_voice()
            else:
                response = "❓ Command not recognized. Say 'help' for available commands."
                self.log_message(response)
                self.speak("Command not recognized")
        
        except Exception as e:
            error_msg = f"❌ Error processing command: {str(e)}"
            self.log_message(error_msg)
            self.speak("Sorry, there was an error processing your command")
    
    def handle_open_folder(self, command):
        """Handle folder opening commands"""
        folder_name = None
        
        # Check for common folder names
        for folder in self.common_dirs.keys():
            if folder in command:
                folder_name = folder
                break
        
        if folder_name and folder_name in self.common_dirs:
            folder_path = self.common_dirs[folder_name]
            if os.path.exists(folder_path):
                self.open_path(folder_path)
                response = f"✅ Opened {folder_name} folder"
                self.log_message(response)
                self.speak(f"Opened {folder_name} folder")
            else:
                response = f"❌ {folder_name} folder not found"
                self.log_message(response)
                self.speak(f"{folder_name} folder not found")
        else:
            response = "❓ Please specify a folder name (downloads, documents, desktop, etc.)"
            self.log_message(response)
            self.speak("Please specify a valid folder name")
    
    def handle_search_file(self, command):
        """Handle file search commands"""
        # Extract filename from command
        words = command.split()
        filename = None
        
        # Look for filename after "for" or "find"
        try:
            if "for" in words:
                idx = words.index("for") + 1
                filename = " ".join(words[idx:])
            elif "find" in words:
                idx = words.index("find") + 1
                filename = " ".join(words[idx:])
        except:
            pass
        
        if filename:
            results = self.search_files(filename)
            if results:
                self.log_message(f"🔍 Found {len(results)} file(s) matching '{filename}':")
                for result in results[:5]:  # Show max 5 results
                    self.log_message(f"   📄 {result}")
                self.speak(f"Found {len(results)} files matching {filename}")
            else:
                response = f"❌ No files found matching '{filename}'"
                self.log_message(response)
                self.speak(f"No files found matching {filename}")
        else:
            response = "❓ Please specify a filename to search for"
            self.log_message(response)
            self.speak("Please specify a filename to search for")
    
    def handle_delete_file(self, command):
        """Handle file deletion commands"""
        # Extract filename from command
        words = command.split()
        filename = None
        
        try:
            if "delete" in words:
                idx = words.index("delete") + 1
                filename = " ".join(words[idx:])
        except:
            pass
        
        if filename:
            # Search for the file first
            results = self.search_files(filename)
            if results:
                # For safety, ask for confirmation through GUI
                result = messagebox.askyesno("Confirm Deletion", 
                                           f"Delete '{results[0]}'?\n\nThis action cannot be undone!")
                if result:
                    try:
                        os.remove(results[0])
                        response = f"✅ Deleted '{filename}'"
                        self.log_message(response)
                        self.speak(f"Deleted {filename}")
                    except Exception as e:
                        response = f"❌ Failed to delete '{filename}': {str(e)}"
                        self.log_message(response)
                        self.speak("Failed to delete file")
                else:
                    response = "❌ Deletion cancelled"
                    self.log_message(response)
                    self.speak("Deletion cancelled")
            else:
                response = f"❌ File '{filename}' not found"
                self.log_message(response)
                self.speak(f"File {filename} not found")
        else:
            response = "❓ Please specify a filename to delete"
            self.log_message(response)
            self.speak("Please specify a filename to delete")
    
    def handle_list_files(self, command):
        """Handle file listing commands"""
        folder_name = "current"
        
        # Check for specific folder
        for folder in self.common_dirs.keys():
            if folder in command:
                folder_name = folder
                break
        
        if folder_name == "current":
            folder_path = os.getcwd()
        else:
            folder_path = self.common_dirs.get(folder_name, os.getcwd())
        
        try:
            files = os.listdir(folder_path)
            self.log_message(f"📁 Files in {folder_name} folder ({len(files)} items):")
            for file in files[:10]:  # Show max 10 files
                self.log_message(f"   📄 {file}")
            if len(files) > 10:
                self.log_message(f"   ... and {len(files) - 10} more items")
            
            self.speak(f"Listed files in {folder_name} folder")
        except Exception as e:
            response = f"❌ Failed to list files: {str(e)}"
            self.log_message(response)
            self.speak("Failed to list files")
    
    def search_files(self, filename):
        """Search for files matching the given name"""
        results = []
        search_paths = [Path.home() / 'Downloads', Path.home() / 'Documents', 
                       Path.home() / 'Desktop', Path.cwd()]
        
        for search_path in search_paths:
            if search_path.exists():
                try:
                    for root, dirs, files in os.walk(str(search_path)):
                        for file in files:
                            if filename.lower() in file.lower():
                                results.append(os.path.join(root, file))
                        # Limit search depth to avoid long searches
                        if len(results) >= 10:
                            break
                except:
                    continue
        
        return results
    
    def open_path(self, path):
        """Open file or folder using system default"""
        try:
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', path])
            else:  # Linux
                subprocess.run(['xdg-open', path])
        except Exception as e:
            self.log_message(f"❌ Failed to open {path}: {str(e)}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """🎤 Voice File Manager - Commands:

📂 FOLDER OPERATIONS:
• "Open downloads folder"
• "Open documents folder"  
• "Open desktop folder"

🔍 SEARCH OPERATIONS:
• "Search for report.pdf"
• "Find presentation.pptx"

📋 LIST OPERATIONS:
• "List files in downloads"
• "Show files in documents"

🗑️ DELETE OPERATIONS:
• "Delete test.txt"
• "Delete old_file.doc"

❓ OTHER:
• "Help" - Show this help

💡 TIPS:
• Speak clearly and at normal speed
• File names should be specific
• Deletion requires confirmation for safety
• Search works across common folders"""
        
        messagebox.showinfo("Voice File Manager Help", help_text)
    
    def show_help_voice(self):
        """Show help via voice"""
        self.log_message("📋 Available commands: open folder, search file, list files, delete file")
        self.speak("Available commands are: open folder, search file, list files, and delete file")
    
    def clear_log(self):
        """Clear the command log"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🗑️ Log cleared")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🎤 Starting Voice File Manager...")
    
    # Check for required dependencies
    try:
        import speech_recognition
        import pyttsx3
    except ImportError as e:
        print(f"❌ Missing required dependency: {e}")
        print("📦 Install with: pip install speechrecognition pyttsx3 pyaudio")
        return
    
    # Start the application
    app = VoiceFileManager()
    app.run()

if __name__ == "__main__":
    main()
