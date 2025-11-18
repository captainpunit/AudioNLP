import spacy

class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def process(self, text):
        doc = self.nlp(text)

        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        return {
            "original_text": text,
            "keywords": keywords,
            "entities": entities
        }
