import json
import os 
import filesystem
import auth


def whitelistCheck(filename,permissions):
    user = auth.user_from_cert()
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
    perm =  whitelistCheck(filename,"read")
    if perm == 0:
            print("you are not authorized to read " + filename)
    if perm == 1:
        return(filesystem.fs_read(filename,enc))

def write_request(filename,data,enc):
    perm = whitelistCheck(filename,"write")
    if perm == 0:
        print("you are not authorized to write to " + filename)
    if perm == 1:
        filesystem.fs_write(filename,data,enc)

def mkdir_request(filename):
    # perm = whitelistCheck(user,filename,"mkdir")
    # if perm == 0:
    #     print("you are not authorized to write to " + filename)
    # if perm == 1:
        filesystem.fs_mkdir(filename)

def rm_request(filename):
    perm = whitelistCheck(filename,"rm")
    if perm ==  0:
        print("you are not authorized to remove " + filename)
    if perm == 1:
        filesystem.fs_delete(filename)

def touch_request(filename,data):
    #perm = whitelistCheck(filename,"touch")    #decided against limiting file creation
    # if perm == 0:
    #     print("you are not authorized to creat files")
    perm = 1        #patch so we can roll back without dificulty
    user = auth.user_from_cert()
    if perm == 1:
        add_perm(filename,user,"mod_perm")
        add_perm(filename,user,"write")
        add_perm(filename,user,"read")
        add_perm(filename,user,"rm")
        return(filesystem.create_file(filename,data))


def add_perm(filename, data, perm):
    with open("whitelist.json", "r") as f:
        whitelist = json.load(f)

    if filename in whitelist:
        if (whitelistCheck(filename,"mod_perm") == 1):
            whitelist[filename].setdefault(perm, [])
            if data not in whitelist[filename][perm]:
                whitelist[filename][perm].append(data)
            with open("whitelist.json","w") as f:
                json.dump(whitelist, f, indent=4)
        else:
             print("you do not have permission to modify " + filename + "'s permissions")
    else:
        whitelist[filename] = {
            "read": [],
            "write": [],
            "mod_perm": [],
            "rm" : []
        }
        whitelist[filename][perm].append(data)
        with open("whitelist.json", "w") as f:
            json.dump(whitelist, f, indent=4)
