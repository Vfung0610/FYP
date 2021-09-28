from googlesearch import search, get_random_user_agent
from bs4 import BeautifulSoup
from textSummarization import textSummarize
import requests
from googleapiclient.discovery import build
import googleapiclient
import spacy

def searchQuery(searchObj): #destructe and execute search request
    #print(searchObj)
    searchArticleOnly = False
    #if searchObj["documentType"]["all"] == False and searchObj["documentType"]["article"]==True:
    #    print("SearchQuery searchArticle triggered")
    #    searchArticleOnly = True

    resultObj = {}
    for key, item in searchObj.items(): #search for each search domain keyword and its selected subDomain specific knowledge
        if key!="documentType":
            resultObj[key] = {}
            resultObj[key]["result"] = searchKeyword(key, True, searchArticleOnly) #execute search
            resultObj[key]["subDomain"] = []
            for subConcept, flag in item.items(): #saerch for each selected subDomain specific knowledge
                if flag:
                    tmpSubClassObj = {}
                    tmpSubClassObj["keyword"] = subConcept #build return result object
                    tmpSubClassObj["result"] = searchKeyword(subConcept, False, searchArticleOnly) #execute search
                    resultObj[key]["subDomain"].append(tmpSubClassObj) #build return result object

    return resultObj

def searchKeyword(keyword, domainKeyword=False, searchArticleOnly=False): #execute search and gather/build search result
    resultList = []
    if domainKeyword: #gather url for each keyword
        urlList = getSearchResult(keyword, 10)
    else:
        urlList = getSearchResult(keyword, 1)

    for urlID, urlObj in enumerate(urlList): #perform action on each url gathered
        soupResult = webScrapper(urlObj["link"])

        #if searchArticleOnly == True:
        #    print("searchKeyword searchArticle triggered")
        #    docType = soupResult.find("meta", property="og:type")
        #    if not docType:
        #        print("searchKeyword searchArticle triggered")
        #        continue
        #    elif docType["content"] != "article":
        #        print("searchKeyword searchArticle triggered")
        #        continue

        resultList.append({
            "id": urlID,
            "link": urlObj["link"],
            "title": urlObj["title"],
            "summary": textSummarize(textCombine(soupResult))
            #"summary": "Hello "+ urlObj["title"]
        })
        
    #print(resultList)
    return resultList

def getSearchResult(keyword, loopTime): #function to gather url for each keyword searched
    #Below are action to access the existing search engine
    try:
        apiKey = "" #API key removed for security reason, please insert new apikey from google search api
        service = build("customsearch", "v1", developerKey=apiKey)
        websiteList = []
        for i in range(loopTime):
            print("gathering url: " + str(i))
            result = service.cse().list(q=keyword, cx="9771b38c355104835", start=i*10, num=10).execute()
            for item in result["items"]:
                websiteListObj = {}
                websiteListObj["title"] = item["title"]
                websiteListObj["link"] = item["link"]
                websiteList.append(websiteListObj)

        return websiteList
    except googleapiclient.errors.HttpError:
        #Use another search api if google search api dont work
        print("Google quota used up")
        return list(search(keyword, tld="com", num=10*loopTime, start=0, stop=10*loopTime, pause=2))

def getOntologyBuildURL(keyword, num=100, stop=100): #function to gather url to build/extend ontology of missing keyword
    #Below are action to access the existing search engine
    try:
        apiKey = "" #API key removed for security reason, please insert new apikey from google search api
        service = build("customsearch", "v1", developerKey=apiKey)
        websiteList = []
        for i in range(10):
            print("gathering url: " + str(i))
            result = service.cse().list(q=keyword, cx="9771b38c355104835", start=i*10, num=10).execute()
            for item in result["items"]:
                websiteList.append(item["link"])
        return websiteList
    except googleapiclient.errors.HttpError:
        #Use another search api if google search api dont work
        print("Google quota used up")
        return list(search(keyword, tld="com", num=100, start=0, stop=100, pause=2))

def webScrapper(url): #function to scrap a website and return beautifulsoup source
    try:
        print("WebScrapper Start: " + str(url))
        print("webScrapper Result")
        result = requests.get(url, timeout=10, headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}) #get website source
        #print(result)
        resultText = result.text
        print("WebScrapper Beautiful Soup")
        soup = BeautifulSoup(resultText, 'html5lib')
        print("WebScrapper End")
        return soup
    except requests.exceptions.ReadTimeout:
        return BeautifulSoup("", 'html5lib')
    except Exception as e:
        print(e)
        return BeautifulSoup("", 'html5lib')

def textCombine(textSoup): #function to gather the needed text from a web document
    print("TextCombine Start")
    VALID_TAGS = ["html", "body", "article", "div", "h1", "h2", "h3", "h4", "h5", "h6", "p", "span", "li", "main", "ol", "section", "table", "tfoot", "ul", "b", "big", "code", "dfn", "em", "i", "kbd", "label", "q", "samp", "small", "strong", "sub", "sup", "var", "b", "em"]
    for tag in textSoup.find_all():
        if tag.name not in VALID_TAGS:
            tag.replaceWith(". ")

    returnSoup = textSoup.text
    returnSoup = " ".join(returnSoup.split())
    print("TextCombine End")
    return returnSoup

def trimSearchQuery(query): #function to extract keyword from a long search engine
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)
    tmpQuery = ""
    for token in doc:
        if token.is_stop == False:
            tmpQuery += token.text + " "

    doc = nlp(tmpQuery.strip())
    allQueryDetected = []
    for noun_chunk in doc.noun_chunks:
        allQueryDetected.append(noun_chunk)

    return allQueryDetected
