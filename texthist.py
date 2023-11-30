import argparse
from ascii_graph import Pyasciigraph
from tqdm import tqdm
import time
from collections import defaultdict
import sys
import os

parser=argparse.ArgumentParser(prog='texthist.py',description='Make a histogram from a text file.')
parser.add_argument('-f','--filename',action='store',help='name of the text file (works only if directory is not provided)')
parser.add_argument('-wc','--wordcount',action='store',default=10,type=int,help='number of words to be plotted on histogram (default: 10)')
parser.add_argument('-ml','--minlength',action='store',default=0,type=int,help='minimal length of a word to be analysed (default: 0)')
parser.add_argument('-i','--ignored',action='store',nargs='*',default='',help='list of words to be ignored (default: none)')
parser.add_argument('-ex','--exchar',action='store',nargs='*',default='',help='list of characters that words cannot contain (default: none)')
parser.add_argument('-in','--inchar',action='store',nargs='*',default='',help='list of characters that words must contain (default: none)')
parser.add_argument('-d','--dir',action='store',default='',help='name of the directory that contains text file(s) to be analysed, current working directory must contain this directory (default: none)')
args=parser.parse_args()

if args.dir=='':
    files=[args.filename]
else:
    files=os.listdir(os.getcwd()+'\\'+args.dir)
    os.chdir(args.dir)
d=defaultdict(int)
for file in files:
    f=open(file,'rt')
    size=os.path.getsize(file)
    bar=tqdm(total=size,file=sys.stdout)
    for l in f:
        for w in l.split():
            if len(w)>=args.minlength and w not in args.ignored:
                flage=0
                flagi=0
                if args.exchar!='':
                    for e in args.exchar: 
                        if e not in w: flage+=1
                if args.inchar!='':
                    for i in args.inchar: 
                        if i in w: flagi+=1
                if flage+flagi>=len(args.exchar)+len(args.inchar):
                    d[w]+=1
        if size<100000: time.sleep(0.001)
        bar.update(len(l))
    f.close()
    bar.reset()
    bar.update(size)
    bar.close()
    graph=Pyasciigraph()
    k=0
for line in graph.graph("Word frequency histogram",sorted(d.items(),key=lambda x:x[1],reverse=True)):
    if k<args.wordcount+2: print(line)
    k+=1