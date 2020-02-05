import json
import pickle
data = pickle.load('data.pickle')
with open('app.json', 'w') as fp:
    json.dump(data, fp)