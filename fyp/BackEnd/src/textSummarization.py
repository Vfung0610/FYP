#The following code is refering to this online tutorial: https://betterprogramming.pub/extractive-text-summarization-using-spacy-in-python-88ab96d1fd97
#Ng Wai Foong (2020, Jan 30). "Extractive Text Summarization Using spaCy in Python". Available: https://betterprogramming.pub/extractive-text-summarization-using-spacy-in-python-88ab96d1fd97 [Accessed: Jan 30, 2021]

import spacy
from collections import Counter
from string import punctuation

def textSummarize(text):
    print("TextSummarize Start")
    textLoader = spacy.load("en_core_web_lg")
    keyword = []
    VALID_TAG = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    doc = textLoader(text.lower())
    for token in doc:
        if(token.text in textLoader.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in VALID_TAG):
            keyword.append(token.text)

    if not keyword:
        return "No summary found."

    freq_word = Counter(keyword)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for w in freq_word:
        freq_word[w] = (freq_word[w]/max_freq)
        
    sent_strength={}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]

    summary = []

    sorted_x = sorted(sent_strength.items(), key=lambda kv: kv[1], reverse=True)

    counter = 0
    limit = 2
    for i in range(len(sorted_x)):
        summary.append(str(sorted_x[i][0]).capitalize())

        counter += 1
        if(counter >= limit):
            break
            
    #print(' '.join(summary))
    print("TextSummarize End")
    return ' '.join(summary)