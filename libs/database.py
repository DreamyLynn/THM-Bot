import libs.config as config
import json
import mysql.connector

jsonFile = config.get_config("db_file")
jsonDB = json.loads(open(jsonFile, "r").read())

host = jsonDB["host"]
database = jsonDB["db"]
user = jsonDB["user"]
passwd = jsonDB["pass"]
user_table = jsonDB["user_table"]
row_discord_UID = jsonDB["discord_uid"]
row_thm_token = jsonDB["thm_discord_token"]


def connect_to_db():
    try:
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
    except:
        print("\n[ERROR]\t Could not connect to database.")
        exit()
    
    return connection


def add_user(db, discord_uid, thm_token):
    mycursor = db.cursor()
    
    sql = f"INSERT INTO {user_table} ({row_discord_UID}, {row_thm_token}) values (%s, %s)"
    val = (discord_uid, thm_token)

    mycursor.execute(sql, val)


def remove_user_by_discord_uid(db, discord_uid):
    mycursor = db.cursor()
    
    sql = f"DELETE FROM {user_table} WHERE {row_discord_UID} = %s"
    val = (discord_uid, )

    mycursor.execute(sql, val)


def get_user_all(db):
    mycursor = db.cursor()
    
    sql = "SELECT * FROM "+ user_table

    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result


def get_user_by_discord_uid(db, discord_uid):
    mycursor = db.cursor()
    
    sql = f"SELECT * FROM {user_table} WHERE {row_discord_UID} = %s"
    val = (discord_uid, )

    mycursor.execute(sql, val)
    result = mycursor.fetchall()

    return result


def get_user_by_thm_token(db, thm_token):
    mycursor = db.cursor()
    
    sql = f"SELECT * FROM {user_table} WHERE {row_thm_token} = %s"
    val = (thm_token, )

    mycursor.execute(sql, val)
    result = mycursor.fetchall()

    return result
