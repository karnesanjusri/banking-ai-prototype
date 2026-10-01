"""
classifier.py

A small, self-contained intent classifier for the Banking AI Case Study.

How it works (matches the "embedding-based similarity classifier" from
03_Solution_Design.docx, using TF-IDF vectors instead of neural embeddings --
see README.md, section "Approach & limitations", for why):

1. Load the BANKING77 training examples (data/train.csv).
2. Convert every training message into a TF-IDF vector (a vector of word
   importance scores). This is our stand-in for "embeddings".
3. When a new customer message comes in, convert it into the same kind of
   vector and compare it to every training vector using cosine similarity
   (a standard way to measure how close two vectors are in meaning/wording).
4. Look at the top-K most similar training examples ("nearest neighbours").
   Each one votes for its own intent, weighted by how similar it is.
5. The intent with the most weighted votes wins. The confidence score is
   that intent's share of the total vote among the top-K neighbours, so it
   is always between 0 and 1.
6. Look up a recommended action for the winning intent (intent_actions.py).

This whole approach needs no internet access and no GPU -- it trains in a
couple of seconds on a laptop, which fits the "simple proof of concept"
instruction in the assignment.
"""

from collections import defaultdict
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from intent_actions import get_recommended_action

DATA_DIR = Path(__file__).parent / "data"
DEFAULT_TRAIN_FILE = DATA_DIR / "train.csv"

# Below this confidence, we tell the caller we are not sure.
# (This mirrors the "Confidence Check" step in 03_Solution_Design.docx.)
LOW_CONFIDENCE_THRESHOLD = 0.45


class IntentClassifier:
    def __init__(self, train_file: Path = DEFAULT_TRAIN_FILE, top_k: int = 15):
        """
        train_file: path to a CSV with columns 'text' and 'category'
        top_k: how many nearest training examples to vote on
        """
        self.top_k = top_k

        df = pd.read_csv(train_file)
        self.texts = df["text"].tolist()
        self.labels = df["category"].tolist()

        # min_df=1 keeps rare-but-useful words; ngram_range=(1,2) also looks
        # at word pairs (e.g. "card arrival") not just single words.
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
        )
        self.train_vectors = self.vectorizer.fit_transform(self.texts)

    def classify(self, message: str) -> dict:
        """
        Classify a single customer message.

        Returns a dict shaped like the assignment's example:
            {
              "intent": "card_arrival",
              "confidence": 0.92,
              "recommended_action": "Check card delivery status"
            }
        plus two extra, clearly-labelled fields ("needs_review" and
        "top_matches") that a real system would use for the Confidence
        Check / LLM Double-Check steps described in 03_Solution_Design.docx.
        """
        query_vector = self.vectorizer.transform([message])
        similarities = cosine_similarity(query_vector, self.train_vectors)[0]

        # Get the indices of the top-K most similar training examples.
        top_indices = similarities.argsort()[::-1][: self.top_k]

        # Weighted vote: each neighbour contributes its similarity score
        # to its own intent's total.
        votes = defaultdict(float)
        for idx in top_indices:
            votes[self.labels[idx]] += float(similarities[idx])

        total_vote = sum(votes.values()) or 1e-9
        best_intent = max(votes, key=votes.get)
        confidence = round(votes[best_intent] / total_vote, 2)

        # Small extra: show the runner-up intents, useful for an
        # LLM Double-Check step or for a human reviewing "Needs Review" cases.
        ranked = sorted(votes.items(), key=lambda kv: kv[1], reverse=True)
        top_matches = [
            {"intent": intent, "score": round(score / total_vote, 2)}
            for intent, score in ranked[:3]
        ]

        return {
            "intent": best_intent,
            "confidence": confidence,
            "recommended_action": get_recommended_action(best_intent),
            "needs_review": confidence < LOW_CONFIDENCE_THRESHOLD,
            "top_matches": top_matches,
        }


if __name__ == "__main__":
    # Quick manual smoke test: python classifier.py
    clf = IntentClassifier()
    for msg in [
        "My card hasn't arrived yet.",
        "I made a transfer yesterday but the money still hasn't reached the recipient.",
        "why was I charged for withdrawing cash",
    ]:
        print(msg, "->", clf.classify(msg))
