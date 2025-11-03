include json
include os 


def view_request(user,whitelist,filename): #checks user authority
    bool perm = 0 #bool for permissions 
   
   try:
        with open("whitelist.json", "r") as whitelist:
            if user in jason.load(whitelist)[filename][read]:
                perm = 1
            else:
                print(user + " is not authorized to read " + filename)
    except:
        print("whitelist failed to load")
    
    if perm == 1:
        fs_read(filename)


