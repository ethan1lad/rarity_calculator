import csv

with open('../data/background.csv', mode='r') as FILE:
    reader = csv.reader(FILE)
    background = {rows[0]:rows[1] for rows in reader}
with open('../data/body.csv', mode='r') as FILE:
    reader = csv.reader(FILE)
    body = {rows[0]:rows[1] for rows in reader}
with open('../data/ears.csv', mode='r') as FILE:
    reader = csv.reader(FILE)
    ears = {rows[0]:rows[1] for rows in reader}
with open('../data/expression.csv', mode='r') as FILE:
    reader = csv.reader(FILE)
    expression = {rows[0]:rows[1] for rows in reader}
with open('../data/eyes.csv', mode='r') as FILE:
    reader = csv.reader(FILE)
    eyes = {rows[0]:rows[1] for rows in reader}
with open('../data/facecolor.csv', mode='r') as FILE:
    reader = csv.reader(FILE)
    facecolor = {rows[0]:rows[1] for rows in reader}
with open('../data/head.csv', mode='r') as FILE:
    reader = csv.reader(FILE)
    heads = {rows[0]:rows[1] for rows in reader}
with open('../data/nose.csv', mode='r') as FILE:
    reader = csv.reader(FILE)
    nose = {rows[0]:rows[1] for rows in reader}

initial_object = {
    'gnomekins': [],
    'background': background,
    'eyes': eyes,
    'body':body,
    'ears': ears,
    'expression':expression,
    'facecolor':facecolor,
    'head':heads,
    'nose':nose}

print(initial_object)
class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store


global data_store
data_store = Datastore()

