import requests
import json
from bs4 import BeautifulSoup
import argparse

parser=argparse.ArgumentParser(prog='static.py',description='Scrape table containing skills from the game "Sekiro: Shadows Die Twice".')
parser.add_argument('-f','--filename',action='store',default='data',help='name of the file to save the table to (default: "data")')
args=parser.parse_args()
filename=args.filename+".json"

res=requests.get("https://sekiroshadowsdietwice.wiki.fextralife.com/Skills+and+Skill+Trees")
soup=BeautifulSoup(res.text,"html.parser")
table_div=soup.find("div",class_="table-responsive")
data=table_div.select("table tbody tr td")
counter=0
name=[]
tree=[]
desc=[]
points=[]
req=[]
for d in data:
    if counter%5==0:
        name.append(d.text.strip())
    elif counter%5==1:
        tree.append(d.text.strip())
    elif counter%5==2:
        desc.append(d.text.strip())
    elif counter%5==3:
        points.append(d.text.strip())
    elif counter%5==4:
        req.append(d.text.strip())
    counter+=1
        
assert len(name)==len(tree)==len(desc)==len(points)==len(req)

table=list(zip(name,tree,desc,points,req))
with open("COPIUM2/PWZN/P5/"+filename,"w") as f:
    json.dump(table,f,indent=4)