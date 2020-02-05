from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import json

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

def check_similarity(db,inpt): #inp are sets
    return len(db.intersection(inpt))/len(inpt)

def join_sen(l):
    return ' '.join(l)

with open("intents.json", "rb") as f:
    datasets = json.load(f)
with open("sentence_intents.json","rb") as g:
    data_sen = json.load(g)

inp = input("Enter what you want to search :- ")
inp_list = primary_clean(inp)

final_inp_set = stop_and_stem(inp_list)

sen_str = join_sen(inp_list)

temp_dict = {}
for i in range(len(datasets['intents'])):
    datasets['intents'][i]['patterns'] = set(datasets['intents'][i]['patterns'])
    semantic_acc = check_similarity(datasets['intents'][i]['patterns'],final_inp_set)
    temp_list = datasets['intents'][i]['responses'][0].split()
    temp_list.append(semantic_acc)
    
    
    if(sen_str in data_sen['intents'][i]['patterns']):
        temp_list.append("Yes")
    else:
        temp_list.append("No")


    temp_dict[i] = temp_list
print(temp_dict)
    

