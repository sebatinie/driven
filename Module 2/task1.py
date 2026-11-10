import pickle

obj = {"name": "Jenny", "age": 25}

# Pickling
pickle.dump(obj, open("data.pkl", "wb"))
# Unpickling
loaded = pickle.load(open("data.pkl", "rb"))
#print(loaded)

pickle.dump(obj, file) # write pickled object to file
pickle.dumps(obj) # return pickled object as bytes
with open('data.pkl', 'rb') as file:
    data = pickle.load(file)
print(data)
# read pickled object from file
pickle.loads(bytes) 