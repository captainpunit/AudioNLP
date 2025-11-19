"""
Automated setup script for downloading translation models
Run this script once to download and setup all required models
"""

import os
import sys
from pathlib import Path

def setup_translation_model():
    """Download and setup the English-Hindi translation model"""
    try:
        from transformers import MarianMTModel, MarianTokenizer
    except ImportError:
        print("❌ Error: transformers package not installed")
        print("   Install it using: pip install transformers torch")
        return False
    
    model_name = "Helsinki-NLP/opus-mt-en-hi"
    
    # Determine save path
    current_dir = Path(__file__).parent
    save_path = current_dir / "models" / "opus-mt-en-hi"
    
    print("="*60)
    print("🚀 Audio Translator - Model Setup")
    print("="*60)
    print()
    print(f"📥 Downloading translation model: {model_name}")
    print(f"💾 Save location: {save_path}")
    print()
    print("⏳ This may take 2-5 minutes (downloading ~300MB)...")
    print()
    
    try:
        # Create directory if it doesn't exist
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Download tokenizer
        print("1/2 Downloading tokenizer...")
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(str(save_path))
        print("   ✅ Tokenizer downloaded")
        
        # Download model
        print("2/2 Downloading model...")
        model = MarianMTModel.from_pretrained(model_name)
        model.save_pretrained(str(save_path))
        print("   ✅ Model downloaded")
        
        print()
        print("="*60)
        print("✅ SUCCESS! Translation model setup complete!")
        print("="*60)
        print()
        print("📝 Next steps:")
        print("   1. Download Vosk speech model from:")
        print("      https://alphacephei.com/vosk/models")
        print("   2. Extract to: models/vosk_model/")
        print("   3. Run the application: python gui_app.py")
        print()
        return True
        
    except Exception as e:
        print()
        print("="*60)
        print("❌ ERROR during download")
        print("="*60)
        print(f"Error: {str(e)}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Check your internet connection")
        print("   2. Make sure you have enough disk space (~1GB)")
        print("   3. Try running: pip install --upgrade transformers")
        print()
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...")
    print()
    
    required_packages = {
        'transformers': 'transformers',
        'torch': 'torch',
        'sentencepiece': 'sentencepiece',
        'pyttsx3': 'pyttsx3',
        'vosk': 'vosk',
        'sounddevice': 'sounddevice',
        'spacy': 'spacy',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    
    for package_import, package_name in required_packages.items():
        try:
            __import__(package_import)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - NOT INSTALLED")
            missing_packages.append(package_name)
    
    print()
    
    if missing_packages:
        print("⚠️  Missing packages detected!")
        print()
        print("📦 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        print()
        print("Or install all at once:")
        print("   pip install -r requirements.txt")
        print()
        
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    else:
        print("✅ All dependencies installed!")
        print()
    
    return True


def check_spacy_model():
    """Check if SpaCy English model is installed"""
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            print("✅ SpaCy English model installed")
            return True
        except OSError:
            print("⚠️  SpaCy English model not found")
            print()
            print("📥 Install it using:")
            print("   python -m spacy download en_core_web_sm")
            print()
            return False
    except ImportError:
        print("⚠️  SpaCy not installed")
        return False


def main():
    """Main setup function"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     🎤 English to Hindi Audio Translator - Setup          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Setup cancelled. Please install missing dependencies first.")
        sys.exit(1)
    
    print()
    
    # Check SpaCy model
    check_spacy_model()
    
    print()
    
    # Setup translation model
    print("─" * 60)
    response = input("📥 Download translation model now? (y/n): ")
    
    if response.lower() == 'y':
        success = setup_translation_model()
        if success:
            print("🎉 Setup completed successfully!")
            print()
            print("🚀 You can now run the application:")
            print("   python gui_app.py")
            print()
        else:
            print("⚠️  Setup completed with errors")
            sys.exit(1)
    else:
        print()
        print("ℹ️  Model download skipped")
        print("   You can run this script again anytime")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)