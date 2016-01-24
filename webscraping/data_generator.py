"""
data_generator.py
functions to create random (US) names and (UK) addresses for mock contact lists of any size
"""

import pymongo as mgo
from random import randint, seed, choice


def generate_names(size=100):
    """
    generate_names creates a list of length size of random names from a database of popular first and last names
    :param size:  Number of names desired, int
    :return: list of (last_name, first_name, email) tuples of string
    """

    host = "localhost"
    port = "27017"
    connection = "mongodb://{}:{}/".format(host, port)

    with mgo.MongoClient(connection) as client:
        db = client["random_names"]
        fname = db['first_names']
        sname = db['surnames']
        for i in range(size):
            seed()
            num = randint(1, fname.count())
            fn = fname.find_one({'number': num})["name"]
            seed()
            num = randint(1, sname.count())
            sn = sname.find_one({'number': num})["last_name"]

            # create email address
            email = create_email(fn,sn)
            yield fn, sn, email


def create_phone_numbers(town=''):
    """ create_phone_numbers: generates a mock UK style phone number
    :param town: for upgrade - may involve real area codes, string
    :return: home and mobile number as 2-tuple of string
    """

    seed()
    if town not in ['London', 'Greater London']:
        home = "01" + "{} {}".format(randint(200, 999),randint(333333, 999999))
    else:
        home = "020" + choice(['7', '8']) + " {} {}".format(randint(100, 999), randint(1000, 9999))

    mobile = "07" + "{} {}".format(randint(850, 970), randint(333333, 999999))

    return home, mobile


def create_email(first_name, last_name):
    """ create_email: generates a mock email address given the user's first and last names
    :param first_name: user's first name, string
    :param last_name: user's last name, string
    :return: email address, string
    """
    email_suffixes = ['hotmail', 'gmail', 'yahoo', 'btinternet', 'plusnet', 'excite']
    domains = ['com', 'co.uk']
    last_name = last_name.lower()
    if len(last_name) >= 8:
        last_name = last_name[:6] + "'"

    email = first_name[0].lower()
    seed()
    for ch in last_name:
        if ch != "'":
            email += ch
        else:
            email += str(randint(10, 99))
            break
    email += "@{}.{}".format(choice(email_suffixes), choice(domains))
    return email


def generate_street_name_from_town(collection):
    """ generate_street_name_from_town works with any mongoDB collection with a 'town' field
    and produces a street name from single word towns only
    :param collection: mongoDB collection cursor with 'town' field
    :return: suitable town name (based on filtering criteria), string
    """

    size = collection.count()
    seed()

    # filter out hyphenated and multi-word names
    while True:
        town = collection.find_one({"number": randint(1, size)})['town']
        if len(town.split('-')) > 1:
            continue
        elif len(town.split(' ')) > 1:
            return town[0]
        else:
            return town


def generate_addresses(size=100):
    """ generate_addresses: Creates a list of mock UK address of length size
    a rudimentary weighting algorithm is used to generated apartment numbers and street names
    :param size: desired number of addresses to create, int
    :return: a list of size mock UK addresses, strings
    """

    street_suffix = ['Rd', 'St', 'Mews', 'Rise', 'Hill', 'Close', 'Crescent', 'Ave', 'Ln', 'Row', 'Court']
    flat_suffix = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g']
    street_nouns = []
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Nouns commonly associated with UK street names are contained in the file 'streetnouns.txt'
    with open('street_nouns.txt', 'r') as fd:
        for line in fd:
            line = line.strip().capitalize()
            street_nouns.append(line)

    host = "localhost"
    port = "27017"
    connection = "mongodb://{}:{}/".format(host, port)

    with mgo.MongoClient(connection) as client:
        db = client["uk_towns"]
        towns = db['town_and_county']

        for i in range(size):
            flatsfx = {'high': flat_suffix[0], 'low': str(choice(flat_suffix[1:]))}
            seed()
            # provides a 15% chance of an apartment in the listing
            house_number = str(randint(1, 200)) + (flatsfx['high'] if randint(1, 100) < 85 else flatsfx['low'])
            seed()
            # provides a 50% chance of street name beginning with a UK town name, otherwise picks
            # a name from the common street noun list
            street = "{} {}".format(choice(street_nouns) if randint(1, 100) < 50 else
                                    generate_street_name_from_town(towns),
                                    choice(street_suffix))

            # generate the fake postcode
            postcode = "{}{} {}{}".format(town[:2].upper(), str(randint(1, 20)), str(randint(1, 9)), choice(alphabet) + choice(alphabet))
            home, mobile = create_phone_numbers(town)
            yield house_number, street, town, county, postcode, home, mobile

if __name__ == '__main__':
    # We'll create a client_details database and populate is with documents with the following schema
    # first_name, last_name, Address(House, Street,Town,County,Postcode),Email, Phone(Home, Mobile)
    # Generate a population of names and contact details
    population = 200

    # Create generators for efficiency
    names = generate_names(population)
    details = generate_addresses(population)
    hostname = 'localhost'
    port = '27017'
    connection = "mongodb://{}:{}/".format(hostname, port)
    print("connecting to {}...".format(connection))

    with mgo.MongoClient(connection) as dbclient:
        db = dbclient['customers']
        print("dropping existing collection...")
        db.drop_collection('contact_info')
        print("Adding new contact details to database...")
        for i in range(population):
            first_name, last_name, email = next(names)
            house_number, street, town, county, postcode, home, mobile = next(details)
            db['contact_info'].insert({"first_name":first_name,
                                       "last_name": last_name,
                                       "address": {
                                           "house": house_number,
                                           "street": street,
                                           "town": town,
                                           "county": county,
                                           "postcode": postcode},
                                       "email": email,
                                       "tel": {
                                           "home": home,
                                           "mobile": mobile
                                       }})
