import requests

base_url = "http://127.0.0.1:80"
user = "0xBe1db1dc16341f7eD608753D94583c458fF4098F"

def create_user(base_url,user,):
    print("[+] Test (tokens user) start.")
    route = "/tokens"
    print(f"[+] Test (tokens user) with user : {user}.")
    r = requests.get(url=base_url)
    print(f"[+] response : {r}")
    print("[+] Test (tokens user) done.")

create_user(base_url,user)