from transformers import MarianMTModel, MarianTokenizer
import os

# Get the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) if 'src' in current_dir else current_dir

# Use relative path to avoid space issues
model_path = os.path.join(project_root, "models", "opus-mt-en-hi")

# Initialize model and tokenizer
try:
    if os.path.exists(model_path):
        print(f"Loading model from: {model_path}")
        tokenizer = MarianTokenizer.from_pretrained(model_path, local_files_only=True)
        model = MarianMTModel.from_pretrained(model_path, local_files_only=True)
    else:
        print("Local model not found, loading from HuggingFace...")
        model_name = "Helsinki-NLP/opus-mt-en-hi"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
except Exception as e:
    print(f"Error loading model: {e}")
    print("Falling back to HuggingFace...")
    model_name = "Helsinki-NLP/opus-mt-en-hi"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

def translate_to_hindi(text):
    """Translate English text to Hindi"""
    if not text or text.strip() == "":
        return ""
    
    try:
        batch = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
        generated = model.generate(**batch)
        hindi_text = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
        return hindi_text
    except Exception as e:
        return f"Translation error: {str(e)}"