import os
import re
import json
import math
from bs4 import BeautifulSoup
from collections import Counter


# Task 1 – Load HTML Documents

PAGES_FOLDER = "pages"

html_files = [f for f in os.listdir(PAGES_FOLDER) if f.endswith(".html")]

total_documents = len(html_files)

print("Total HTML files found:", total_documents)


# Task 2 – Extract Visible Text

documents_text = {}

for file_name in html_files:

    file_path = os.path.join(PAGES_FOLDER, file_name)

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # remove script and style
    for tag in soup(["script", "style"]):
        tag.extract()

    text = soup.get_text()

    documents_text[file_name] = text


# Task 3 – Tokenization

tokens_per_doc = {}

for doc, text in documents_text.items():

    text = text.lower()

    text = re.sub(r'[^a-z0-9\s]', '', text)

    tokens = text.split()

    tokens_per_doc[doc] = tokens


# Task 4 – Compute Term Frequency

tf_per_doc = {}

for doc, tokens in tokens_per_doc.items():

    word_counts = Counter(tokens)

    tf_per_doc[doc] = word_counts


# Task 5 – Build Inverted Index

inverted_index = {}

for doc, word_counts in tf_per_doc.items():

    for word, freq in word_counts.items():

        if word not in inverted_index:
            inverted_index[word] = []

        inverted_index[word].append((doc, freq))


# Task 6 – Save Inverted Index to Disk

with open("inverted_index.json", "w", encoding="utf-8") as f:
    json.dump(inverted_index, f, indent=2)

print("Inverted index saved.")


# Task 7 – Compute IDF

idf = {}

for word, docs in inverted_index.items():

    df = len(docs)

    idf[word] = math.log(total_documents / df)


# Task 8 – Save IDF to Disk

with open("idf.json", "w", encoding="utf-8") as f:
    json.dump(idf, f, indent=2)

print("IDF values saved.")


# Task 9 – Validation

print("\nValidation Results")

print("Number of documents indexed:", total_documents)

print("Number of unique terms:", len(inverted_index))

print("\nSample index entries:")

for word in list(inverted_index.keys())[:5]:
    print(word, "->", inverted_index[word])

print("\nSample IDF values:")

for word in list(idf.keys())[:5]:
    print(word, "->", idf[word])
    