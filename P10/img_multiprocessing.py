import requests
from bs4 import BeautifulSoup
import time
import re
import os
from concurrent.futures import ProcessPoolExecutor
from PIL import Image,ImageFilter

def process_image(n):
    for i in range(n):
        with open("img/"+imgs[i],"wb") as handle:
            handle.write(requests.get(url+imgs[i]).content)
            img=Image.open("img/"+imgs[i])
            img=img.convert("L")
            img=img.filter(ImageFilter.GaussianBlur(radius=5))
            img.save("img/"+imgs[i])

if __name__=='__main__':
    url="http://www.if.pw.edu.pl/~mrow/dyd/wdprir/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html.parser")
    imgs=[]
    for a in soup.find_all("a",href=True):
        if re.findall(r"\.png$",a["href"]):
            imgs.append(a["href"])
    if not os.path.exists("img"):
        os.makedirs("img")
    print("Beginning the first test with serial processing")
    s0=time.time()
    process_image(10)
    e0=time.time()
    print("The first test has concluded, proceeding to the second test with parallel processing")
    s1=time.time()
    with ProcessPoolExecutor(10) as ex:
        for i in range(10):
            ex.submit(process_image,i)
    e1=time.time()
    print("The second test has concluded, the results are:")
    print("Serial processing:   %4f sec"%(e0-s0))
    print("Parallel processing: %4f sec"%(e1-s1))