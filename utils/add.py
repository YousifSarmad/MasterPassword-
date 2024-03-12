from getpass import getpass
from crypto.Protocol.KDF import PBKDF2
from crypto.Hash import SHA512
from crypto.Random import get_random_bytes

import utils.aesutil
from utils.dbconfig import dbconfig


def computeMasterKey (mp,ds):
    password = mp.encode()
    salt= ds.encode()
    key = PBKDF2(password, salt, 32 , count = 1000000, hmac_hash_module=SHA512)
    return key

def addEntry(mp,ds, sitename,siteurl, email, username):
    # Get the password
    password = getpass("Password: ")

    mk = computeMasterKey(mp, ds)

    encrypted = utils.aesutil.encrypt(key=mk,source=password, keyType="bytes")

    # Add to the Database
    db = dbconfig()
    cursor = db.cursor()
    query = "INSERT INTO pm.entries (sitename, siteurl, email, username, password) values (%s,%s,%s,%s,%s)"
    val = (sitename,siteurl,email,username,encrypted)
    cursor.execute(query,val)
    db.commit()

    print("[green][+][/green] Added entry ")