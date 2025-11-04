include json
include os 




def whitelistCheck(user,filename,permissions):
    try:
        with open("whitelist.json", "r") as whitelist:
            if user in jason.load(whitelist)[filename][permissions]:
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

