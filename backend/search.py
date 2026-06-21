import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class FAQSearch:

    def __init__(self, faq_file="faq.json"):

        # FAQ DATASET
        with open(faq_file, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

        # GREETINGS
        with open("greetings.json", "r", encoding="utf-8") as f:
            self.greetings = json.load(f)

        # GREETING RESPONSES
        with open("greeting_responses.json", "r", encoding="utf-8") as f:
            self.responses = json.load(f)

        self.search_texts = []

        for faq in self.faqs:

            text = faq["question"]

            text += " " + " ".join(
                faq.get("keywords", [])
            )

            text += " " + " ".join(
                faq.get("variations", [])
            )

            self.search_texts.append(text)

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.search_texts
        )

    def search(self, user_query):

        query = user_query.lower().strip()

        # GREETINGS

        if query in self.greetings["greetings"]:
            return {
                "answer": self.responses["greeting"],
                "confidence": 1.0,
                "matched_question": "Greeting"
            }

        # THANKS

        if query in self.greetings["thanks"]:
            return {
                "answer": self.responses["thanks"],
                "confidence": 1.0,
                "matched_question": "Thanks"
            }

        # GOODBYE

        if query in self.greetings["goodbye"]:
            return {
                "answer": self.responses["goodbye"],
                "confidence": 1.0,
                "matched_question": "Goodbye"
            }

        # TF-IDF SEARCH

        query_vector = self.vectorizer.transform(
            [user_query]
        )

        scores = cosine_similarity(
            query_vector,
            self.tfidf_matrix
        )[0]

        best_index = scores.argmax()

        confidence = scores[best_index]

        # FALLBACK

        if confidence < 0.15:

            fallback = next(
                faq
                for faq in self.faqs
                if faq["id"] == "GEN001"
            )

            return {
                "answer": fallback["answer"],
                "confidence": float(confidence),
                "matched_question": "Fallback"
            }

        faq = self.faqs[best_index]

        return {
            "answer": faq["answer"],
            "confidence": float(confidence),
            "matched_question": faq["question"],
            "category": faq["category"]
        }


search_engine = FAQSearch()