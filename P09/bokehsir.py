import numpy as np
from scipy.integrate import odeint
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import row,column
from bokeh.models import Slider,Div,ColumnDataSource
from bokeh.io import curdoc

N=1000
R0=0
I0=3
S0=N-I0-R0
y0=S0,I0,R0
tmax=200
t=np.linspace(0,tmax,tmax+1)
b=0.4
g=0.04

def SIR(y,t,b,N,g):
    S,I,R=y
    dS=-(b*I*S)/N
    dI=(b*I*S)/N-g*I
    dR=g*I
    return dS,dI,dR

y=odeint(SIR,y0,t,(b,N,g))
df=pd.DataFrame({"t":t,"S":y[:,0],"I":y[:,1],"R":y[:,2]})
data=ColumnDataSource(df)

fig=figure(x_axis_label="t",y_axis_label="N",width=1000,aspect_ratio=1.9)
sl=fig.line("t","S",color="blue",line_width=2,source=data,legend_label="S(t)")
il=fig.line("t","I",color="red",line_width=2,source=data,legend_label="I(t)")
rl=fig.line("t","R",color="green",line_width=2,source=data,legend_label="R(t)")
fig.title.text="SIR model"
fig.title.align="center"
fig.toolbar.logo=None
fig.toolbar.autohide=True
fig.border_fill_color="white"
fig.background_fill_color="white"
gs=Slider(start=0,end=1,step=0.01,value=g,title="Gamma",bar_color='gold',background='white')
bs=Slider(start=0,end=1,step=0.01,value=b,title="Beta",bar_color='purple',background='white')
desc=Div(text=r"""
<h1>SIR model</h1>
<h2>
System of ODEs:
<p></p>
$$
\begin{equation*}
    \begin{dcases}
        \frac{dS}{dt}=-\frac{\beta IS}{N}\\\\
        \frac{dI}{dt}=\frac{\beta IS}{N}-\gamma I\\\\
        \frac{dR}{dt}=\gamma I
    \end{dcases}
\end{equation*}
$$
<p></p>
Initial condition:
<p></p>
$$S(0)+I(0)+R(0)=N=const$$
</h2>
""")

def updateg(attr,old,new):
    g=gs.value
    b=bs.value
    y=odeint(SIR,y0,t,(b,N,g))
    df=pd.DataFrame({"t":t,"S":y[:,0],"I":y[:,1],"R":y[:,2]})
    sl.data_source.data=df
    il.data_source.data=df
    rl.data_source.data=df

def updateb(attr,old,new):
    b=bs.value
    g=gs.value
    y=odeint(SIR,y0,t,(b,N,g))
    df=pd.DataFrame({"t":t,"S":y[:,0],"I":y[:,1],"R":y[:,2]})
    sl.data_source.data=df
    il.data_source.data=df
    rl.data_source.data=df

bs.on_change("value",updateb)
gs.on_change("value",updateg)

curdoc().add_root(row(fig,column(gs,bs,desc,width=400)))