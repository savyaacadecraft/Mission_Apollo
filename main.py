from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime, timedelta


from validate_email_own import PatternCheck

from threading import Thread, Lock



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

from time import sleep
from sys import exit

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

COMPANY_EMPLOYEE_LIST = None
COMPANY_EMPLOYEE_LOCK = None
PROCESS_COMPLETE = False

COUNTER = 1000
BLOCK_COUNTER = 0

COMMON_DOMAIN = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com", "aol.com", "protonmail.com", "zoho.com", "ymail.com", "live.com", "mail.com", "gmx.com", "me.com", "rocketmail.com", "tutanota.com", "fastmail.com", "att.net", "verizon.net", "cox.net", "sbcglobal.net"]

def update_pattern_list(ptrn):
        patterns = list()
        with open('patterns.txt', 'r') as f:
            for l in f:
                patterns.append(l.split("\n")[0])

        if ptrn in patterns:
            patterns.remove(ptrn)
            patterns.insert(0, ptrn)

        with open("patterns.txt", "w") as file:
            for pattern in patterns:
                file.write( pattern + "\n")

def data_insertion(company, id, email):
    global collection

    print("data_insertion :::: ",company, id, email)
    if ( email.split("@")[-1] )in COMMON_DOMAIN:

        print("personal")
        collection.replace_one({ "Company": company, "data_dict" :{"$elemMatch" : {"id": int(id)}} }, 
                            {'$set': {
                                "data_dict.$.email": email,
                                "data_dict.$.Verification": True,
                                "data_dict.$.Checked24": datetime.now(),
                                "data_dict.$.Type": "Personal"
                            
                            }
                            })
    else:
        print("professional")
        collection.find_one_and_update({ "Company": company, "data_dict" :{"$elemMatch" : {"id": int(id)}} }, 
                            {'$set': 
                            {
                                "data_dict.$.email": email,
                                "data_dict.$.Verification": True,
                                "data_dict.$.Checked24": datetime.now()
                            
                            }})

def email_verification():
    global COUNTER, COMPANY_EMPLOYEE_LIST, COMPANY_EMPLOYEE_LOCK, PROCESS_COMPLETE
    
    while True:
        if not len(COMPANY_EMPLOYEE_LIST):

            sleep(1)
            if PROCESS_COMPLETE: 
                break
            continue

        else:

            COMPANY_EMPLOYEE_LOCK.acquire()
            company, employee = COMPANY_EMPLOYEE_LIST.pop(0)
            COMPANY_EMPLOYEE_LOCK.release()

            counter = 0
            EMail = None
            ptrn = None
            MAX_ID = 65
            START_ID = 45
            domain = collection.find_one({"Company": company}, {"Domain":1, "_id":0})

            while True:
                try:

                    ptrn, EMail, counter = PatternCheck(employee["first"]+" "+employee["last"], domain["Domain"], START_ID)
                    break
                except Exception as E:
                    START_ID += 1
                    if START_ID == MAX_ID: break
                    

            if counter >= COUNTER:
                START_ID += 1


            if EMail:
                collection.update_one({ "Company": company, "data_dict" :{"$elemMatch" : {"id": employee["id"]}}}, {'$set': {
                        "data_dict.$.email": EMail,
                        "data_dict.$.Verification": True,
                        "data_dict.$.Checked24": datetime.now() 
                        }})
                update_pattern_list(ptrn)

            else:
                collection.update_one({"Company": company, "data_dict" :{"$elemMatch" : {"id": employee["id"]}}},  {'$set': {"data_dict.$.Verification": False}})

def pending_mail_verifier(engine, Company):
    global COMPANY_EMPLOYEE_LIST, COMPANY_EMPLOYEE_LOCK

    data = collection.find_one({"Company": Company,}, {"data_dict": 1})
    print(len(data["data_dict"]))
    for i in data["data_dict"]:
        
        if i['Verification'] == "pending":
            print(i["id"], "Employee Name:", i["first"], i["last"],sep=" ")
            
            # Visit to the LinkedIn Profile of Person whose Email Verification is Pending
            engine.get(i["Profile_Link"])
            sleep(1)

            try:
                WebDriverWait(engine, 2).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Sign in')]")))
                print(datetime.now(), " ::: ", BLOCK_COUNTER, file=open("BLOCK_COUNTER.txt", "a"))
                break
            
            except:
                BLOCK_COUNTER += 1
                # Searching for the Apollo Box for Checking
                try:
                    WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "apollo-opener-icon"))).click()
                except Exception as E:
                    print("Element not appeared by 10 Seconds Error.....", E)

                # Clicking on the View email address Textarea
                try:
                    WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'View email address')]"))).click()
                except Exception as E:
                    print("Clickable Text for Display Email was not found....")

                try:
                    email = WebDriverWait(engine, 2).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[13]/div/div[2]/div/div/div[4]/div/div[1]/div[1]/div[3]/div[1]/div/div[1]/div/div[2]/div/div/span/div"))).text
                    if email != "Verifying":

                        data_insertion(Company, i["id"], email)
                    else:

                        email = "Not Found"
                        COMPANY_EMPLOYEE_LOCK.acquire()
                        COMPANY_EMPLOYEE_LIST.append((Company, i))
                        COMPANY_EMPLOYEE_LOCK.release()

                except Exception as E:
                    email = "Not Found"
                    print("Email Not Found.......")
                    COMPANY_EMPLOYEE_LOCK.acquire()
                    COMPANY_EMPLOYEE_LIST.append((Company, i))
                    COMPANY_EMPLOYEE_LOCK.release()

            

                print(Company, i["id"], email, sep=", ", file=open(Company+"_Pending_Email.csv", "a"))
            
def false_mail_verifier(engine, Company):
    global COUNTER

    data = collection.find_one({"Company": Company,}, {"data_dict": 1})
    for i in data["data_dict"]:
        
        if i['Verification'] == False:
            COUNTER += 1
            print("Employee Name:", i["first"], i["last"],sep=" ")
            
            # Visit to the LinkedIn Profile of Person whose Email Verification is Pending
            engine.get(i["Profile_Link"])
            sleep(1)

            # Searching for the Apollo Box for Checking
            try:
                WebDriverWait(engine, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "apollo-opener-icon"))).click()
                sleep(0.5)
            except Exception as E:
                print("Element not appeared by 10 Seconds Error.....", E)
            
            # Clicking on the View email address Textarea
            try:
                WebDriverWait(engine, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'View email address')]"))).click()
            except Exception as E:
                print("Clickable Text for Display Email was not found....")

            try:
                email = WebDriverWait(engine, 2).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[13]/div/div[2]/div/div/div[4]/div/div[1]/div[1]/div[3]/div[1]/div/div[1]/div/div[2]/div/div/span/div"))).text
                if email != "Verifying":
                    data_insertion(Company, i["id"], email)
            except Exception as E:
                print("Email Not Found....")
                email = "Not Found"
            

            print(Company, i["id"], i["first"], i["last"], email, sep=", ", file=open(Company+"_False_Email.csv", "a"))


if __name__ == "__main__":

    COMPANY_EMPLOYEE_LIST = list()
    COMPANY_EMPLOYEE_LOCK = Lock()


    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9999")
    # options.add_argument("--headless")
    # options.add_argument("--incognito")

    service = Service(ChromeDriverManager().install())

    engine = webdriver.Chrome(service=service, options=options)

    engine.maximize_window()
    print("Operation Started-----")

    COUNTER = 0
    T1 = Thread(target=email_verification)
    T1.start()
    print("Thread is Up and Running......")
    
    # List of Companies for Verification Status as "pending"
    companies = collection.find({"data_dict.Verification": "pending"}, {"Company":1})
        
    for company in companies:

        print("Company Name :::: ", company["Company"])
        # pending_mail_verifier(engine, company["Company"])
        
    
    
    """
    # List of Companies for Verification Status as "False"
    companies = collection.find({"data_dict.Verification": False}, {"Company":1})

    for company in companies:
        # if company["Company"] in ["Permutive", "Inkitt"]: continue

        print("Company Name :::: ", company["Company"])
        false_mail_verifier(engine, company["Company"])
        print(f"Count for {company['Company']} :::::  {COUNTER}")
    """

    T1.join()
    PROCESS_COMPLETE = True