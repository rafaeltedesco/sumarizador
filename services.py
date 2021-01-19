import PyPDF2
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
import re
from collections import defaultdict
from heapq import nlargest


nltk.download('stopwords')
nltk.download('punkt')
stops = stopwords.words('portuguese')
punctuation = list(punctuation)

stops.extend(punctuation)


PATTERN = r"""\w+\-+\w+|\w+['"]{1}"""

def meu_tokenizer(input_string):
  return re.findall(PATTERN, input_string)

def process_file(filename):
  if (filename.split('.')[1] == 'pdf'):
    file = open(filename, 'rb')

    fileReader = PyPDF2.PdfFileReader(file)
    text = []
    for i in range(fileReader.numPages):
      text.append(fileReader.getPage(i).extractText())
    
    resumo = summarize(text)

    return resumo

  elif (filename.split('.')[1] in ['txt', 'doc', 'docx']):
    with open(filename, 'rb') as f:
      text = f.readlines()
    
    resumo = summarize(text)

    return resumo

  else:
    print('Arquivo não é pdf, txt ou doc')

def summarize(text):
  text = ' '.join(text).strip().replace('\n','')
  sents = sent_tokenize(text)
  words = word_tokenize(text)
  words = list(filter(lambda word: word.lower() not in stops, words))

  freq = FreqDist(words)
  sentencas_importantes = defaultdict(int)

  for i, sentenca in enumerate(sents):
    for palavra in word_tokenize(sentenca.lower()):
      if palavra in freq:
        sentencas_importantes[i] += freq[palavra]

  return (sentencas_importantes, sents)



def summary(filename, n_paragraphs):
  data = process_file(filename)
  idx_sentencas_importantes = nlargest(int(n_paragraphs), data[0], data[0].get)
  
  resumo = []
  for i in sorted(idx_sentencas_importantes):
    resumo.append(data[1][i])

  resumo = ' '.join(resumo)
  return resumo
