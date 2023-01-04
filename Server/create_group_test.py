import requests

base_url = "http://127.0.0.1:80"
TokenID = "7926"  
user = "0xBe1db1dc16341f7eD608753D94583c458fF4098F"

def create_group(base_url,user,TokenID):
    print("[+] Test (Create user) start.")
    route = "/create_group"
    aa = {'wallet':user , 'nftid':TokenID}
    print(f"[+] Test (Create user) with user : {user}.")
    r = requests.post(url = base_url+route, json=aa)
    print(f"[+] response : {r.text}")
    print("[+] Test (Create user) done.")

create_group(base_url,user,TokenID)