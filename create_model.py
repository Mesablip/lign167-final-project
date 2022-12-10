import spacy
import pandas as pd
from tqdm import tqdm
from spacy.tokens import DocBin
from sklearn.model_selection import train_test_split

#Code adapted from https://www.machinelearningplus.com/nlp/custom-text-classification-spacy/
clickbait = pd.read_csv("shuffled_data.csv")
nlp = spacy.load("en_core_web_lg")

def make_docs(data):
    docs = []
    for doc, label in tqdm(nlp.pipe(data, as_tuples=True), total = len(data)):
        if label == 1:
            doc.cats["clickbait"] = 1
            doc.cats["not_clickbait"] = 0
        else:
            doc.cats["clickbait"] = 0
            doc.cats["not_clickbait"] = 1
        docs.append(doc)
    return docs

train_docs = make_docs(list(clickbait[:15000].itertuples(index=False, name=None)))
doc_bin = DocBin(docs=train_docs)
doc_bin.to_disk("./data/train.spacy")

valid_docs = make_docs(list(clickbait[15000:].itertuples(index=False, name=None)))
doc_bin = DocBin(docs=valid_docs)
doc_bin.to_disk("./data/valid.spacy")



