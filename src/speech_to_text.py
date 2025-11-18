import json
import sys
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

def recognize_speech(vosk_path="models/vosk_model"):
    print("\n🎤 Speak something in English...")

    model = Model(vosk_path)
    recognizer = KaldiRecognizer(model, 16000)

    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):
        audio_queue.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):

        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                return text
