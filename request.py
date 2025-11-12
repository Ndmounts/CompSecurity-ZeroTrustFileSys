import json
import os 
import fs
import auth


def whitelistCheck(filename,permissions):
    user_from_cert()
    try:
        with open("whitelist.json", "r") as whitelist:
            if user in json.load(whitelist)[filename][permissions]:
                return 1
            else:
                return 0
    except:
        print("whitelist failed to load")
        return -1
    
def view_request(filename):
    perm =  whitelistCheck(filename,"read",enc)
    if perm == 0:
            print("you are not authorized to read " + filename)
    if perm == 1:
        return(fs_read(filename,enc))

def write_request(filename,data):
    perm = whitelistCheck(user,filename,"write",enc)
    if perm == 0:
        print("you are not authorized to write to " + filename)
    if perm == 1:
        fs_write(filename,data,enc)

def mkdir_request(filename):
    # perm = whitelistCheck(user,filename,"mkdir")
    # if perm == 0:
    #     print("you are not authorized to write to " + filename)
    # if perm == 1:
        fs_mkdir(filename)

def rm_request(filename):
    perm = whirelistCheck(filename,"rm")
    if perm ==  0:
        print(user + " is not authorized to remove " + filename)
    if perm == 2: 
        fs_rm(filename)

def touch_request(filename):
    perm = whitlistCheck(filename,"touch"):
    if perm == 0:
        print("you are not authorized to creat files")
    if perm == 1:
        add_perm(filename,user,"mod_perm")
        add_perm(filename,user,"write")
        add_perm(filename,user,"read")
        return(make_file(filename))



def add_perm(filename, data, perm):
    with open(whitelist.json, "r",touch) as f:
        whitelist = f.load

    if filename in whitelist:
        if whitelistCheck(filename,"mod_perm"):
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
