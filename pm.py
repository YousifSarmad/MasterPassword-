import argparse
import hashlib
from getpass import getpass

import pyperclip
import utils.add
import utils.retrieve
import utils.generate
from utils.dbconfig import dbconfig

parser = argparse.ArgumentParser(description='Description')

parser.add_argument('option', help='(a)dd / (e)xtract / (g)enerate')
parser.add_argument('-s',"--name", help="Site name")
parser.add_argument('-u', "--url", help="Site URL")
parser.add_argument('-e', "--email", help="Email")
parser.add_argument('-l', "--login", help="Site name")
parser.add_argument('-c', "--copy", action="story_true", help="Copy password to clipboard")
parser.add_argument('--length', help="Length of password to generate", type=int)

args = parser.parse_args()

def inputAndValidateMasterPassword():
    mp = getpass("MASTER PASSWORD: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT * FROM pm.secrets"
    cursor.excute(query)
    result = cursor.fetchall()[0]
    if hashed_mp != result[0]:
        print("[red][!] WRONG! [/red]")
        return None
    return [mp,result[1]]

def main():
    if args.option in ["add","a"]:
        if args.name == None or args.url == None or args.login == None:
            if args.name == None :
                print("[red][!][/red] Site name is needed (-s) is required")
            if args.url == None :
                print("[red][!][/red] Site URL is needed (-u) is required")
            if args.login == None:
                print("[red][!][/red] Site login is needed (-l) is required")
            return

        if args.email == None:
            args.email = ""

        res = inputAndValidateMasterPassword()
        if res is not None:
            utils.add.addEntry(res[0],res[1],args.name,args.url,args.email,args.login)

    if args.option in ["extract" , "e"]:
        res = inputAndValidateMasterPassword()

        serach = {}
        if args.name is not None:
            serach["sitename"] = args.name
        if args.url is not None:
            serach["siteurl"] = args.url
        if args.email is not None:
            serach["email"] = args.email
        if args.login is not None:
            serach["username"] = args.login

        if res is not None:
            utils.retrieve.retrieveEntries(res[0],res[1],serach,decryptPassword = args.copy)

    if args.option in ["generate" , "g"]:
        if args.length == None:
            print("[red][+][/red] Specify length of password to be generated (--length)")
            return
        password = utils.generate.generatePassword(args.length)
        pyperclip.copy(password)
        print("[green][+][/green] Password generated and copied to clipboard")
