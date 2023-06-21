from pymongo import MongoClient
import json

# Set up the MongoDB client, replace "your_connection_string" with your actual connection string
client = MongoClient("mongodb://127.0.0.1:27017")

# Select the database and collection
db = client["community_garden"]
collection = db["p_patch_data_2"]

# Open the JSON file and load it into a Python object
with open("output.txt") as file:
    data = json.load(file)

for obj in data:
    obj['_id'] = obj['SomeUniqueField']

# Write the updated JSON objects back to the file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

# Insert the JSON objects into the collection
collection.insert_many(data)