import hashlib
import random
import string
import sys
from getpass import getpass

import mysql.connector
from rich import print as printc
from rich.console import Console

def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def dbconfig():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='pm',
            passwd='StrongPassword123!'
        )
        return db
    except Exception as e:
        printc("[red][!] An error occurred while trying to connect to MySQL.")
        raise

def config():
    db = dbconfig()
    cursor = db.cursor()

    # Check if database exists, create if it doesn't
    cursor.execute("SHOW DATABASES")
    if 'pm' not in [x[0] for x in cursor]:
        try:
            cursor.execute("CREATE DATABASE pm")
            printc("[green][+][/green] Database 'pm' created")
        except Exception as e:
            printc("[red][!] An error occurred while trying to create db.")
            console.print_exception()
            sys.exit(0)

    # Create Tables
    cursor.execute("CREATE TABLE IF NOT EXISTS pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)")
    printc("[green][+][/green] Table 'secrets' created")

    cursor.execute("CREATE TABLE IF NOT EXISTS pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)")
    printc("[green][+][/green] Table 'entries' created")

    while True:
        mp = getpass("Choose a MASTER PASSWORD: ")
        if mp == getpass("Re-type: "):
            break
        else:
            printc("[yellow][+] Passwords do not match. Please try again.[/yellow]")

    # Hash the Master Password
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")

    # Generate a DEVICE SECRET
    ds = generateDeviceSecret()

    # Add them to the Database
    query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) VALUES (%s, %s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Added to the database")
    printc("[green][+][/green] Configuration done!")
    db.close()

if __name__ == "__main__":
    console = Console()
    config()
