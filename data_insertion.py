from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timedelta

username = "manojtomar326"
password = "Tomar@@##123"
cluster_url = "cluster0.ldghyxl.mongodb.net"

# Encode the username and password using quote_plus()
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Create the MongoDB Atlas connection string with the encoded credentials
connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster_url}/test?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(connection_string)

# Query all documents in the collection
db = client['mydatabase']
collection = db['my_collection']

def get_data_from_file(file_name):

    file_data = list()
    with open(file_name, "r") as file:
        for line in file:
            line_data = tuple((line.split("\n")[0]).replace(' ','').split(","))
            file_data.append(line_data)

    print("Data Extraction Completed....")

    for i in file_data:
        company, emid, email = i
        print(":::: ", company, emid, email)

        x = collection.find_one_and_update({ "Company": company, "data_dict" :{"$elemMatch" : {"id": int(emid)}} }, 
                                {'$set': {
                                    "data_dict.$.email": email,
                                    "data_dict.$.Verification": True,
                                    "data_dict.$.Checked24": datetime.now(),                           
                                }
                                })

        
if __name__ == "__main__":

    Files = "Bitly.csv"
    get_data_from_file(Files)