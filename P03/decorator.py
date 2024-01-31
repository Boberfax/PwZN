import time
import numpy as np

class NDescriptor:
    def __get__(self,instance,owner):
        return instance._n
    def __set__(self,instance,value):
        if value<0:
            instance._n=1
        else:
            instance._n=value

class Decorator:
    n=NDescriptor()
    def __init__(self,n):
        self._counter=0
        self.n=n
        self._t=[]
    def __call__(self,*args,**kwargs):
        s=time.time()
        _=self._func(*args,**kwargs)
        e=time.time()
        self._t.append(e-s)
        self._counter+=1
        print('Number of test: %d, time of execution: %f sec'%(self._counter,e-s))
    def Wrapper(self,func):
        self._func=func
        print('==================================================')
        print('Loaded function %s'%self._func.__name__)
    def ResetSeries(self):
        self._counter=0
        self._t=[]
        print('==================================================')
        print("Cleared previous results")
    def TestSeries(self,n=0):
        if n>0:
            self.n=n
        print('==================================================')
        print('Starting n=%d tests for function %s'%(self.n,self._func.__name__))
        for _ in range(self.n):
            self()
        print('Tests concluded')
        self.PrintResults()
    def PrintResults(self):
        print('==================================================')
        print('Tested function: %s'%self._func.__name__)
        print('Total number of tests done: %d'%self._counter)
        print('Min: %f sec'%np.min(self._t))
        print('Max: %f sec'%np.max(self._t))
        print('Mean: %f sec'%np.mean(self._t))
        print('Stdev: %f sec'%np.std(self._t))

decorator=Decorator(5)

@decorator.Wrapper
def my_func():
    a=np.random.rand(2000,2000)
    _=np.linalg.eig(a)

decorator.TestSeries()
decorator.ResetSeries()
decorator.TestSeries(3)
decorator.TestSeries(5)