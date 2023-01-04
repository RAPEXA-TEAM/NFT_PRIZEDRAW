import requests

base_url = "http://127.0.0.1:80"
TokenID = "7926"  
user = "0xBe1db1dc16341f7eD608753D94583c458fF4098F"
uniqeid = "079caaa44f001cd414a6e6aa1c7e7c186ddb30c1a3cbd509925de6c97f8d4087"

def create_group(base_url,user,TokenID):
    print("[+] Test (Create user) start.")
    route = "/add_to_group"
    aa = {'wallet' : user, 'nftid' : TokenID, 'uniqeid' : uniqeid}
    print(f"[+] Test (Create user) with user : {user}.")
    r = requests.post(url = base_url+route, json=aa)
    print(f"[+] response : {r.text}")
    print("[+] Test (Create user) done.")

create_group(base_url,user,TokenID)