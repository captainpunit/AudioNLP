import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import pyttsx3
from translator import translate_to_hindi
from nlp_processor import NLPProcessor

# Try to import speech recognition
try:
    from speech_to_text import recognize_speech
    SPEECH_AVAILABLE = True
except:
    SPEECH_AVAILABLE = False
    print("Warning: Speech recognition not available")


class AudioTranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 English to Hindi Audio Translator with NLP")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.nlp_processor = NLPProcessor()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        
        self.is_recording = False
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI components"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🎤 English to Hindi Translator", 
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.grid(row=0, column=0, pady=10)
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        self.record_btn = tk.Button(
            button_frame,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            bg='#3498db',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.record_btn.pack(side=tk.LEFT, padx=5)
        
        self.translate_btn = tk.Button(
            button_frame,
            text="🌐 Translate",
            command=self.translate_text,
            bg='#2ecc71',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.translate_btn.pack(side=tk.LEFT, padx=5)
        
        self.speak_btn = tk.Button(
            button_frame,
            text="🔊 Speak Hindi",
            command=self.speak_hindi,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.speak_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear All",
            command=self.clear_all,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = tk.Label(
            control_frame,
            text="Ready",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.status_label.pack(pady=5)
        
        # Main Content Area
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left Panel - English Text
        left_panel = ttk.LabelFrame(content_frame, text="📝 English Text", padding="10")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(0, weight=1)
        
        self.english_text = scrolledtext.ScrolledText(
            left_panel,
            wrap=tk.WORD,
            font=('Arial', 11),
            height=15,
            bg='white',
            fg='#2c3e50'
        )
        self.english_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Right Panel - Hindi Translation
        right_panel = ttk.LabelFrame(content_frame, text="🌐 Hindi Translation", padding="10")
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        
        self.hindi_text = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            font=('Arial', 11),
            height=15,
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.hindi_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.hindi_text.config(state=tk.DISABLED)
        
        # NLP Analysis Panel
        nlp_frame = ttk.LabelFrame(main_frame, text="🧠 NLP Analysis", padding="10")
        nlp_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        nlp_frame.columnconfigure(0, weight=1)
        
        self.nlp_text = scrolledtext.ScrolledText(
            nlp_frame,
            wrap=tk.WORD,
            font=('Courier', 9),
            height=8,
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.nlp_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.nlp_text.config(state=tk.DISABLED)
    
    def update_status(self, message, color='#7f8c8d'):
        """Update status label"""
        self.status_label.config(text=message, fg=color)
        self.root.update_idletasks()
    
    def toggle_recording(self):
        """Start or stop recording"""
        if not SPEECH_AVAILABLE:
            messagebox.showwarning(
                "Speech Recognition Unavailable",
                "Speech recognition module is not available.\n"
                "Please type your text manually."
            )
            return
        
        if not self.is_recording:
            self.is_recording = True
            self.record_btn.config(text="⏹️ Stop Recording", bg='#e74c3c')
            self.update_status("🎤 Listening... Speak now!", '#e74c3c')
            
            # Run speech recognition in a separate thread
            thread = threading.Thread(target=self.record_speech)
            thread.daemon = True
            thread.start()
        else:
            self.is_recording = False
            self.record_btn.config(text="🎤 Start Recording", bg='#3498db')
            self.update_status("Recording stopped", '#7f8c8d')
    
    def record_speech(self):
        """Record speech and convert to text"""
        try:
            text = recognize_speech()
            
            if text:
                self.english_text.delete(1.0, tk.END)
                self.english_text.insert(1.0, text)
                self.update_status(f"✅ Recognized: {text[:50]}...", '#2ecc71')
                
                # Auto-translate
                self.translate_text()
            else:
                self.update_status("❌ No speech detected", '#e74c3c')
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", '#e74c3c')
        finally:
            self.is_recording = False
            self.record_btn.config(text="🎤 Start Recording", bg='#3498db')
    
    def translate_text(self):
        """Translate English text to Hindi"""
        english = self.english_text.get(1.0, tk.END).strip()
        
        if not english:
            messagebox.showwarning("No Text", "Please enter or record some English text first.")
            return
        
        self.update_status("🌐 Translating...", '#f39c12')
        self.root.update_idletasks()
        
        # Run translation in thread to prevent UI freezing
        thread = threading.Thread(target=self._translate_worker, args=(english,))
        thread.daemon = True
        thread.start()
    
    def _translate_worker(self, text):
        """Worker thread for translation"""
        try:
            # Translate
            hindi = translate_to_hindi(text)
            
            # Update Hindi text
            self.hindi_text.config(state=tk.NORMAL)
            self.hindi_text.delete(1.0, tk.END)
            self.hindi_text.insert(1.0, hindi)
            self.hindi_text.config(state=tk.DISABLED)
            
            # Perform NLP analysis
            self.analyze_text(text)
            
            self.update_status("✅ Translation complete!", '#2ecc71')
        except Exception as e:
            self.update_status(f"❌ Translation error: {str(e)}", '#e74c3c')
    
    def analyze_text(self, text):
        """Perform NLP analysis on text"""
        try:
            analysis = self.nlp_processor.process(text)
            
            # Format analysis output
            output = "="*50 + "\n"
            output += "TEXT ANALYSIS\n"
            output += "="*50 + "\n\n"
            
            output += f"📊 Statistics:\n"
            output += f"   • Words: {analysis['word_count']}\n"
            output += f"   • Sentences: {analysis['sentence_count']}\n\n"
            
            if analysis['keywords']:
                output += f"🔑 Keywords:\n"
                output += f"   {', '.join(analysis['keywords'][:15])}\n\n"
            
            if analysis['entities']:
                output += f"🏷️  Named Entities:\n"
                for ent in analysis['entities'][:10]:
                    output += f"   • {ent['text']} ({ent['label']})\n"
                output += "\n"
            
            if analysis['pos_tags']:
                # Count POS tags
                pos_counts = {}
                for item in analysis['pos_tags']:
                    pos = item['pos']
                    pos_counts[pos] = pos_counts.get(pos, 0) + 1
                
                output += f"📝 Part of Speech Distribution:\n"
                for pos, count in sorted(pos_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                    output += f"   • {pos}: {count}\n"
            
            # Update NLP text widget
            self.nlp_text.config(state=tk.NORMAL)
            self.nlp_text.delete(1.0, tk.END)
            self.nlp_text.insert(1.0, output)
            self.nlp_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"NLP Analysis error: {e}")
    
    def speak_hindi(self):
        """Speak the Hindi translation"""
        hindi = self.hindi_text.get(1.0, tk.END).strip()
        
        if not hindi:
            messagebox.showwarning("No Translation", "Please translate some text first.")
            return
        
        self.update_status("🔊 Speaking...", '#9b59b6')
        
        # Run TTS in thread
        thread = threading.Thread(target=self._speak_worker, args=(hindi,))
        thread.daemon = True
        thread.start()
    
    def _speak_worker(self, text):
        """Worker thread for text-to-speech"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.update_status("✅ Speech complete!", '#2ecc71')
        except Exception as e:
            self.update_status(f"❌ Speech error: {str(e)}", '#e74c3c')
    
    def clear_all(self):
        """Clear all text fields"""
        self.english_text.delete(1.0, tk.END)
        self.hindi_text.config(state=tk.NORMAL)
        self.hindi_text.delete(1.0, tk.END)
        self.hindi_text.config(state=tk.DISABLED)
        self.nlp_text.config(state=tk.NORMAL)
        self.nlp_text.delete(1.0, tk.END)
        self.nlp_text.config(state=tk.DISABLED)
        self.update_status("Ready", '#7f8c8d')


def main():
    root = tk.Tk()
    app = AudioTranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()