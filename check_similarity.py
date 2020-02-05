from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import pickle

def primary_clean(inp):
    given_list = word_tokenize(inp)
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
    return set(new_list)

def check_similarity(db,inpt):
    return len(db.intersection(inpt))/len(inpt)

with open("data.pickle", "rb") as f:
    datasets = pickle.load(f)

inp = input("Enter what you want to search :- ")
inp_list = primary_clean(inp)
final_inp_set = stop_and_stem(inp_list)
for i in datasets['b1']:
    print(i)
    print(check_similarity(datasets['b1'][i],final_inp_set))



