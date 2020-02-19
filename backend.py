import json
import mysql.connector
from datetime import date, datetime

class UserData:
    def __init__(self):
        self.data = '{}'
        self.load_data()

    def load_data(self):
        with open('data.json', 'r') as f:
            self.data = json.load(f)

    def update_data(self, new_name, new_surname):
        self.data['logged_once'] = 'Yes'
        self.data['name'] = new_name
        self.data['surname'] = new_surname

        self.write_data(self.data)

    def write_data(self, d):
        with open('data.json', 'w') as outfile:
            json.dump(d, outfile)



class Database:

    class DatabaseData:
        def __init__(self):
            self.data = '{}'
            self.load_data()
            self.db_name = self.data['db_name']
            self.username = self.data['username']
            self.password = self.data['password']
            self.host = self.data['host']
            self.port = int(self.data['port'])
            self.today = date.today()
            self.today_format = self.today.strftime("%Y-%m-%d")

        def load_data(self):
            with open('db_data.json', 'r') as f:
                self.data = json.load(f)

    def __init__(self):
        self.db_connector = 0
        self.db_data = self.DatabaseData()
        self.connect()
        self.query = ""

    def connect(self):
        self.db_connector = mysql.connector.connect(user=self.db_data.username,
                                                    password=self.db_data.password,
                                                    host=self.db_data.host,
                                                    database=self.db_data.db_name,
                                                    port=self.db_data.port)
        self.cursor = self.db_connector.cursor()

    def close(self):
        self.cursor.close()
        self.db_connector.close()

    def send_raport(self, u_name, u_surname, u_raport):
        self.query = "INSERT INTO Raports (name, surname, date, raport) VALUES(%s, %s, %s, %s)"
        values = (u_name, u_surname, str(self.db_data.today_format), u_raport)
        self.cursor.execute(self.query, values)
        self.db_connector.commit()

    def generate_raport(self):
        generated_raport = ""
        self.query = "SELECT name, surname, raport FROM Raports WHERE date = " + "'" + str(self.db_data.today_format) + "'"
        self.cursor.execute(self.query)
        for (name, surname, raport) in self.cursor:
            generated_raport += "{} {} \n {} \n\n".format(name, surname, raport)
        return generated_raport

    def check_if_pushed(self):
        self.query = "SELECT date FROM History WHERE date = " + "'" + str(self.db_data.today_format) + "'"
        self.cursor.execute(self.query)
        is_already_pushed = 0
        for date in self.cursor:
            is_already_pushed = 1
        return is_already_pushed

    def push_raport(self):
        self.query = "INSERT INTO History (date) VALUE (" + "'" + str(self.db_data.today_format) + "'" + ")"
        self.cursor.execute(self.query)
        self.db_connector.commit()

    def load_dates_to_list(self):
        self.query = "SELECT DISTINCT date FROM History"
        self.cursor.execute(self.query)
        list = []
        iter = 0
        for date in self.cursor:
            list.append(date[iter].strftime("%Y-%m-%d"))
        return list

    def show_history(self, selected_date):
        generated_raport = ""
        self.query = "SELECT name, surname, raport FROM Raports WHERE date = " + "'" + str(selected_date) + "'"
        self.cursor.execute(self.query)
        for (name, surname, raport) in self.cursor:
            generated_raport += "{} {} \n {} \n\n".format(name, surname, raport)
        return generated_raport