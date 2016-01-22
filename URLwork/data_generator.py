"""
data_generator.py

functions to create random (US) names and (UK) addresses for mock work
"""

import pymongo as mgo
from random import randint, seed, choice

def generateNames(size=100):
    '''
    generateNames creates a list of length size of random names from a database of popular first and last names

    :param size:  Number of names desired
    :return: list of names as (lastname, firstname, email) tuples
    '''

    host = "localhost"
    port = "27017"
    connection = "mongodb://{}:{}/".format(host, port)

    with mgo.MongoClient(connection) as client:
        db = client["customers"]
        fname = db['firstnames']
        sname = db['surnames']
        for i in range(size):
            seed()
            num = randint(1, fname.count())
            fn = fname.find_one({'number': num})["name"]
            seed()
            num = randint(1, sname.count())
            sn = sname.find_one({'number': num})["lastname"]

            # create email address
            email = createEmail(fn,sn)
            yield fn, sn, email

def createPhoneNumbers(town=''):
    seed()
    if town not in ['London', 'Greater London']:
        home = "01" + "{} {}".format(randint(200,999),randint(333333,999999))
    else:
        home = "020" + choice(['7','8']) + " {} {}".format(randint(100,999), randint(1000,9999))

    mobile = "07" + "{} {}".format(randint(850,970), randint(333333,999999))

    return home, mobile



def createEmail(firstname, lastname):
    emailSuffixes = ['hotmail', 'gmail', 'yahoo', 'btinternet', 'plusnet', 'excite']
    domains = ['com', 'co.uk']
    lastname = lastname.lower()
    if len(lastname) >= 8:
        lastname = lastname[:6] + "'"

    email = firstname[0].lower()
    seed()
    for ch in lastname:
        if ch != "'":
            email += ch
        else:
            email += str(randint(10, 99))
            break
    email += "@{}.{}".format(choice(emailSuffixes), choice(domains))
    return email

def generateStreetNameFromTown(collection):
    '''
    generateStreetNameFromTown works with any mongoDB collection with a 'town' field
    and produces a street name from single word towns only

    :param collection: mongoDB collection with 'town' field
    :return: suitable town name (based on filtering criteria)

    '''

    size = collection.count()
    seed()

    # filter out hyphenated and multi-word names
    while True:
        town = collection.find_one({"number": randint(1, size)})['town']
        if len(town.split('-')) > 1:
            continue
        elif len(town.split(' ')) > 1:
            continue
        else:
            return town

def generateAddresses(size=100):
    '''
    generateAddresses: Creates a list of mock UK address of length size

    a rudimentary weighting algorithm is used to generated apartment numbers and street names

    :param size: desired number of addresses to create
    :return: a list of size mock UK addresses
    '''

    streetSuffix = ['Rd', 'St', 'Mews', 'Rise', 'Hill', 'Close', 'Crescent', 'Ave', 'Ln', 'Row', 'Court']
    flatSuffix = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g']
    streetNouns = []
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Nouns commonly associated with UK street names are contained in the file 'streetNouns.txt'
    with open('streetNouns.txt', 'r') as fd:
        for line in fd:
            line = line.strip().capitalize()
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
            # provides a 15% chance of an apartment in the listing
            houseNumber = str(randint(1, 200)) + (flatsfx['high'] if randint(1, 100) < 85 else flatsfx['low'])
            seed()
            # provides a 50% chance of street name beginning with a UK town name, otherwise picks
            # a name from the common street noun list
            street = "{} {}".format(choice(streetNouns) if randint(1, 100) < 50 else
                                    generateStreetNameFromTown(towns),
                                    choice(streetSuffix))
            # randomly select a town from the database
            seed()
            number = randint(1, towns.count())
            townCounty = towns.find_one({'number': number})
            town = townCounty['town']
            county = townCounty['county']
            seed()
            # generate the fake postcode
            postcode = "{}{} {}{}".format(town[:2].upper(), str(randint(1, 20)), str(randint(1, 9)), choice(alphabet) + choice(alphabet))
            home, mobile = createPhoneNumbers(town)
            yield houseNumber, street, town, county, postcode, home, mobile

if __name__ == '__main__':
    # We'll create a clientdetails database and populate is with documents with the following schema
    # Firstname, Lastname, Address(House, Street,Town,County,Postcode),Email, Phone(Home, Mobile)

    # Generate a population of names and addresses
    population = 200
    names = generateNames(population)
    details = generateAddresses(population)

    hostname = 'localhost'
    port = '27017'
    connection = "mongodb://{}:{}/".format(hostname, port)

    print("connecting to {}...".format(connection))

    with mgo.MongoClient(connection) as dbclient:
        db = dbclient['client_details']
        print("dropping existing collection...")

        db.drop_collection('contact_info')

        print("Adding new contact details to database...")
        for i in range(population):
            firstname, lastname, email = next(names)
            houseNumber, street, town, county, postcode, home, mobile = next(details)
            db['contact_info'].insert({"firstname":firstname,
                                       "lastname": lastname,
                                       "address": {
                                           "houseNumber": houseNumber,
                                           "street": street,
                                           "town": town,
                                           "county": county,
                                           "postcode": postcode},
                                       "email": email,
                                       "tel": {
                                           "home": home,
                                           "mobile": mobile
                                       }})

