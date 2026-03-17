import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow UI to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load inverted index
with open("../data/inverted_index.json", "r") as f:
    inverted_index = json.load(f)

# Load IDF values
with open("../data/idf.json", "r") as f:
    idf = json.load(f)


# Query Processing
def tokenize_query(query):

    query = query.lower()

    query = re.sub(r'[^a-z0-9\s]', '', query)

    tokens = query.split()

    return tokens


# Search + TF-IDF ranking
def search_documents(tokens):

    scores = {}

    for word in tokens:

        if word in inverted_index:

            for doc, tf in inverted_index[word]:

                score = tf * idf[word]

                if doc not in scores:
                    scores[doc] = 0

                scores[doc] += score

    return scores


# Sort results
def rank_results(scores):

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return ranked[:10]


# Search endpoint
@app.get("/search")
def search(q: str):

    tokens = tokenize_query(q)

    scores = search_documents(tokens)

    results = rank_results(scores)

    return results