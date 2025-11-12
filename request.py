import json
import os 
import fs.py
import auth.py


def whitelistCheck(user,filename,permissions):
    try:
        with open("whitelist.json", "r") as whitelist:
            if user in json.load(whitelist)[filename][permissions]:
                return 1
            else:
                return 0
    except:
        print("whitelist failed to load")
        return -1
    
def view_request(user,filename):
    perm =  whitelistCheck(user,filename,"read")
    if perm == 0:
            print(user + " is not authorized to read " + filename)
    if perm == 1:
        fs_read(filename)

def write_request(user,filename,data):
    perm = whitelistCheck(user,filename,"write")
    if perm == 0:
        print(user + " is not authorized to write to " + filename)
    if perm == 1:
        fs_write(filename,data)

def mkdir_request(user,filename):
    perm = whitelistCheck(user,filename,"mkdir")
    if perm == 0:
        print(user + " is not authorized to write to " + filename)
    if perm == 1:
        fs_mkdir(filename)

def rm_request(user,filename):
    perm = whirelistCheck(user,filename,"rm")
    if perm ==  0:
        print(user + " is not authorized to remove " + filename)
    if perm == 2: 
        fs_rm(filename)

def touch_request(user, filename):
    perm = whitlistCheck(user, filename,"touch"):
    if perm == 0:
        print(user, "is not authorized to creat files in " + files.rsplit('/', 1)[0])
    if perm == 1:
        make_file(user, filename)
        add_perm(user,filename,user,"mod_perm")
        add_perm(user,filename,user,"write")
        add_perm(user,filename,user,"read")


def add_perm(user, filename, data, perm):
    with open(whitelist.json, "r") as f:
        whitelist = f.load

    if filename in whitelist:
        if whitelistCheck(user,filename,"mod_perm"):
            whitelist[filename].setdefault(perm, [])
            if user not in whitelist[filename][perm]:
                whitelist[filename][perm].append(user)
            with open(whitelist.json,w) f:
                json.dump(whitelist, f, indent=4)
        else:
             print(user + " dose not have permission to modify " + filename "'s permissions")
    else:
        whitelist[filename] = {
            "read": {},
            "write": {},
            "mod_perm": {}
        }
        whitelist[filename][perm].append(user)
    with open("whitelist.json", "w") as f:
        json.dump(whitelist, f, indent=4)