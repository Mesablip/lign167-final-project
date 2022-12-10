from urllib.request import urlopen
from bs4 import BeautifulSoup
import spacy
import en_core_web_lg

page = urlopen("https://www.cnn.com/2022/02/25/europe/ukraine-russia-snake-island-attack-intl-hnk-ml/index.html?utm_term=link&utm_content=2022-02-25T09%3A54%3A21&utm_source=twCNN&utm_medium=social")
soup = BeautifulSoup(page, "html.parser")
text = soup.find("div", attrs={"class": "article__content"}).get_text()
nlp = spacy.load('en_core_web_lg')
search_doc = nlp("A Ukrainian soldier on a tiny island in the Black Sea didn't hold back when threatened with bombing by a Russian warship as Moscow continued its assault on Ukrainian territory")
main_doc = nlp(text)
search_doc_no_stop_words = nlp(' '.join([str(t) for t in search_doc if not t.is_stop]))
main_doc_no_stop_words = nlp(' '.join([str(t) for t in main_doc if not t.is_stop]))

print(search_doc_no_stop_words.similarity(main_doc_no_stop_words))
