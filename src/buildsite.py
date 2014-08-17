'''
'  pnbp - pnbp is not a blogging platform
'  buildsite.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
import os, shutil

# Builds the site off of a filestructure dictionary.
def buildSite(site,loc):
    try:
        shutil.rmtree(loc)

    except:
        print("No directory {}, ignoring".format(loc))

    os.mkdir(loc)
    for page, subpages in site.items():
        if page == "index":
            if loc[-1] == "/":
                currentDir = loc[0:-1]

            else:
                currentDir = loc

        else:
            if loc[-1] == "/":
                currentDir = loc+page

            else:
                currentDir = loc+"/"+page

            try:
                os.mkdir(currentDir)

            except:
                pass
        
        subpageLoop(subpages,currentDir)

    if loc[-1] != "/":
        loc = loc + "/"
    try:
        for i in os.listdir("data/static/"):
            try:
                shutil.copytree("data/static/"+i,loc+i)
                
            except:
                shutil.copy2("data/static/"+i,loc+i)
    except:
        print("No directory data/static, ignoring")

#Recursive loop through all subpages
#d = dict of all subpages, cd = Current directory
def subpageLoop(d,currentDir):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            subpageLoop(v,currentDir + "/" + k)
        else:
            if k == "default":
                k = ""

            else:
                k = k + "/"

            try:
                file("{}/{}index.html".format(currentDir,k), "w").write(v)

            except:
                try:
                    os.mkdir("{}".format(currentDir))

                except:
                    pass

                try:
                    os.mkdir("{}/{}".format(currentDir,k))
                except:
                    pass

                file("{}/{}index.html".format(currentDir,k), "w").write(v)