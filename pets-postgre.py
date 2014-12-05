import psycopg2
import csv
from pprint import pprint as pp

try:
    conn = psycopg2.connect("dbname='pets' user='action' host='localhost'")
    print "I am connected to the database!"
except:
    print "I am unable to connect to the database"

# Create a dictionary to store results
mydict = {}
results = {}
# Connect to the database
cur = conn.cursor()
with open('pets_to_add.csv', 'rb') as f:
    # Add missing fields as needed
    cur.execute(""" INSERT INTO shelter(name) VALUES ('NYCSPCA') """)
    conn.commit()

#   Create a CSV reader
    dictReader = csv.DictReader(f, skipinitialspace=True)
#   Populate results
    for new_pet in dictReader:
        for item in new_pet:
            new_pet[item] = new_pet[item].title()
            if new_pet[item] is None or new_pet[item] is '':
                new_pet[item] = "NULL"

        # create a database request
        cur.execute("SELECT id FROM species WHERE name = %s", (new_pet["species_name"],))
        mySpeciesID = (cur.fetchone()[0])
        new_pet["species_id"] = mySpeciesID
        new_pet["shelter_name"] = new_pet["shelter_name"].upper()
        # print results from first request to check entries
        # pp(new_pet)

        # Show results & add values into database with FK's -- add the FK's in the order show in the cur.execute line.
        cur.execute(""" INSERT INTO pet("shelter_name", name, age, adopted, "breed_name", "species_name", shelter_id, breed_id, species_id)
        VALUES (%(shelter_name)s, %(name)s, %(age)s, %(adopted)s, %(breed_name)s, %(species_name)s,
        (SELECT id FROM shelter WHERE name=%(shelter_name)s),
        (SELECT id FROM breed WHERE name=%(breed_name)s and species_id=%(species_id)s),
        (SELECT id FROM species WHERE name=%(species_name)s))""", new_pet)
        conn.commit()
