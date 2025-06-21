#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
igfont = {"family":"IPAexGothic"}

st.set_page_config(layout="wide")

A0 = {"Am-Be":[2.34E+06,1.70E+5,dt.datetime(2024,5,31,12,0,0)],
      "Cf":[3.32E+06,3.07E+05,dt.datetime(2024,5,30,12,0,0)]} #A0,eA0,t0
		

par = {"Am-Be":[1.0505, 8.90E-5,157857.67],
       "Cf" :[1.0023, 1.06E-4,966.07]} #f90,sigma,T[days]

h = {"Am-Be":[391,411],
       "Cf" :[385,400]} #h*(10),hp(10)

err = {"Am-Be":[0.0689,0.1055,0.1055],
       "Cf" :[0.072,0.075,0.075]} #h*(10),hp(10)


def calcA(src):
    dt = (t - A0[src][2]).days
    A = A0[src][0] *(0.5)**(dt/par[src][2])
    return A

def calcF(src,L):
    dt = (t - A0[src][2]).days
    A = A0[src][0] *(0.5)**(dt/par[src][2])
    f90,sigma,T = par[src][0],par[src][1],par[src][2]
    F  = A/(4*math.pi*L**2) *f90 * math.e ** (-sigma*L)#math.exp(-sigma * L)
    eF = F * err[src][0]
    return F,eF

def calcH0(src,L):
    dt = (t - A0[src][2]).days
    A = A0[src][0] *(0.5)**(dt/par[src][2])
    f90,sigma,T = par[src][0],par[src][1],par[src][2]
    F  = A/(4*math.pi*L**2) *f90 * math.e ** (-sigma*L)#math.exp(-sigma * L)
    H  = F*h[src][0]*3600/1E+6
    eH = H * err[src][1]
    return H,eH

def calcH1(src,L):
    dt = (t - A0[src][2]).days
    A = A0[src][0] *(0.5)**(dt/par[src][2])
    f90,sigma,T = par[src][0],par[src][1],par[src][2]
    F  = A/(4*math.pi*L**2) *f90 * math.e ** (-sigma*L)#math.exp(-sigma * L)
    H  = F*h[src][1]*3600/1E+6
    eH = H * err[src][1]
    return H,eH

Lmin,Lmax = 50,450
L  = np.arange(Lmin,Lmax+10,10)


st.title("**RI(241Am-Be,252Cf)速中性子場　基準量の計算**")
col1,col2 = st.columns(2)

#st.write(A0["Am-Be"][0])

src = "Am-Be"
src = "Cf"



with col1:
    st.markdown("速中性子場の基準フルエンスを計算します。基準量を計算したい日と照射距離を入力してください。")
    st.latex(r'''
        \begin{equation*}
            \phi = \frac{A}{4\pi D^{2}} \cdot F_{90} \cdot \exp{(-\Sigma l)}
         \end{equation*}
    ''')
    
    t_ = st.date_input('基準算定日', dt.datetime.today())
    t = dt.datetime(t_.year,t_.month,t_.day,12,0,0)

    L0 = st.number_input("距離 (cm) :50cm～450cm", value=100)
    #A = st.number_input("中性子放出率(s-1) ", value=calcA(src))
    st.divider()

    src = "Am-Be"
    #st.markdown("**$^{241}$Am-Be 速中性子場**")
    st.markdown("##### $^{241}$Am-Be 速中性子場 （%s時点）"%t.strftime("%Y-%m-%d"))
    A = calcA(src)
    F,eF = calcF(src,L0)
    H0,eH0 = calcH0(src,L0)
    H1,eH1 = calcH1(src,L0)
    st.markdown("中性子放出率 $A$ (s-1)")
    st.code("%.2e" %A,"html")
    st.markdown("フルエンス率 $\phi$ (s-1 cm-2) @%icm" %L0)
    st.code("%.2e" %F,"html")
    st.markdown("周辺線量当量率 $H^{*}(10)$ ($\mu$Sv/h) @%icm" %L0)
    st.code("%.2e" %H0,"html")
    st.markdown("個人線量当量率 $H_{p}(10)$ ($\mu$Sv/h) @%icm" %L0)
    st.code("%.2e" %H1,"html")

    st.divider()
    src = "Cf"
    #.markdown("**$^{252}$Cf 速中性子場**")
    st.markdown("##### $^{252}$Cf 速中性子場 （%s時点）"%t.strftime("%Y-%m-%d"))
    A = calcA(src)
    F,eF = calcF(src,L0)
    H0,eH0 = calcH0(src,L0)
    H1,eH1 = calcH1(src,L0)
    st.markdown("中性子放出率 $A$ (s-1)")
    st.code("%.2e" %A,"html")
    st.markdown("フルエンス率 $\phi$ (s-1 cm-2) @%icm" %L0)
    st.code("%.2e" %F,"html")
    st.markdown("周辺線量当量率 $H^{*}(10)$ ($\mu$Sv/h) @%icm" %L0)
    st.code("%.2e" %H0,"html")
    st.markdown("個人線量当量率 $H_{p}(10)$ ($\mu$Sv/h) @%icm" %L0)
    st.code("%.2e" %H1,"html")

with col2:
    #st.markdown("HELLO")
    L = np.linspace(50,500,450)
    #y = P = A/4/math.pi/x**2 * f90 * np.exp(-att * x)
    
    #フルエンスプロット
    fig= plt.figure(figsize=(8,8),dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    plt.rc('font',**igfont) 

    src = "Am-Be"
    F,eF = calcF(src,L)  
    plt.plot(L,F,c="blue",label=src)
    plt.fill_between(L,F-eF,F+eF,facecolor='b',alpha=0.2)
    plt.annotate("%.1f s$^{-1}$cm$^{-2}$ @100cm"%calcF(src,100)[0], xy = (100, calcF(src,100)[0]),
             xytext = (100*0.6, calcF(src,100)[0]*0.5), fontsize = 8, color = "black", 
             arrowprops=dict(edgecolor='black', arrowstyle = '-'))   
    
    src = "Cf"
    F,eF = calcF(src,L)  
    plt.plot(L,F,c="red",label=src)
    plt.fill_between(L,F-eF,F+eF,facecolor='red',alpha=0.2)
    plt.annotate("%.1f s$^{-1}$cm$^{-2}$ @100cm"%calcF(src,100)[0], xy = (100, calcF(src,100)[0]),
             xytext = (100*1.0, calcF(src,100)[0]*1.8), fontsize = 8, color = "black", 
             arrowprops=dict(edgecolor='black', arrowstyle = '-'),horizontalalignment="left")

    #ax.set_title("Reference flux available in RI neutron field @%s" %t.strftime('%Y-%m-%d'))
    ax.set_title("中性子フルエンス率 @%s" %t.strftime('%Y-%m-%d'))
    ax.set_xlabel("Distance from source [cm]")
    ax.set_ylabel("Neutron flux [s$^{-1}$cm$^{-2}$]")
    #ax.set_xticks([50,100,200,300,400,500])
    ax.set_xticks([50,100,200,300,400,500])
    plt.legend()
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(which='major',color='gray',linestyle='-',alpha=0.3)
    plt.grid(which='minor',color='gray',linestyle='-',alpha=0.3)

    st.pyplot(fig)

    #周辺線量当量プロット
    fig= plt.figure(figsize=(8,8),dpi=300)
    bx = fig.add_subplot(1, 1, 1)
    plt.grid(which='major',color='gray',linestyle='-',alpha=0.3)
    plt.grid(which='minor',color='gray',linestyle='-',alpha=0.3)

    src = "Am-Be"
    H,eH = calcH0(src,L)  
    plt.plot(L,H,c="blue",label=src)
    plt.fill_between(L,H-eH,H+eH,facecolor='b',alpha=0.2)
    plt.annotate("%.1f $\mu$Sv h$^{-1}$@100cm"%calcH0(src,100)[0], xy = (100, calcH0(src,100)[0]),
                xytext = (100, calcH0(src,100)[0]*0.5), fontsize = 8, color = "black", 
                arrowprops=dict(edgecolor='black', arrowstyle = '-'),horizontalalignment="right")

    src = "Cf"
    H,eH = calcH0(src,L)  
    plt.plot(L,H,c="red",label=src)
    plt.fill_between(L,H-eH,H+eH,facecolor='red',alpha=0.2)
    plt.annotate("%.1f $\mu$Sv h$^{-1}$@100cm"%calcH0(src,100)[0], xy = (100, calcH0(src,100)[0]),
                xytext = (100*1.0, calcH0(src,100)[0]*1.8), fontsize = 8, color = "black", 
                arrowprops=dict(edgecolor='black', arrowstyle = '-'),horizontalalignment="left")

    #plt.xlim(0.8,4.2) #plt.ylim(0,)
    bx.set_title("周辺線量当量率 $H^{*}(10)$ @%s" %t.strftime('%Y-%m-%d'))
    bx.set_xlabel("Distance from source [cm]")
    bx.set_ylabel("H$^{*}$(10),amient dose equivalent rate [$\mu$Sv h$^{-2}$]")
    plt.legend()
    plt.xscale("log")
    plt.yscale("log")
    st.pyplot(fig)
    
    #個人線量当量プロット
    fig= plt.figure(figsize=(8,8),dpi=300)
    bx = fig.add_subplot(1, 1, 1)
    plt.grid(which='major',color='gray',linestyle='-',alpha=0.3)
    plt.grid(which='minor',color='gray',linestyle='-',alpha=0.3)

    src = "Am-Be"
    H,eH = calcH1(src,L)  
    plt.plot(L,H,c="blue",label=src)
    plt.fill_between(L,H-eH,H+eH,facecolor='b',alpha=0.2)
    plt.annotate("%.1f $\mu$Sv h$^{-1}$@100cm"%calcH1(src,100)[0], xy = (100, calcH1(src,100)[0]),
                xytext = (100, calcH1(src,100)[0]*0.5), fontsize = 8, color = "black", 
                arrowprops=dict(edgecolor='black', arrowstyle = '-'),horizontalalignment="right")

    src = "Cf"
    H,eH = calcH1(src,L)  
    plt.plot(L,H,c="red",label=src)
    plt.fill_between(L,H-eH,H+eH,facecolor='red',alpha=0.2)
    plt.annotate("%.1f $\mu$Sv h$^{-1}$@100cm"%calcH1(src,100)[0], xy = (100, calcH1(src,100)[0]),
                xytext = (100*1.0, calcH1(src,100)[0]*1.8), fontsize = 8, color = "black", 
                arrowprops=dict(edgecolor='black', arrowstyle = '-'),horizontalalignment="left")

    #plt.xlim(0.8,4.2) #plt.ylim(0,)
    bx.set_title("個人線量当量率 $H_{p}(10)$ @%s" %t.strftime('%Y-%m-%d'))
    bx.set_xlabel("Distance from source [cm]")
    bx.set_ylabel("H$_{p}$(10),personal dose equivalent rate [$\mu$Sv h$^{-2}$]")
    plt.legend()
    plt.xscale("log")
    plt.yscale("log")

    # cx = bx.twinx()
    # cx.plot(legend=False)
    # cx.set_ylim(bx.get_ylim()[0]*h[src][1]/h[src][0],bx.get_ylim()[1]*h[src][1]/h[src][0])
    # cx.set_xscale('log')
    # cx.set_yscale('log')
    # cx.set_ylabel("H$_{p}$(10),personal dose equivalent rate [$\mu$Sv h$^{-1}$]",rotation=270,verticalalignment="bottom")

    st.pyplot(fig)