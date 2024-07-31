import sqlite3
from sqlite3 import Error


def create_table():
    try:
        connection= sqlite3.connect('sqlite3.db')

        table = """ CREATE TABLE Members (
                    chat_id BIGINT NOT NULL ,
                    user_id BIGINT NOT NULL ,
                    fullname TEXT NOT NULL ,
                    soni BIGINT NOT NULL
                ); """
        cursor = connection.cursor()
        print("databaza yaratildi")
        cursor.execute(table)
        cursor.close()
    
    except Error as error:
        print("hatolik", error)
    finally:
        if connection:
            connection.close()    
            print("sqlite o'chdi")
# create_table()
            

def Add_db(chat_id, user_id, fullname, soni):
    try:
        with sqlite3.connect("sqlite3.db") as connection:
            cursor = connection.cursor()
            
            table = '''
                INSERT INTO Members(chat_id, user_id, fullname, soni) VALUES(?, ?, ?, ?)
            '''
            cursor.execute(table, (chat_id, user_id, fullname, soni))
            connection.commit()
            print("SQLite tablega qo'shildi")
            cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if connection:
            connection.close()
            # print("Sqlite ish foalyatini tugatdi")   


def Read_db():
    try:
        with sqlite3.connect("sqlite3.db") as sqliteconnection:
            cursor = sqliteconnection.cursor()
            sql_query = """
                SELECT * FROM Members 
            """
        
            cursor.execute(sql_query) 
            A = cursor.fetchall()
            print("table oqildi")
            return A

    except Error as error:
        print("xatolik:", error)
    finally:
        if sqliteconnection:
            sqliteconnection.close()
            # print("sqlite faoliyatini tugatdi")       


def Update_Soni(soni, chat_id, user_id):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE Members SET soni = ? WHERE chat_id = ? AND user_id = ?", (soni, chat_id, user_id)
            )
            con.commit()
            print("mahsulot soni yangilandi")
            cur.close()

    except sqlite3.Error as err:
        print(f"Yangilashda xatolik: {err}")
    finally:
        if con:
            con.close()
            # print("Sqlite ish foalyatini tugatdi")                               