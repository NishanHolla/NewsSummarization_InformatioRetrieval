import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

class Summarizer:
    def __init__(self):
        self.tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
        self.model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

    def summarize_with_tfidf(self, text, per):
        nlp = spacy.load('en_core_web_sm')

        # Split text into sentences
        sentences = sent_tokenize(text)

        # Tokenize and preprocess text
        processed_sentences = []
        for sent in sentences:
            doc = nlp(sent)
            tokens = [token.text.lower() for token in doc if token.text.lower() not in STOP_WORDS and token.text.lower() not in punctuation]
            processed_text = ' '.join(tokens)
            processed_sentences.append(processed_text)
            
        # Join processed sentences into a single string
        processed_text = ' '.join(processed_sentences)
        
        # Calculate TF-IDF scores for each word
        tfidf_vectorizer = TfidfVectorizer()
        
        tfidf_matrix = tfidf_vectorizer.fit_transform([processed_text])

        feature_names = tfidf_vectorizer.get_feature_names_out()

        word_scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))

        # Calculate sentence scores based on TF-IDF of words in each sentence
        sentence_scores = {}
        for sent in sentences:
            doc = nlp(sent)
            sent_tokens = [token.text.lower() for token in doc if token.text.lower() in word_scores]
            if sent_tokens:
                sentence_scores[sent] = sum(word_scores[token] for token in sent_tokens)

        # Select top sentences for summary
        min_select_length = 1  # Set a minimum threshold for summary length
        select_length = max(min_select_length, int(len(sentences) * per))
        if select_length == 0:
            select_length = min_select_length
        summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
        final_summary = ' '.join(summary)
        
        return final_summary

    def summarize_with_pegasus(self, text, per):
        # Preprocess text (tokenization, truncation, padding)
        inputs = self.tokenizer([text], max_length=1024, return_tensors="pt", truncation=True, padding="max_length")

        # Generate summary using PEGASUS model
        summary_ids = self.model.generate(inputs["input_ids"], max_length=int(len(text) * per), num_beams=4, early_stopping=True)

        # Decode the summary
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary
