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


company, id, email = ("Inkitt", 76, "german@inkitt.com")
print(company, id ,email)

domain = collection.find_one({"Company": company}, {"Domain":1, "_id":0})
print(domain["Domain"])


collection.find_one_and_update({ "Company": company, "data_dict" :{"$elemMatch" : {"id": id}} }, 
                            {'$set': {
                                "data_dict.$.email": email,
                                "data_dict.$.Verification": True,
                                "data_dict.$.Checked24": datetime.now(),
                                "data_dict.$.Type": "Personal"                            
                            }
                            })

# COMMON_DOMAIN = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com", "aol.com", "protonmail.com", "zoho.com", "ymail.com", "live.com", "mail.com", "gmx.com", "me.com", "rocketmail.com", "tutanota.com", "fastmail.com", "att.net", "verizon.net", "cox.net", "sbcglobal.net"]

# def get_file_dict(file_name):
#     file_dict = dict()

#     with open(file_name, "r") as file:
#         for line in file:
#             line_data = (line.split("\n")[0]).split(", ")
#             file_dict[int(line_data[0])] = "Not Found" if line_data[-1] in ("Verifying", "Not Found") else line_data[-1]
        
#     return file_dict

# file_dict = get_file_dict("Output_False_Email.csv")

# print("Length of File_Dict: ",len(file_dict.keys()))
# #---------------------------------------------------

# Comp = "Universal Music Group"

# Company = collection.find({"Company": Comp}, {"data_dict": 1, "_id": 0})[0]

# for i in Company["data_dict"]:


#     if i["id"] in file_dict.keys():
#         if file_dict[i["id"]] == "Not Found": continue
            
#         print(f"{i['id']}:::", i["first"], i["last"], sep=" ")

#         if ( file_dict[i["id"]].split("@")[-1] )in COMMON_DOMAIN:

#             print("personal")
#             collection.replace_one({ "Company": Comp, "data_dict" :{"$elemMatch" : {"id": i["id"]}} }, 
#                             {'$set': {
#                                 "data_dict.$.email": file_dict[i["id"]],
#                                 "data_dict.$.Verification": True,
#                                 "data_dict.$.Checked24": datetime.now(),
#                                 "data_dict.$.Type": "Personal"
                            
#                             }
#                             })
#         else:
#             print("professional")
#             collection.find_one_and_update({ "Company": Comp, "data_dict" :{"$elemMatch" : {"id": i["id"]}} }, 
#                             {'$set': 
#                             {
#                                 "data_dict.$.email": file_dict[i["id"]],
#                                 "data_dict.$.Verification": True,
#                                 "data_dict.$.Checked24": datetime.now()
                            
#                             }})
        
        