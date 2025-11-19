import json
import queue
import os

try:
    import sounddevice as sd
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("Warning: Vosk or sounddevice not available")

def recognize_speech(vosk_path="models/vosk_model", timeout=10):
    """
    Recognize speech using Vosk
    
    Args:
        vosk_path: Path to Vosk model
        timeout: Maximum recording time in seconds
        
    Returns:
        str: Recognized text or empty string
    """
    if not VOSK_AVAILABLE:
        print("Error: Speech recognition not available")
        return ""
    
    # Get absolute path for model
    if not os.path.isabs(vosk_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir) if 'src' in current_dir else current_dir
        vosk_path = os.path.join(project_root, vosk_path)
    
    if not os.path.exists(vosk_path):
        print(f"Error: Vosk model not found at {vosk_path}")
        print("Download a model from https://alphacephei.com/vosk/models")
        return ""
    
    try:
        print("\n🎤 Speak something in English...")
        print("   (The system will automatically detect when you stop speaking)")
        
        model = Model(vosk_path)
        recognizer = KaldiRecognizer(model, 16000)
        
        audio_queue = queue.Queue()
        recording = True
        silence_frames = 0
        max_silence_frames = 30  # Stop after ~2 seconds of silence
        
        def callback(indata, frames, time, status):
            if status:
                print(f"Status: {status}")
            audio_queue.put(bytes(indata))
        
        with sd.RawInputStream(
            samplerate=16000, 
            blocksize=8000, 
            dtype='int16',
            channels=1, 
            callback=callback
        ):
            print("   [Recording started...]")
            
            while recording:
                data = audio_queue.get()
                
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = json.loads(result).get("text", "")
                    
                    if text:
                        print(f"   ✓ Recognized: {text}")
                        return text
                    else:
                        silence_frames += 1
                else:
                    # Partial result - reset silence counter
                    partial = recognizer.PartialResult()
                    partial_text = json.loads(partial).get("partial", "")
                    if partial_text:
                        silence_frames = 0
                    else:
                        silence_frames += 1
                
                # Stop if too much silence
                if silence_frames > max_silence_frames:
                    final_result = recognizer.FinalResult()
                    text = json.loads(final_result).get("text", "")
                    if text:
                        print(f"   ✓ Final: {text}")
                        return text
                    else:
                        print("   ✗ No speech detected")
                        return ""
            
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return ""


def test_microphone():
    """Test if microphone is working"""
    try:
        import sounddevice as sd
        print("\n🎤 Testing microphone...")
        print("Available audio devices:")
        print(sd.query_devices())
        return True
    except Exception as e:
        print(f"Microphone test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the speech recognition
    test_microphone()
    text = recognize_speech()
    if text:
        print(f"\nYou said: {text}")
    else:
        print("\nNo speech recognized")