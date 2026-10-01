# 04_Prototype — Banking Intent Classifier (Proof of Concept)

A small, working prototype that takes a customer message and returns an
intent, a confidence score, and a recommended action for a support agent —
matching the flow described in `03_Solution_Design.docx`.

```
Input:  "My card hasn't arrived yet."
Output: {
  "intent": "card_arrival",
  "confidence": 0.67,
  "recommended_action": "Check card delivery status",
  "needs_review": false,
  "top_matches": [ ... top 3 candidate intents ... ]
}
```

## How to run it

```bash
cd source_code
pip install -r ../requirements.txt

python demo.py                              # runs 5 built-in sample messages
python demo.py "My card hasn't arrived"     # classify your own message
python demo.py --interactive                # type messages one at a time
```

No internet connection or GPU is needed — it trains itself from the bundled
CSV files in a few tenths of a second every time it starts.

## What I attempted, what worked, and what didn't

What I attempted first:the design in `03_Solution_Design.docx` calls for
an *embedding-based* classifier (neural sentence embeddings, e.g. Sentence-BERT
via the `sentence-transformers` library), compared using cosine similarity.
That was my first choice for the prototype.

Where I got blocked: `sentence-transformers` needs to download a
pretrained model (a few hundred MB) from `huggingface.co` the first time it
runs. My development sandbox's network only allows a specific list of
domains (`pypi.org`, `github.com`, etc.) and **does not** allow
`huggingface.co`, so the model download fails there. This is a sandbox
limitation, not a limitation of the approach itself.

What worked instead:I built the same architecture using **TF-IDF
vectors + cosine similarity + weighted k-nearest-neighbour voting**
(scikit-learn, from `classifier.py`) instead of neural embeddings. TF-IDF
turns each message into numbers based on word importance rather than deep
"meaning," so it's a simpler stand-in for the same idea: *turn text into
vectors, then compare vectors to find the closest known intents.* It needs
zero internet access after installation, which made it possible to fully
build, test, and evaluate here.

What I would do next(if running somewhere with normal internet access,
like a personal laptop or a cloud VM):
1. Install `sentence-transformers` and swap `TfidfVectorizer` in
   `classifier.py` for `SentenceTransformer('all-MiniLM-L6-v2')` — the rest
   of the pipeline (cosine similarity, weighted voting, confidence score)
   stays the same, since it was designed to compare *any* kind of vectors.
2. Compare accuracy between the TF-IDF version and the embedding version on
   the same test set (see results below) to see how much embeddings help.
3. Fine-tune the embedding model on the BANKING77 training data itself for a
   further accuracy boost, as suggested in the original BANKING77 paper.

## How the working prototype performs

Evaluated on the full official BANKING77 test set (3,080 messages, 77
intents), which the model never saw during training:

| Metric                                                          | Result    |

| Top-1 accuracy (exact intent correct)                           | **74.4%** |
| Top-3 accuracy (correct intent in top 3 candidates)             | **90.6%** |
| "Needs review" rate (confidence below threshold)                | 25.9%     |
| Average time per message                                        | ~2 ms     |

This lines up with what we predicted in `01_Dataset_Analysis.docx`: the
model does well overall, but a meaningful share of mistakes happen between
intents that look similar in wording (e.g. `pending_transfer` vs.
`transfer_not_received_by_recipient`) — exactly why `03_Solution_Design.docx`
adds a confidence check and a human agent, rather than trusting the AI
blindly.

## Files in this folder

```
04_Prototype/
├── README.md                    <- this file
├── requirements.txt
├── sample_inputs_outputs.json   <- 7 example inputs and their real outputs
└── source_code/
    ├── classifier.py            <- the core intent classifier
    ├── intent_actions.py        <- intent -> recommended action lookup table
    ├── demo.py                  <- command-line demo script (run this)
    └── data/
        ├── train.csv            <- BANKING77 training data (10,003 examples)
        └── test.csv             <- BANKING77 test data (3,080 examples)
```

## Data source

BANKING77 dataset, from the PolyAI research team:
https://huggingface.co/datasets/PolyAI/banking77
(CSV files obtained from the official PolyAI GitHub repository:
https://github.com/PolyAI-LDN/task-specific-datasets)
