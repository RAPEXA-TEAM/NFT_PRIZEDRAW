#!/usr/bin/env
import sys
import pymysql
import CONFIG     #SERVER CONGIG

def connect_to_database():
    '''This function make a connection with datebase'''
    db = pymysql.connect(host=CONFIG.MYSQL_HOST,
                       user=CONFIG.MYSQL_USER,
                       passwd=CONFIG.MYSQL_PASS,
                       db=CONFIG.MYSQL_DATABAS)
    return(db)

def write_user_to_database(wallet, nft, uniqeid):
    '''this function create user on database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO users (id, wallet, nft, uniqeid) VALUES (null, "{wallet}", "{nft}", "{uniqeid}");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def remove_user_from_database(nft):
    '''this function remove user that at past have this nft'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'DELETE FROM users WHERE nft = "{nft}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True    

def create_group_to_database(wallet1, uniqeid):
    '''this function create user on database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO groupss (id, wallet1, wallet2, wallet3, winner, uniqeid, status) VALUES (null, "{wallet1}", "0", "1", "2", "{uniqeid}", "open");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def writing_Wallet2_in_group_to_database(wallet,uniqeid):
    '''This function write one game winner to database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE groupss SET wallet2 = "{wallet}" WHERE uniqeid = "{uniqeid}";'
    cur.execute(qury)
    db.commit()
    db.close()
    return True

def writing_Wallet3_in_group_to_database(wallet,uniqeid):
    '''This function write one game winner to database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE groupss SET wallet3 = "{wallet}" WHERE uniqeid = "{uniqeid}";'
    cur.execute(qury)
    db.commit()
    db.close()
    return True

def writing_Winer_to_database(winer_wallet,uniqeid):
    '''This function write one game winner to database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE groupss SET winner = "{winer_wallet}" WHERE uniqeid = "{uniqeid}";'
    cur.execute(qury)
    db.commit()
    db.close()
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE groupss SET status = "closed" WHERE uniqeid = "{uniqeid}";'
    cur.execute(qury)
    db.commit()
    db.close()
    db = connect_to_database()
    cur = db.cursor()
    query = f'INSERT INTO winers (id, winner , payment) VALUES (null, "{winer_wallet}", "no");'
    cur.execute(query)
    db.commit()
    db.close()
    return True

def update_winner_payment_in_database(winner):
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE winers SET payment = "yes" WHERE winner = "{winner}";'
    cur.execute(qury)
    db.commit()
    db.close()
    return True

def read_groups_from_database():
    '''this function return all working dates'''
    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM groupss;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def read_users_from_database():
    '''this function return all users informations'''
    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM users;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def read_winners_from_database():
    '''this function return all winers informations'''
    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM winers;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()