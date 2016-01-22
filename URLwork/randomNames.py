import pymongo as mgo
from random import randint, seed, choice

def generateNames(size=100):
    host = "localhost"
    port = "27017"
    connection = "mongodb://{}:{}/".format(host, port)

    with mgo.MongoClient(connection) as client:
        db = client["customers"]
        fname = db['firstnames']
        sname = db['surnames']

        names = []
        for i in range(size):
            seed()
            num = randint(1, fname.count())
            fn = fname.find_one({'number': num})["name"]
            seed()
            num = randint(1, sname.count())
            sn = sname.find_one({'number': num})["lastname"]
            names.append((sn, fn))

        return names

def generateAddresses(size=100):
    streetSuffix = ['Rd', 'St', 'Mews', 'Rise', 'Hill', 'Close', 'Crescent', 'Ave', 'Ln', 'Row', 'Court']
    flatSuffix = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g']
    streetNouns = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'.upper()
    with open('streetNouns.txt','r') as fd:
        for line in fd:
            line = line.strip()
            line = line.capitalize()
            streetNouns.append(line)

    host = "localhost"
    port = "27017"
    connection = "mongodb://{}:{}/".format(host, port)

    with mgo.MongoClient(connection) as client:
        db = client["customers"]
        towns = db['towns']

        for i in range(size):
            flatsfx = {'high': flatSuffix[0], 'low': str(choice(flatSuffix[1:]))}
            seed()
            houseNumber = str(randint(1, 200)) + (flatsfx['high'] if randint(1, 100) < 98 else flatsfx['low'])
            street = "{} {}".format(choice(streetNouns), choice(streetSuffix))

            number = randint(1, towns.count())
            townCounty = towns.find_one({'number': number})
            town = townCounty['town']
            county = townCounty['county']
            seed()
            postcode = "{}{} {}{}".format(town[:2].upper(), str(randint(1, 20)), str(randint(1, 9)), choice(alphabet) + choice(alphabet))

            print("{},{},{},{},{}".format(houseNumber, street, town, county, postcode))