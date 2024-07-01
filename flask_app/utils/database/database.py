import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row
    
    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        print("In creating tables..")

        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")


        # Open all SQL files, read them, and create them by querying into db
        f1 = open(data_path + "create_tables/feedback.sql")
        f2 = open(data_path + "create_tables/institutions.sql")
        f3 = open(data_path + "create_tables/positions.sql")
        f4 = open(data_path + "create_tables/experiences.sql")
        f5 = open(data_path + "create_tables/skills.sql")
        f6 = open(data_path + "create_tables/users.sql")
        sql_files = [f1, f2, f3, f4, f5, f6]

        for file in sql_files:
            query = file.read()
            self.query(query)

        # Pre-populate each table with CSV data
        pp1 = csv.reader(open(data_path + "initial_data/institutions.csv"))
        pp2 = csv.reader(open(data_path + "initial_data/positions.csv"))
        pp3 = csv.reader(open(data_path + "initial_data/experiences.csv"))
        pp4 = csv.reader(open(data_path + "initial_data/skills.csv"))

        table_names = ["institutions", "positions", "experiences", "skills"]
        csv_files = [pp1, pp2, pp3, pp4]

        for i in range(len(csv_files)):
            columns = next(csv_files[i])
            parameters = []
            for row in csv_files[i]:
                for j in range(len(row)):
                    if row[j] == 'NULL':
                        row[j] = None
                parameters.append(row)
            
            self.insertRows(table_names[i], columns, parameters)

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        cols_str = f"({', '.join(columns)})"
        for value in parameters:
            placeholder = ["%s" for _ in range(len(value))]
            value_str = f"({', '.join(placeholder)})"
            query = f"INSERT INTO {table}{cols_str} values{value_str};"
            self.query(query, value)
    
    def getResumeData(self):
        # Pulls data from the database to genereate nested dictionary of data
        master = {}
        query = """
                SELECT i.*, p.*
                FROM institutions i JOIN
                positions p
                ON i.inst_id = p.inst_id;
                """
        inst = self.query(query)
    
        
        for row in inst:
            if row["inst_id"] not in master:
                master[row['inst_id']] = {}
                master[row['inst_id']]['type'] = row['type']
                master[row['inst_id']]['name'] = row['name']
                master[row['inst_id']]['department'] = row['department']
                master[row['inst_id']]['address'] = row['address']
                master[row['inst_id']]['city'] = row['city']
                master[row['inst_id']]['state'] = row['state']
                master[row['inst_id']]['zip'] = row['zip']

            
                master[row['inst_id']]['positions'] = {}

            inst_dict = master[row['inst_id']] 
            if row['position_id'] not in inst_dict['positions']:
                inst_dict['positions'][row['position_id']] = {}
                inst_dict['positions'][row['position_id']]['title'] = row['title']
                inst_dict['positions'][row['position_id']]['responsibilities'] = row['responsibilities']
                inst_dict['positions'][row['position_id']]['start_date'] = row['start_date']
                inst_dict['positions'][row['position_id']]['end_date'] = row['end_date']
                inst_dict['positions'][row['position_id']]['experiences'] = {}


        query = """
                SELECT i.inst_id, p.position_id, e.*
                FROM institutions i JOIN positions p
                ON i.inst_id = p.inst_id
                JOIN experiences e
                ON e.position_id = p.position_id;
                """
        exp = self.query(query)

        for row in exp:
            inst_id = row["inst_id"]
            pos_id = row["position_id"]
            exp_id = row['experience_id']
            master[inst_id]["positions"][pos_id]["experiences"][exp_id] = {}
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]['name'] = row['name']
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]['description'] = row['description']
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]['hyperlink'] = row['hyperlink']
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]['start_date'] = row['start_date']
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]['end_date'] = row['end_date']
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]['skills'] = {}

        query = """
                SELECT i.inst_id, p.position_id, e.experience_id, s.*
                FROM institutions i JOIN positions p
                ON i.inst_id = p.inst_id
                JOIN experiences e
                ON e.position_id = p.position_id
                JOIN skills s
                ON s.experience_id = e.experience_id;
                """

        sk = self.query(query)

        for row in sk:
            inst_id = row["inst_id"]
            pos_id = row["position_id"]
            exp_id = row['experience_id']
            sk_id = row["skill_id"]
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]["skills"][sk_id] = {}
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]["skills"][sk_id]['name'] = row['name']
            master[inst_id]["positions"][pos_id]["experiences"][exp_id]["skills"][sk_id]['skill_level'] = row['skill_level']
        
        return master

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        query = f"SELECT email FROM users WHERE email='{email}';"
        res = self.query(query)
        # If there are any users from query, don't create duplicate
        if res:
            print("User creation failed.")
            # Return success code 0 if creation failed
            return {"success": 0}
        else:
            # Encrypt pw with Scrypt
            encrypted_pw = self.onewayEncrypt(password)

            columns = ["role", "email", "password"]
            params = [[role, email, encrypted_pw]]
            self.insertRows("users", columns, params)

            # Return success code 1 if creation was successful
            return {'success': 1}
    

    def authenticate(self, email='me@email.com', password='password'):
        auth_results = self.query(f"SELECT * FROM users WHERE email='{email}' and password='{password}';")
        
        # If list is not empty, we have found the email/pw combination
        if auth_results:
            print("Record Found! Login authenticated succesfully!")
            # Return success code 1 if auth was successful
            return {'success': 1}
        
        print("Cannot find user. Authentication failed.")
        # Return success code 0 if auth failed
        return {'success': 0}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


