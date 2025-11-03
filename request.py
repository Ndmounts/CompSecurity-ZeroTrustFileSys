
include os 


def view_request(user,whitelist,filename): #checks user authority
    if user in whitelist.filename:
        with open(filename,r):
            for line in file:
                print line
        
