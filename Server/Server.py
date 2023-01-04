#!/usr/bin/env

from flask import Flask, jsonify, request
from flask_cors import CORS
import Mysql
import requests
import random
import hashlib
import CONFIG     #SERVER CONGIG

app = Flask(__name__)
CORS(app)

# config
app.config.update(
    SECRET_KEY = CONFIG.SECRET_KEY
)

@app.route("/create_user",methods=["GET","POST"])
def handle_create_user():
    
    if request.method == "POST":

        wallet = request.json["wallet"]
        tokenid = request.json["nftid"]
        uniqeid = hashlib.sha256(str(wallet+tokenid).encode("utf-8")).hexdigest()
        
        List_Of_users = Mysql.read_users_from_database() 
        List_of_nfts = []

        for user in List_Of_users:

            id, wallet_db, nft, uniqeid_db = user
            List_of_nfts.append(nft)

        if tokenid in List_of_nfts:
            
            if Check_User(wallet, tokenid) != True :
            
                ret = {"code" : 402 , "data" : "user dont have nft !"}
                return jsonify(ret) , 402
            
            else:
            
                if Mysql.remove_user_from_database(tokenid) and Mysql.write_user_to_database(wallet,tokenid,uniqeid):
                
                    ret = {"code" : 200 , "data" : "new user create correctly !"}
                    return jsonify(ret) , 200

                else:

                    ret = {"code" : 401 , "data" : "error connection with mysql !"}
                    return jsonify(ret) , 401

        if Check_User(wallet, tokenid): 
        
            if Mysql.write_user_to_database(wallet,tokenid,uniqeid):
            
                ret = {"code" : 200 , "data" : "user create correctly !"}
                return jsonify(ret) , 200

            else:

                ret = {"code" : 401 , "data" : "error connection with mysql !"}
                return jsonify(ret) , 401
        
        else:

            ret = {"code" : 403 , "data" : "user dont have nft !"}
            return jsonify(ret), 403

    ret = {"code" : 500 , "data" : "request not valid !"}
    return jsonify(ret) , 500

@app.route("/groups")
def handle_return_open_group():
    
    List_Of_Groups = Mysql.read_groups_from_database()
    Jsonify_List_Of_Open_Groups = {} 
    
    for Group in List_Of_Groups:
    
        id, wallet1, wallet2, wallet3, winner, uniqeid, status = Group
        
        if status != "closed":
        
            Jsonify_List_Of_Open_Groups[id] = {'wallet1' : wallet1 , 'wallet2' : wallet2 , 'wallet3' : wallet3, 'winner' : winner , "uniqeid" : uniqeid}
        
        else:
            continue

    Response = {'Status Code':200 , 'groups': Jsonify_List_Of_Open_Groups}
    return jsonify(Response), 200

@app.route("/history")
def handle_return_close_group():
    
    List_Of_Groups = Mysql.read_groups_from_database()
    Jsonify_List_Of_Close_Groups = {} 
    
    for Group in List_Of_Groups:
    
        id, wallet1, wallet2, wallet3, winner, uniqeid, status = Group
        
        if status == "closed":
        
            Jsonify_List_Of_Close_Groups[id] = {'wallet1' : wallet1 , 'wallet2' : wallet2 , 'wallet3' : wallet3, 'winner' : winner , "uniqeid" : uniqeid}
        
        else:
            continue

    Response = {'Status Code':200 , 'groups': Jsonify_List_Of_Close_Groups}
    return jsonify(Response), 200

@app.route("/balance")
def handle_balance():

    wallet = CONFIG.MAIN_WALLET
    baseurl = CONFIG.APIURL
    apikey = CONFIG.APIKEY
    query = f"?module=account&action=balance&address={wallet}&tag=latest&apikey={apikey}"

    url = baseurl + query
    response = requests.get(url)
    balance = int(response.json()['result']) / 1000000000000000000

    Response = {'Code':200 , 'balance': balance}
    return jsonify(Response), 200

@app.route("/winners")
def handle_return_winners():

    if request.method == "POST":
        
        wallet = request.json["wallet"]

        if Mysql.update_winner_payment_in_database(wallet):

            ret = {f"payment status for {wallet} insert in database correctly."}
            return jsonify(ret)
        
        else:
            ret = {"code" : 400 , "data" : "error connection with mysql !"}
            return jsonify(ret)

    List_Of_winners = Mysql.read_winners_from_database()
    Jsonify_List_Of_winners = {}
    
    for winer in List_Of_winners:
    
        id, wallet , payment= winer
        Jsonify_List_Of_winners[id] = {"winner" : wallet , 'amount' : '0.07776', 'status' : payment}
        

    Response = {'Code':200 , 'winners': Jsonify_List_Of_winners}
    return jsonify(Response), 200

@app.route("/create_group",methods=["GET","POST"])
def handle_create_group():

    if request.method == 'POST':
        
        wallet = request.json["wallet"]
        nftid = request.json["nftid"]
        uniqeid = hashlib.sha256(str(wallet).encode("utf-8")).hexdigest()

        List_Of_users = Mysql.read_users_from_database() 
        List_of_wallets = []

        for user in List_Of_users:

            id, wallet_db, nft, uniqeid_db = user
            List_of_wallets.append(wallet_db)

        if wallet in List_of_wallets:

            if Check_User(wallet, nftid):
            
                if Mysql.create_group_to_database(wallet,uniqeid):
                    
                    ret = {"code" : 200 , "data" : "group create correctly !"}
                    return jsonify(ret) , 200

                else:

                    ret = {"code" : 401 , "data" : "error connection with mysql !"}
                    return jsonify(ret) , 401
            
            else:

                ret = {"code" : 402 , "data" : "user dont have nft !"}
                return jsonify(ret) , 402

        else:

            ret = {"code" : 404 , "data" : "user dont exist on database !"}
            return jsonify(ret) , 404

    ret = {"code" : 500 , "data" : "request not valid !"}
    return jsonify(ret) , 500


@app.route("/add_to_group",methods=["POST","GET"])
def handle_add_to_group():

    if request.method == "POST":

        wallet = request.json["wallet"]
        nftid = request.json["nftid"]
        uniqeid = request.json["uniqeid"]

        List_Of_Groups = Mysql.read_groups_from_database()
        
        if Check_User(wallet,nftid):
        
            for Group in List_Of_Groups:
            
                id, wallet1, wallet2_db, wallet3, winner, uniqeid_db, status = Group
                
                if status != "closed":

                    if uniqeid_db == uniqeid and wallet2_db != "0":
                        
                        if Mysql.writing_Wallet3_in_group_to_database(wallet,uniqeid):

                            List_Of_Groups_db = Mysql.read_groups_from_database()
                            List_chance = []

                            for Group_db in List_Of_Groups_db:
                            
                                id, wallet1_db_winner, wallet2_db_winner, wallet3_db_winner, winner_db, uniqeid_db_winner, status_db = Group_db
                                
                                if uniqeid_db_winner == uniqeid:
                                    List_chance.append(wallet1_db_winner)
                                    List_chance.append(wallet2_db_winner)
                                    List_chance.append(wallet3_db_winner)
                            
                            winner = random.choice(List_chance)
                            Mysql.writing_Winer_to_database(winner,uniqeid)
                            ret = {"code" : 200 , "data" : "wallet 3 added to group correctly !"}
                            return jsonify(ret) , 200

                        else:

                            ret = {"code" : 406 , "data" : "error connection to database!"}
                            return jsonify(ret) , 406

                    else:

                        if uniqeid_db == uniqeid and Mysql.writing_Wallet2_in_group_to_database(wallet,uniqeid):

                            ret = {"code" : 200 , "data" : "wallet 2 added to group correctly !"}
                            return jsonify(ret) , 200

                        else:

                            ret = {"code" : 406 , "data" : "error connection to database!"}
                            return jsonify(ret) , 406

            else:

                ret = {"code" : 402 , "data" : "group status is closed !"}
                return jsonify(ret) , 402

        else:

                ret = {"code" : 401 , "data" : "user dont have nft !"}
                return jsonify(ret) , 402

    ret = {"code" : 500 , "data" : "request not valid !"}
    return jsonify(ret) , 500

def Check_User(user, TokenID):
    '''This function check user address and user nft to validate user'''

    contract = CONFIG.CONTRACT_ADDRESS
    apikey = CONFIG.APIKEY
    baseurl = CONFIG.APIURL
    
    query = f"?module=account&action=addresstokennftinventory&address={user}&contractaddress={contract}&page=1&offset=100&apikey={apikey}"
    #query1 = f"?module=account&action=tokennfttx&contractaddress={contract}&address={user}&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey={apikey}"

    url = baseurl + query
    response = requests.get(url)
    json_Response = response.json()

    try:

        list_tokens = []
        
        for result in json_Response["result"]:
            list_tokens.append(result["TokenId"])
        
        if TokenID in list_tokens:
            return True

        else:
            return False

    except:
        return False

if __name__ == "__main__":
    app.run("0.0.0.0",80,debug=True)