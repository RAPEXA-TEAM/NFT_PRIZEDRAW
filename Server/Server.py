#!/usr/bin/env

from flask import Flask, jsonify, request
from flask_cors import CORS
from web3 import Web3
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

# whitelist

whitelist_wallets_file = open("Whitelist.txt","r")
whitelist_wallets_from_file = whitelist_wallets_file.readlines()
whitelist = []

for wallet in whitelist_wallets_from_file:
    whitelist.append(wallet.strip())

@app.route("/whitelist",methods=["GET","POST"])
def handle_whitelist():
    if request.method == "POST":

        wallet = request.json["wallet"]
        
        if wallet in whitelist:
            ret = {"code" : 200 , "data" : "ok"}
            return jsonify(ret)

        else:
            ret = {"code" : 404 , "data" : "error"}
            return jsonify(ret)    

    ret = {"code" : 500 , "data" : "request not valid !"}
    return jsonify(ret) , 500

@app.route("/wallets",methods=["GET","POST"])
def handle_wallets():

    try:    

        List_Of_users = Mysql.read_users_from_database() 
        Users = {}
        for user in List_Of_users:

            id, wallet_db, nft, uniqeid_db = user
            Users[wallet_db] = {'nft' : nft}

        Response = {'Status Code':200 , 'Users': Users}
        return jsonify(Response), 200

    except Exception as error:
        
        ret = {"code" : 400 , "data" : error}
        return jsonify(ret)

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

    try:    
        List_Of_Groups = Mysql.read_groups_from_database()
        Jsonify_List_Of_Open_Groups = {} 
        
        for Group in List_Of_Groups:
        
            id, wallet1, wallet2, wallet3, winner, uniqeid, status = Group
            nft1 = wallet_to_nft(wallet1)
            nft2 = wallet_to_nft(wallet2)
            nft3 = wallet_to_nft(wallet3)
            nft_winner = wallet_to_nft(winner)

            if status != "closed":
            
                Jsonify_List_Of_Open_Groups[id] = {'wallet1' : wallet1 , 'nft1' : nft1 , 'wallet2' : wallet2 , 'nft2' : nft2 , 'wallet3' : wallet3, 'nft3' : nft3 , 'winner' : winner , 'nft_winner' : nft_winner , "uniqeid" : uniqeid}
            
            else:
                continue

        Response = {'Status Code':200 , 'groups': Jsonify_List_Of_Open_Groups}
        return jsonify(Response), 200

    except Exception as error:
        
        ret = {"code" : 400 , "data" : error}
        return jsonify(ret)

@app.route("/history")
def handle_return_close_group():
    
    try:
        List_Of_Groups = Mysql.read_groups_from_database()
        Jsonify_List_Of_Close_Groups = {} 
        
        for Group in List_Of_Groups:
        
            id, wallet1, wallet2, wallet3, winner, uniqeid, status = Group
            nft1 = wallet_to_nft(wallet1)
            nft2 = wallet_to_nft(wallet2)
            nft3 = wallet_to_nft(wallet3)
            nft_winner = wallet_to_nft(winner)


            if status == "closed":
            
                Jsonify_List_Of_Close_Groups[id] = {'wallet1' : wallet1 , 'nft1' : nft1 , 'wallet2' : wallet2 , 'nft2' : nft2 , 'wallet3' : wallet3, 'nft3' : nft3 , 'winner' : winner , 'nft_winner' : nft_winner , "uniqeid" : uniqeid}
            
            else:
                continue

        Response = {'Status Code':200 , 'groups': Jsonify_List_Of_Close_Groups}
        return jsonify(Response), 200

    except Exception as error:

        ret = {"code" : 400 , "data" : error}
        return jsonify(ret)

@app.route("/balance")
def handle_balance():

    try:
    
        wallet = CONFIG.MAIN_WALLET
        baseurl = CONFIG.APIURL
        apikey = CONFIG.APIKEY
        query = f"?module=account&action=balance&address={wallet}&tag=latest&apikey={apikey}"

        url = baseurl + query
        response = requests.get(url)
        balance = int(response.json()['result']) / 1000000000000000000

        Response = {'Code':200 , 'data': balance}
        return jsonify(Response), 200
    
    except Exception as error:

        ret = {"code" : 400 , "data" : error}
        return jsonify(ret)

@app.route("/winners")
def handle_return_winners():

    List_Of_winners = Mysql.read_winners_from_database()
    Jsonify_List_Of_winners = {}
    
    for winer in List_Of_winners:
    
        id, wallet , payment= winer
        nft = wallet_to_nft(wallet)
        Jsonify_List_Of_winners[id] = {"winner" : wallet , 'nft' :nft,'txhash' : payment}
        

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

        if Check_attend(wallet):

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

        else:
            ret = {"code" : 401 , "data" : "user attended in prizedraw once !"}
            return jsonify(ret) , 401

    ret = {"code" : 500 , "data" : "request not valid !"}
    return jsonify(ret) , 500


@app.route("/add_to_group",methods=["POST","GET"])
def handle_add_to_group():

    if request.method == "POST":

        wallet = request.json["wallet"]
        nftid = request.json["nftid"]
        uniqeid = request.json["uniqeid"]

        List_Of_Groups = Mysql.read_groups_from_database()
        
        if Check_attend(wallet):

            if Check_User(wallet,nftid):
            
                for Group in List_Of_Groups:
                
                    id, wallet1, wallet2_db, wallet3, winner_db_a, uniqeid_db, status = Group
                    
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
                                tx_hash = Send_prize(winner)
                                Mysql.writing_Winer_to_database(winner,uniqeid,tx_hash)
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
        else:
            ret = {"code" : 401 , "data" : "user attended in prizedraw once !"}
            return jsonify(ret) , 401

    ret = {"code" : 500 , "data" : "request not valid !"}
    return jsonify(ret) , 500

def Send_prize(wallet):
    web3 = Web3(Web3.HTTPProvider(CONFIG.ETH_URL))
    block = web3.eth.get_block('latest')

    total_prize = (0.096 * 0.3) * 3
    prize_fee = total_prize * 0.1
    gas = 16000000000
    main_prize_without_gas_fee = total_prize - prize_fee
    main_prize_with_gas_fee = web3.toWei(main_prize_without_gas_fee, 'ether') - block.gasLimit

    #get the nonce.  Prevents one from sending the transaction twice
    nonce = web3.eth.getTransactionCount(wallet)

    #build a transaction in a dictionary
    tx = {
        'nonce': nonce,
        'to': str(wallet),
        'value': main_prize_with_gas_fee,
        'gas': block.gasLimit,
        'gasPrice': web3.eth.gas_price
    }

    #sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, CONFIG.WALLET_KEY)

    #send transaction
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    #get transaction hash
    return web3.toHex(tx_hash)

def wallet_to_nft(wallet):

    try:

        List_Of_users = Mysql.read_users_from_database() 
        Users = {}
        
        for user in List_Of_users:

            id, wallet_db, nft_db, uniqeid_db = user
            Users[wallet_db] = nft_db
        
        for Wallet_user, nft in Users.items():
            
            if wallet != Wallet_user:

                continue 

            else:

                return nft

        return "0"

    except:

        return "0"

def Check_attend(wallet):

    try:

        List_Of_Groups = Mysql.read_groups_from_database()
        List_Of_Groups_Members = [] 

        for Group in List_Of_Groups:

            id, wallet1, wallet2, wallet3, winner, uniqeid_group, status = Group
            List_Of_Groups_Members.append(wallet1)
            List_Of_Groups_Members.append(wallet2)
            List_Of_Groups_Members.append(wallet3)

        if wallet not in List_Of_Groups_Members:
            return True
        
        else:
            return False

    except:
        return False

def Check_User(user, TokenID):
    '''This function check user address and user nft to validate user'''

    contract = CONFIG.CONTRACT_ADDRESS
    apikey = CONFIG.APIKEY
    baseurl = CONFIG.APIURL
    
    query = f"?module=account&action=addresstokennftinventory&address={user}&contractaddress={contract}&page=1&offset=100&apikey={apikey}"

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