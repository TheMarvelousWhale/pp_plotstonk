import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

st.title("Mad Stonk")

ticker = st.text_input("Input Ticker: ","SPY")
period = st.text_input("Duration (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)","10y")
data = yf.Ticker(ticker).history(period=period)

fig, axs = plt.subplots(3,2,sharey=True)
fig.tight_layout()
cols = ["Open","High","Low","Close"]
numBins= 20

gs = fig.add_gridspec(3,2)
cells=[[0]*len(cols),[0]*len(cols)]
for i,colName in enumerate(cols):
    #plot the subplot
    ax =axs[i//2,i%2] 
    ax.hist(data[colName],bins=numBins)
    ax.set_title(colName)
    #cal mean and std
    cells[0][i] = data[colName].mean()
    cells[1][i] = data[colName].std()
axs[2,0].axis('off')
axs[2,1].axis('off')
tabAx = fig.add_subplot(gs[2,:])
tabAx.axis('tight')
tabAx.axis('off')
tabAx.table(cellText=cells,rowLabels=["mean","std"],colLabels=cols,loc='bottom')

st.pyplot(fig)