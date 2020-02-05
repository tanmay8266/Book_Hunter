from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import wordnet
import os
from bs4 import BeautifulSoup
import requests
import pickle

try:
    with open("data.pickle","rb") as f:
        dataset = pickle.load(f)
except:
    dataset = {'b1':{}}

    def primary_clean(given_title):
        given_list = word_tokenize(given_title)
        new_list= []
        for i in given_list:
            i = i.lower()
            if(i.isalnum()):
                new_list.append(i)
        return new_list 

    def stop_and_stem(given_list):
        new_list = []
        for w in given_list:
            if(w not in stop_words):
                w = ps.stem(w)
                new_list.append(w)
        return new_list

    def check_similarity(list1,list2):
        set1 = set(list1)
        set2 = set(list2)
        return len(set1.intersection(set2)) / len(set2)

    def get_synonyms(inp_list):
        inp_list = list(set(inp_list))
        synonyms = set([])
        for i in inp_list:
            print(i)
            # synonyms.union(synonyms_of_word(i))
            tem_set = set([])
            synonym_set = synonyms_of_word(i)
            for j in synonym_set:
                if j not in stop_words:
                    tem_set.add(ps.stem(j))
            synonyms.union(synonyms_of_word(i))
        final_set = set(inp_list)
        return final_set.union(synonyms)

    def synonyms_of_word(word):
        str_init = "https://www.thesaurus.com/browse/"
        final_req = str_init + word
        page = requests.get(final_req)
        if(page.status_code == 200):
            soup = BeautifulSoup(page.content,'html.parser')
            hot_soup = soup.find_all('a',class_='css-gkae64 etbu2a31')
            synonyms = []
            for i in range(min(5,len(hot_soup))):
                synonyms.append(hot_soup[i].get_text())
            return set(synonyms)
        else:
            return set([])

    # string1 = input("Enter the Sentence : ")
    a = int(input("From Page: "))
    b = int(input("To Page:"))
    big_stuff = ""
    for i in range(a,b+1):
        command = "pdf2txt.py -p "+str(i)+" ~/b1.pdf > temp.txt"
        print(command)
        os.system(command)
        content = open("temp.txt",'r')
        content = content.read()
        cleaned_content = primary_clean(content)
        final_content = stop_and_stem(cleaned_content)
        page_dataset = get_synonyms(final_content)
        dataset['b1'][i] = page_dataset
    print(dataset)

    with open("data.pickle","wb") as f:
        pickle.dump(dataset,f)
    #     big_stuff+=str(i)+","
    # print(big_stuff[:len(big_stuff)-1])
    # command = "pdf2txt.py -p "+big_stuff[:len(big_stuff)-1]+" ~/b1.pdf"





