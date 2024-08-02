import psycopg2
from faker import Faker
import random
import time

# Initialize the Faker object
fake = Faker()

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(database="yugabyte",
                        host="asia-east1.184b8e94-a319-4264-b326-2fca35dc2fb4.gcp.ybdb.io",
                        user="admin",
                        password="XQngPMG9Zius9zwD9Exn72iSXuy3bH",
                        port="5433",
                        )

cursor = conn.cursor()

# Create tables if they don't exist
create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS city (
        city_id SERIAL PRIMARY KEY,
        city_name VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS region (
        region_id SERIAL PRIMARY KEY,
        region_name VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS address (
        address_id SERIAL PRIMARY KEY,
        street_address VARCHAR(255) NOT NULL,
        room_number VARCHAR(50),
        city_id INT REFERENCES city(city_id),
        region_id INT REFERENCES region(region_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS parties (
        party_id SERIAL PRIMARY KEY,
        nature VARCHAR(50) NOT NULL,
        name VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS properties (
        property_id SERIAL PRIMARY KEY,
        address_id INT REFERENCES address(address_id),
        total_sqm INT NOT NULL,
        number_bedroom INT NOT NULL,
        number_bathroom INT NOT NULL,
        amenity VARCHAR(50)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id SERIAL PRIMARY KEY,
        transaction_type VARCHAR(50) NOT NULL,
        property_id INT REFERENCES properties(property_id),
        date DATE NOT NULL,
        price INT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS transaction_parties (
        transaction_party_id SERIAL PRIMARY KEY,
        transaction_id INT REFERENCES transactions(transaction_id),
        party_id INT REFERENCES parties(party_id),
        type VARCHAR(50) NOT NULL
    )
    """
]

# Execute table creation queries
for query in create_table_queries:
    cursor.execute(query)

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
        "nature": fake.random_element(elements=('Individual', 'Government', 'Organization')),
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
    return {
        "transaction_type": transaction_type,
        "property_id": random.choice(property_ids),
        "date": fake.date(),
        "price": fake.random_int(min=1000, max=1000000)
    }

def generate_transaction_parties_data(transaction_ids, party_ids):
    return {
        "transaction_id": random.choice(transaction_ids),
        "party_id": random.choice(party_ids),
        "type": fake.random_element(elements=('Owner', 'Seller', 'Buyer', 'Lessor', 'Lessee'))
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
sql_insert_transaction = "INSERT INTO transactions (transaction_type, property_id, date, price) VALUES (%s, %s, %s, %s)"
sql_insert_transaction_parties = "INSERT INTO transaction_parties (transaction_id, party_id, type) VALUES (%s, %s, %s)"

# Generate and insert data in batches
batch_size = 1000
city_records = 1000
region_records = 1000
address_records = 5000
party_records = 10000
property_records = 10000
transaction_records = 100000
transaction_parties_records = 200000

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

# Fetch transaction_ids
cursor.execute("SELECT transaction_id FROM transactions")
transaction_ids = [row[0] for row in cursor.fetchall()]

# Insert data into transaction_parties table
for i in range(transaction_parties_records // batch_size):
    data_batch = [generate_transaction_parties_data(transaction_ids, party_ids) for _ in range(batch_size)]
    insert_data(sql_insert_transaction_parties, data_batch)
    print(f"Inserted {(i + 1) * batch_size} records into transaction_parties...")

# Close the connection
cursor.close()
conn.close()

end_time = time.time()
print(f"Time taken to insert data: {end_time - start_time} seconds")
