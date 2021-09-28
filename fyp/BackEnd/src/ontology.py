from searcher import getOntologyBuildURL, webScrapper, textCombine
import spacy
import re, json, os
from owlready2 import *

def findChild(keyword): #function to get all sub-domain specific knowledge of the searched keyword
    dirname = os.path.dirname(__file__)
    onto = get_ontology("file://"+ dirname +"/ontology/allConcept.owl").load()

    subClassList = []
    print(onto[keyword])
    if onto[keyword] != None:
        for item in list(onto[keyword].subclasses()):
            subClassList.append(str(item).rsplit(".")[-1])

    if len(subClassList) == 0: #build/extend ontology if no sub-domain specific knowledge found
        print(str(keyword))
        result = buildOntology(str(keyword))
        if result == "Ontology Built":
            for item in list(onto[keyword].subclasses()):
                subClassList.append(str(item).rsplit(".")[-1])

    print(subClassList)
    return subClassList


def buildOntology(keyword): #function to build/extend ontology tree
    try:
        print("startBuildOntology: " + keyword)
        nlp = spacy.load("en_core_web_sm")
        allPossibeKeyword = {}
        allPossibeKeyword_NounChunk = {}

        websiteList = getOntologyBuildURL(keyword)
        print("URL Gathered:" + str(len(websiteList)))

        for count, url in enumerate(websiteList): #find potential keyword in each website and calculate the occurence of them in each web document
            print("Scrapping " + str(count) + "|" + url)
            soup = webScrapper(url)
            if soup == "TimeOut":
                continue
            removeSymbolText = re.sub("[^A-z,.']|[\[\]^]", " ", textCombine(soup).lower())
            processedText = ' '.join(removeSymbolText.split())
            doc = nlp(processedText)

            tmpNounPharse = ""
            allKeywordInThisDoc = {}

            lemmizedText = ""
            for token in doc: #count token occurence in single doc (n-gram)
                if token.is_stop == True:
                    lemmizedText += ";"
                else:
                    lemmizedText += " " + token.lemma_

                if token.pos_ in ["ADJ", "NOUN", "PROPN"] and (re.search("[^A-z]", token.text) is None):
                    tmpNounPharse += " " + token.lemma_
                    if len(tmpNounPharse.split()) > 1:
                        if token.lemma_ in allKeywordInThisDoc:
                            allKeywordInThisDoc[token.lemma_] += 1
                        else:
                            allKeywordInThisDoc[token.lemma_] = 1
                    
                    if tmpNounPharse.strip() in allKeywordInThisDoc:
                            allKeywordInThisDoc[tmpNounPharse.strip()] += 1
                    else:
                        allKeywordInThisDoc[tmpNounPharse.strip()] = 1
                else:
                    tmpNounPharse = ""

            for key, value in allKeywordInThisDoc.items(): #count token occurence in all docs (n-gram)
                if key in allPossibeKeyword:
                    allPossibeKeyword[key]["tf"] += value
                    allPossibeKeyword[key]["idf"] += 1
                else:
                    allPossibeKeyword[key] = {}
                    allPossibeKeyword[key]["tf"] = value
                    allPossibeKeyword[key]["idf"] = 1

            allKeywordInThisDoc_NounChunk = {}
            doc = nlp(lemmizedText)
            for chunk in doc.noun_chunks: # other method to extract keyword (spacy's noun chunk)
                if chunk.text in allKeywordInThisDoc_NounChunk:
                    allKeywordInThisDoc_NounChunk[chunk.text] = allKeywordInThisDoc_NounChunk[chunk.text] + 1
                else:
                    allKeywordInThisDoc_NounChunk[chunk.text] = 1

            for key, value in allKeywordInThisDoc_NounChunk.items():# other method to extract keyword (spacy's noun chunk)
                if key in allPossibeKeyword_NounChunk:
                    allPossibeKeyword_NounChunk[key]["tf"] += value
                    allPossibeKeyword_NounChunk[key]["idf"] += 1
                else:
                    allPossibeKeyword_NounChunk[key] = {}
                    allPossibeKeyword_NounChunk[key]["tf"] = value
                    allPossibeKeyword_NounChunk[key]["idf"] = 1

        dirname = os.path.dirname(__file__)
        filepathName = os.path.join(dirname, "ontology/ref/")
        with open(filepathName+keyword+"_NGram.json", "w") as f:
            json.dump(allPossibeKeyword, f, indent=4, sort_keys=True)

        with open(filepathName+keyword+"_NounChunk.json", "w") as f:
            json.dump(allPossibeKeyword_NounChunk, f, indent=4, sort_keys=True)

        onto = get_ontology("file://"+ dirname +"/ontology/allConcept.owl").load()

        with onto: #add to exisiting ontology tree
            if onto[keyword] == None:
                print("triggered")
                types.new_class(keyword,(Thing,))

            for key in allPossibeKeyword:
                if allPossibeKeyword[key]["idf"] >= 20:
                    print(key)
                    doc = nlp(key)
                    if doc[len(doc)-1].pos_ in ["NOUN", "PROPN"]:
                        if onto[key] != None:
                            pass
                        else:
                            types.new_class(key,(onto[keyword],))

        onto.save()

        return "Ontology Built"
    except Exception as e:
        print("Error Occur at ontology.py(buildOntology). Error Message: " + str(e))
        return "Error Occur at ontology.py(buildOntology). Error Message: " + str(e)