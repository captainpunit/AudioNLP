from transformers import MarianMTModel, MarianTokenizer

model_path = "D:/MSC AI/audio_translator_nlp/models/opus-mt-en-hi"   # LOCAL MODEL

tokenizer = MarianTokenizer.from_pretrained(model_path)
model = MarianMTModel.from_pretrained(model_path)

def translate_to_hindi(text):
    batch = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
    generated = model.generate(**batch)
    hindi_text = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
    return hindi_text
