import psycopg2
import csv

try:
    conn = psycopg2.connect("dbname='pets' user='action' host='localhost'")
#     print "I am connected to the database!"
except:
    print "I am unable to connect to the database"

mydict = {}
# Connect to the database
cur = conn.cursor()
with open('pets_to_add.csv', 'rb') as f:
    # Create a CSV reader
    dictReader = csv.DictReader(f, skipinitialspace=True)
    for new_pet in dictReader:
    # create a database request
        cur.execute(""" INSERT INTO pet("shelter_name", name, age, adopted, "breed_name", "species_name", shelter_id, breed_id, species_id)
        VALUES (%(shelter_name)s, %(name)s, %(age)s, %(adopted)s, %(breed_name)s, %(species_name)s,
        (SELECT id FROM shelter WHERE name=%(shelter_name)s),
        (SELECT id FROM breed WHERE name=%(breed_name)s),
        (SELECT id FROM species WHERE name=%(species_name)s))""", new_pet)
        conn.commit()
    	print new_pet

# Show results
cur.fetchall()
# look up how to insert a FK
"""
INSERT INTO pet (shelter_name) VALUES ( 'testing',     SELECT id from foo WHERE type='blue' )

(select id from species where name=%(species_name)s)
"""
