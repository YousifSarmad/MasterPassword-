import pyperclip
from rich import Console
from rich.table import Table

from crypto.Protocol.KDF import PBKDF2
from crypto.Hash import SHA512
from crypto.Random import get_random_bytes

from utils.dbconfig import dbconfig

import utils.aesutil


def computeMasterKey (mp,ds):
    password = mp.encode()
    salt= ds.encode()
    key = PBKDF2(password, salt, 32 , count = 1000000, hmac_hash_module=SHA512)
    return key

def retrieveEntries (mp,ds,search, decrptyPassword = False):
    db = dbconfig()
    cursor = db.cursor()

    query = ""

    if len(search) == 0:
        query = "SELECT * FROMM pm.entries"
    else:
        query = "SELECT * FROM pm.entries WHERE "
        for i in search:
            query += f"{i} = '{search[i]}' AND "
        query = query[:-5]

    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == 0:
        print("[yellow][-][/yellow] No results for the search")

    if (decrptyPassword and len(results) > 1) or (not decrptyPassword):
        table = Table(title="Results")
        table.add_column("Site Name")
        table.add_column("URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")

        for i in results:
            table.add_row(i[0],i[1],i[2],i[3], "{hidden}")

        console = Console()
        console.print(table)

        return

    if len(results) ==1 and decrptyPassword:
        mk = computeMasterKey(mp, ds)
        decrpyted = utils.aesutil.decrypt(key = mk, source=results[0][4], keyType="bytes")

        pyperclip.copy(decrpyted.decode())
        print("[green][+][/green] Password copied to clipboard")

    db.close()
