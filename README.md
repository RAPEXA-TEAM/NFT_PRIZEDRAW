# NFT_PRIZEDRAW
System for run a lottory after minting between buyers 

----

## How to run

1. Install python3, pip3, virtualenv, MySQL in your system.

2. `git clone https://github.com/RAPEXA-TEAM/NFT_PRIZEDRAW.git && cd NFT_PRIZEDRAW/Server`  

3. in the app folder, rename the `CONFIG.py.sample` to `CONFIG.py` and do proper changes.

4. run this comand in MySql Cli :
   
   ```
    CREATE DATABASE prizedraw;
    CREATE USER 'prizedrawuser'@'localhost' IDENTIFIED BY 'prizedrawpass';
    GRANT ALL PRIVILEGES ON prizedraw.* TO 'prizedrawuser'@'localhost';
    USE prizedraw;
    DROP TABLE users;
    CREATE TABLE users (id INT NOT NULL AUTO_INCREMENT, wallet VARCHAR(255) NOT NULL, nft VARCHAR(255) NOT NULL, uniqeid VARCHAR(255) NOT NULL, PRIMARY KEY(id), UNIQUE (id));
    DROP TABLE groupss;
    CREATE TABLE groupss (id INT NOT NULL AUTO_INCREMENT, wallet1 VARCHAR(255) NOT NULL, wallet2 VARCHAR(255) NOT NULL, wallet3 VARCHAR(255) NOT NULL, winner VARCHAR(255) NOT NULL, uniqeid VARCHAR(255) NOT NULL, status VARCHAR(255) NOT NULL, PRIMARY KEY(id), UNIQUE (id));
    CREATE TABLE winers (id INT NOT NULL AUTO_INCREMENT, winner VARCHAR(255) NOT NULL, payment VARCHAR(255) NOT NULL, PRIMARY KEY(id), UNIQUE (id));
   ```

9. Create a virtualenve named build using `virtualenv -p python3 venv`

10. Connect to virtualenv using `source venv/bin/activate`

11. From the project folder, install packages using `pip3 install -r ./app/requirements.txt`

12. Now environment is ready. Run it by `python Server.py`