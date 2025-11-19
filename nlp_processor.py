try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("Warning: spaCy not installed. NLP features will be limited.")

import re
from collections import Counter

class NLPProcessor:
    def __init__(self):
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("SpaCy model 'en_core_web_sm' not found.")
                print("Install it using: python -m spacy download en_core_web_sm")

    def process(self, text):
        """Process text and extract linguistic features"""
        if not text or text.strip() == "":
            return {
                "original_text": "",
                "keywords": [],
                "entities": [],
                "pos_tags": [],
                "word_count": 0,
                "sentence_count": 0
            }

        result = {
            "original_text": text,
            "keywords": [],
            "entities": [],
            "pos_tags": [],
            "word_count": len(text.split()),
            "sentence_count": len(re.split(r'[.!?]+', text))
        }

        if self.nlp:
            doc = self.nlp(text)
            
            # Extract keywords (non-stop words, alphabetic tokens)
            result["keywords"] = [
                token.text for token in doc 
                if token.is_alpha and not token.is_stop and len(token.text) > 2
            ]
            
            # Extract named entities
            result["entities"] = [
                {"text": ent.text, "label": ent.label_} 
                for ent in doc.ents
            ]
            
            # Extract POS tags
            result["pos_tags"] = [
                {"text": token.text, "pos": token.pos_} 
                for token in doc if token.is_alpha
            ]
        else:
            # Fallback: simple keyword extraction
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            # Simple stopwords
            stopwords = {'the', 'is', 'are', 'was', 'were', 'and', 'or', 'but', 
                        'in', 'on', 'at', 'to', 'for', 'of', 'with', 'a', 'an'}
            result["keywords"] = [w for w in words if w not in stopwords]

        return result

    def get_summary(self, text):
        """Get a summary of the text analysis"""
        analysis = self.process(text)
        
        summary = f"""
Text Analysis:
--------------
Words: {analysis['word_count']}
Sentences: {analysis['sentence_count']}
Keywords: {', '.join(analysis['keywords'][:10])}
"""
        
        if analysis['entities']:
            entities_str = ', '.join([f"{e['text']} ({e['label']})" 
                                     for e in analysis['entities'][:5]])
            summary += f"Entities: {entities_str}\n"
        
        return summary