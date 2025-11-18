from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-en-hi"

print("Downloading model… please wait (100–500 MB)...")

# This downloads tokenizer + model and stores inside ~/.cache
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Save locally
save_path = "D:/MSC AI/audio_translator_nlp/models/opus-mt-en-hi"
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)

print("Model downloaded and saved successfully at:", save_path)
