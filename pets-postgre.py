import psycopg2
import csv

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
    cur.execute(""" INSERT INTO shelter(name) VALUES ('NYSPCA') """)
    conn.commit()

#     # Create a CSV reader
    dictReader = csv.DictReader(f, skipinitialspace=True)
#     for row in dictReader:
#         for key, value in row.iteritems():
#             results.setdefault(key, []).append(value)
#         print results
    for new_pet in dictReader:
        for item in new_pet:
            if new_pet[item] is None or new_pet[item] is '':
                new_pet[item] = "NULL"
            if new_pet[item].isalpha():
                new_pet[item] = new_pet[item].capitalize()
            print new_pet[item],

        # create a database request
        cur.execute(""" INSERT INTO pet("shelter_name", name, age, adopted, "breed_name", "species_name", shelter_id, breed_id, species_id)
        VALUES (%(shelter_name)s, %(name)s, %(age)s, %(adopted)s, %(breed_name)s, %(species_name)s,
        (SELECT id FROM shelter WHERE name=%(shelter_name)s),
        (SELECT id FROM breed WHERE name=%(breed_name)s),
        (SELECT id FROM species WHERE name=%(species_name)s))""", new_pet)
        conn.commit()
#     	print new_pet

# Show results
# cur.fetchall()
# look up how to insert a FK
"""
INSERT INTO pet (shelter_name) VALUES ( 'testing',     SELECT id from foo WHERE type='blue' )

(select id from species where name=%(species_name)s)
"""