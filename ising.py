import argparse
from tqdm import tqdm
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

parser=argparse.ArgumentParser(prog='ising.py',description='Simulate and visualize Ising model on a toroidal N x M grid.')
parser.add_argument('-nm','--grid-dimensions',action='store',metavar=('N','M'),nargs=2,default=[100,100],type=int,help='lengths of the sides of N x M grid (should be bigger than the default value of 100)')
parser.add_argument('-j','--interaction-constant',action='store',default=1,type=int,help='constant J describing interaction between neighboring spins, J>0 - ferromagnetic, J<0 - antiferromagnetic, J=0 - no interaction (default: 1)')
parser.add_argument('-b','--beta',action='store',default=1,type=int,help='constant b related to temperature T through the equation b=1/(kT), where k is a Boltzmann constant (default: 1)')
parser.add_argument('-bt','--magnetic-induction',action='store',default=0,type=int,help='value of magnetic induction of external field in [T] (default: 0)')
parser.add_argument('-s','--steps',action='store',default=50,type=int,help='number of steps to simulate (default: 50)')
parser.add_argument('-d','--spin-density',action='store',default=0.5,type=float,help='starting density of positive direction spins (default: 0.5)')
parser.add_argument('-dir','--directory',action='store',default='ising_data',help='name of the directory with the output files, if not provided, output goes to default directory (default: \'ising_data\')')
parser.add_argument('-pf','--pictures-filename',action='store',default='',help='prefix for pictures generated for every step of simulation, if not provided, script does not generate pictures (default: none)')
parser.add_argument('-af','--animation-filename',action='store',default='',help='name of the file containing animation of every step of simulation, if not provided, script does not generate animation (default: none)')
parser.add_argument('-mf','--magnetisation-filename',action='store',default='',help='name of the file containing magnetisation values for every step of simulation, if not provided, script does not generate this file (default: none)')
args=parser.parse_args()

class Ising():
    def __init__(self):
        self.n,self.m=args.grid_dimensions
        self.j=args.interaction_constant
        self.b=args.beta
        self.bt=args.magnetic_induction
        self.s=args.steps
        self.d=args.spin_density
        self.dir=args.directory
        self.pf=args.pictures_filename
        self.af=args.animation_filename
        self.mf=args.magnetisation_filename+'.txt'
        self.grid=np.ones(shape=(self.n,self.m),dtype=int)
        for i in range(self.n):
            for j in range(self.m):
                if self.d<np.random.rand(1):
                    self.grid[i][j]=-self.grid[i][j]
        self.pfdir='pictures'
        if (self.pf!='' or self.af!='' or self.mf!='') and not os.path.exists(os.getcwd()+'\\'+self.dir):
            os.makedirs(self.dir)
        if os.path.exists(os.getcwd()+'\\'+self.dir):
            os.chdir(self.dir)
        if self.pf!='' and not os.path.exists(os.getcwd()+'\\'+self.pfdir):
            os.makedirs(self.pfdir)
        self.Simulate()
    def Simulate(self):
        fig,ax=plt.subplots()
        if self.pf!='':
            img=ax.imshow(self.grid)
            fig.colorbar(img,ax=ax)
            fig.suptitle('t=0',fontsize=20)
            fig.savefig(self.pfdir+'/'+self.pf+'000.jpg')
        if self.af!='':
            self.anim_data=[]
            self.anim_data.append(self.grid.copy())
        if self.mf!='':
            file=open(self.mf,'w')
            file.write(f'{0:3} {np.sum(self.grid)/(self.n*self.m):10}\n')
        self.bar=tqdm(total=self.s*self.n*self.m,file=sys.stdout)
        t=0
        for state in self.Iterate():
            if self.pf!='':
                img.set_data(state)
                fig.suptitle(f't={t+1}',fontsize=20)
                fig.savefig(self.pfdir+'/'+str(self.pf)+str(t+1).zfill(3)+'.jpg')
            if self.af!='':
                self.anim_data.append(state.copy())
            if self.mf!='':
                file=open(self.mf,'a')
                file.write(f'{t+1:3} {np.sum(self.grid)/(self.n*self.m):10}\n')
            t+=1
        if self.af!='':
            writer=PillowWriter(fps=5)
            def update(frame):
                img.set_data(self.anim_data[frame])
                fig.suptitle(f't={frame}',fontsize=20)
                return [img,]
            anim=animation.FuncAnimation(fig,update,interval=200,frames=self.s+1,blit=True)
            anim.save(self.af+'.gif',writer)
    def CalcEnergy(self,i,j,spin):
        if i==0: ii=self.n-1
        else: ii=i-1
        if j==0: jj=self.m-1
        else: jj=j-1
        if i==self.n-1: iii=0
        else: iii=i+1
        if j==self.m-1: jjj=0
        else: jjj=j+1
        return -self.j*spin*(self.grid[ii][j]+self.grid[iii][j]+self.grid[i][jj]+self.grid[i][jjj])-self.bt*spin
    def Iterate(self):
        l=0
        while l<self.s:
            k=0
            while k<self.n*self.m:
                i=np.random.randint(0,self.n,dtype=int)
                j=np.random.randint(0,self.m,dtype=int)
                E0=self.CalcEnergy(i,j,self.grid[i][j])
                E1=self.CalcEnergy(i,j,-self.grid[i][j])
                dE=E1-E0
                if dE<0:
                    self.grid[i][j]=-self.grid[i][j]
                elif np.random.rand(1)<np.exp(-self.b*dE):
                    self.grid[i][j]=-self.grid[i][j]
                k+=1
                self.bar.update(1)
            yield self.grid
            l+=1

ising=Ising()