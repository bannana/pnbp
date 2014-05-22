#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  
'  Paul Longtine - paullongtine@gmail.com
'
'''
import os, shutil, mod, json

def main():
    site = {}
    
    #Loops through defined "sites"
    for name,v in pagedata.items():
        try:
            template = open(v['template']).read()
        except:
            print("Can't open file '{}'".format(v['template']))

        template = generateTemplate(template,v['pagevar'],name)

        site[name] = runMod(template,v['pagemod'],name)
    
    buildSite(site)

# Adds in variables defined in pages.json
#
# t = raw template, var = "pagevar" variables in pages.json (<pagename> -> "pagevar")
def generateTemplate(t,var,page):
    if page == "index":
        page = ""

    t = t.replace("%page%",page)
    
    t = runInlineScript(t,page)
    
    for search,replace in var.items():
        if search[0] == ":":
            try:
                inc = open(replace).read()
                inc = inc.replace("%page%", page)
                for subsearch,subreplace in var.items():
                    inc = inc.replace("%"+subsearch+"%",subreplace)

                t = t.replace("%"+search+"%",inc)

            except:
                print("Can't open file '{}'".format(replace))

        else:
            t = t.replace("%"+search+"%",replace)

    return t

# Runs modules defined in pages.json
#
# t = raw template, var = "pagemod" variables in pages.json (<pagename> -> "pagemod")
def runMod(t,var,page):
    subpage = {}
    for name, mdata in var.items():
        subpage.update(getattr(mod,mdata['mod']).getPages(t,mdata['settings'],name,page))

    return subpage

def runInlineScript(template,page):
    try:
        index = template.index("{:")+2
        exists = True
    except:
        exists = False

    if exists:
        script = ""
        while template[index:index+2] != ":}":
            script = script + template[index]
            index += 1
        returns = ""
        exec script
        template = template.replace(template[template.index("{:"):template.index(":}")+2],returns)
    
    return template

# Builds the site off of a filestructure dictionary.

def buildSite(site):
    try:
        shutil.rmtree("./site/")
    except:
        print("No directory site/, ignoring")

    os.mkdir("./site/")
    for page, subpages in site.items():
        if page == "index":
            currentDir = "./site"
        else:
            currentDir = "./site/"+page
            os.mkdir(currentDir)

        open(currentDir+"/index.html", "w").write(subpages['default'])

        for subdir, data in subpages.items():
            if subdir != "default":
                os.mkdir(currentDir+"/"+subdir)
                for page, content in data.items():
                    if page != "default":
                        os.mkdir(currentDir+"/"+subdir+"/"+page)
                        open(currentDir+"/"+subdir+"/"+page+"/index.html","w").write(content)
                    else:
                        open(currentDir+"/"+subdir+"/index.html", "w").write(data['default'])
        copytree("data/styles","site/styles")
        copytree("data/images","site/images")
        
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)

if __name__ == "__main__":
    print("Going through pages...")
    try:
        pages = open("pages.json")
    except:
        print("Can't open file 'pages.json'")        
    pagedata = json.load(pages)
    pages.close()
    main()
    print("Finished.")
