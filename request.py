include json
include os 




def whitelistCheck(user,filename):
    try:
        with open("whitelist.json", "r") as whitelist:
            if user in jason.load(whitelist)[filename][read]:
                return 1
            else:
                return 0
    except:
        print("whitelist failed to load")
        return -1
    
def view_request(user,filename):
    perm =  whitelistCheck(user,filename)
    if perm == 0:
            print(user + " is not authorized to read " + filename)
    if perm == 1:
        fs_read(filename)

def write_request(user,filename):
    perm = whitelistCheck(user,filename,data)
    if perm == 0:
        print(user + " is not authorized to write to " + filename)
    if perm == 1:
        fs_write(filename,data)



