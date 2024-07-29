import psycopg2
from faker import Faker
import random
import time

# Initialize the Faker object
fake = Faker()

# Establish a connection to your MySQL database

conn = psycopg2.connect(database="yugabyte",
                        host="asia-east1.184b8e94-a319-4264-b326-2fca35dc2fb4.gcp.ybdb.io",
                        user="admin",
                        password="XQngPMG9Zius9zwD9Exn72iSXuy3bH",
                        port="5433",
                        sslMode= 'verify-full',
                        sslRootCert= './server/root.crt'
                        )

cursor = conn.cursor()

# Create functions to generate fake data for each table
def generate_city_data():
    return {
        "city_name": fake.city()
    }

def generate_region_data():
    return {
        "region_name": fake.state()
    }

def generate_address_data(city_ids, region_ids):
    return {
        "street_address": fake.street_address(),
        "room_number": fake.building_number(),
        "city_id": random.choice(city_ids),
        "region_id": random.choice(region_ids)
    }

def generate_parties_data():
    return {
        "nature": fake.random_element(elements=('Individual', 'Company')),
        "name": fake.name()
    }

def generate_property_data(address_ids):
    return {
        "address_id": random.choice(address_ids),
        "total_sqm": fake.random_int(min=50, max=500),
        "number_bedroom": fake.random_int(min=1, max=5),
        "number_bathroom": fake.random_int(min=1, max=3),
        "amenity": fake.random_element(elements=('Pool', 'Garage', 'Garden'))
    }

def generate_transaction_data(party_ids, property_ids):
    transaction_type = fake.random_element(elements=('Sale', 'Rent'))
    if transaction_type == "Sale":
        return {
            "party_id": random.choice(party_ids),
            "transaction_type": transaction_type,
            "property_id": random.choice(property_ids),
            "date": fake.date(),
            "price": fake.random_int(min=10000, max=1000000)
        }
    else:
        return {
            "party_id": random.choice(party_ids),
            "transaction_type": transaction_type,
            "property_id": random.choice(property_ids),
            "date": fake.date(),
            "price": fake.random_int(min=1000, max=10000)
        }
    

# Function to insert data into the database
def insert_data(sql, data_batch):
    values = [tuple(data.values()) for data in data_batch]
    cursor.executemany(sql, values)
    conn.commit()

# SQL statements for insertion
sql_insert_city = "INSERT INTO city (city_name) VALUES (%s)"
sql_insert_region = "INSERT INTO region (region_name) VALUES (%s)"
sql_insert_address = "INSERT INTO address (street_address, room_number, city_id, region_id) VALUES (%s, %s, %s, %s)"
sql_insert_parties = "INSERT INTO parties (nature, name) VALUES (%s, %s)"
sql_insert_property = "INSERT INTO properties (address_id, total_sqm, number_bedroom, number_bathroom, amenity) VALUES (%s, %s, %s, %s, %s)"
sql_insert_transaction = "INSERT INTO transactions (party_id, transaction_type, property_id, date, price) VALUES (%s, %s, %s, %s, %s)"

# Generate and insert data in batches
batch_size = 1000
city_records = 1000
region_records = 1000
address_records = 5000
party_records = 10000
property_records = 10000
transaction_records = 200000

start_time = time.time()

# Insert data into city table
for i in range(city_records // batch_size):
    data_batch = [generate_city_data() for _ in range(batch_size)]
    insert_data(sql_insert_city, data_batch)
    print(f"Inserted {(i + 1) * batch_size} records into city...")

# Insert data into region table
for i in range(region_records // batch_size):
    data_batch = [generate_region_data() for _ in range(batch_size)]
    insert_data(sql_insert_region, data_batch)
    print(f"Inserted {(i + 1) * batch_size} records into region...")

# Fetch city_ids and region_ids
cursor.execute("SELECT city_id FROM city")
city_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT region_id FROM region")
region_ids = [row[0] for row in cursor.fetchall()]

# Insert data into address table
for i in range(address_records // batch_size):
    data_batch = [generate_address_data(city_ids, region_ids) for _ in range(batch_size)]
    insert_data(sql_insert_address, data_batch)
    print(f"Inserted {(i + 1) * batch_size} records into address...")

# Fetch address_ids
cursor.execute("SELECT address_id FROM address")
address_ids = [row[0] for row in cursor.fetchall()]

# Insert data into parties table
for i in range(party_records // batch_size):
    data_batch = [generate_parties_data() for _ in range(batch_size)]
    insert_data(sql_insert_parties, data_batch)
    print(f"Inserted {(i + 1) * batch_size} records into parties...")

# Fetch party_ids
cursor.execute("SELECT party_id FROM parties")
party_ids = [row[0] for row in cursor.fetchall()]

# Insert data into properties table
for i in range(property_records // batch_size):
    data_batch = [generate_property_data(address_ids) for _ in range(batch_size)]
    insert_data(sql_insert_property, data_batch)
    print(f"Inserted {(i + 1) * batch_size} records into properties...")

# Fetch property_ids
cursor.execute("SELECT property_id FROM properties")
property_ids = [row[0] for row in cursor.fetchall()]

# Insert data into transactions table (more than 100,000 records)
for i in range(transaction_records // batch_size):
    data_batch = [generate_transaction_data(party_ids, property_ids) for _ in range(batch_size)]
    insert_data(sql_insert_transaction, data_batch)
    print(f"Inserted {(i + 1) * batch_size} records into transactions...")

# Close the connection
cursor.close()
conn.close()

end_time = time.time()
print(f"Time taken to insert data: {end_time - start_time} seconds")