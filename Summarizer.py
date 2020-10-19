import bs4 as bs
import urllib.request
import re
import heapq
import nltk

def summarizer(url,n):
    web = urllib.request.urlopen(url)
    article = web.read()

    data = bs.BeautifulSoup(article, 'lxml')
    paragraphs = data.find_all('p')
    text = ""

    for p in paragraphs:
        text += p.text

    text = re.sub(r'\[[0-9]*\]',' ', text)
    text = re.sub(r'\s+',' ', text)
    formatted_text = re.sub('[^a-zA-Z]',' ',text)
    formatted_text= re.sub(r'\s+',' ', formatted_text)

    sentences = nltk.sent_tokenize(text)
    stopwords = nltk.corpus.stopwords.words('english')
    freq = {}
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopwords:
            if word not in freq.keys():
                freq[word] = 1
            else:
                freq[word] += 1

    max_freq = max(freq.values())

    for word in freq.keys():
        freq[word] = (freq[word] / max_freq)

    sentence_score = {}
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freq.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = freq[word]
                    else:
                        sentence_score[sent] += freq[word]

    summary_sentence = heapq.nlargest(n, sentence_score, key = sentence_score.get)
    summary = ' '.join(summary_sentence)
    print('Summary:\n'+summary)

print('\n\n\n\n\n\n\n-TEXT SUMMARIZER-')
print('Input the link website you want to summarize: ')
web = ""
web = input(web)
print('How many sentences: ')
n = ""
n = int(input(n))
summarizer(web,n)