import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
pd.options.mode.chained_assignment = None  # default='warn'


def plot_RSI(data, column, window=14, limit_up=70.0, limit_down=30.0):    

    now = datetime.today()

    data['Variation'] = stock[column].diff()
    data = data[1:]
    
    data['Gain'] = np.where(data['Variation'] > 0, data['Variation'], 0) 
    data['Loss'] = np.where(data['Variation'] < 0, data['Variation'], 0) 

    simple_avg_gain = data['Gain'].rolling(window).mean()
    simple_avg_loss = data['Loss'].abs().rolling(window).mean()

    # start off of simple average series
    classic_avg_gain = simple_avg_gain.copy()
    classic_avg_loss = simple_avg_loss.copy()

    # iterate over the new series but only change values after the nth element
    for i in range(window, len(classic_avg_gain)):
        classic_avg_gain.iloc[i] = (classic_avg_gain.iloc[i - 1] * (window - 1) + data['Gain'].iloc[i]) / window
        classic_avg_loss.iloc[i] = (classic_avg_loss.iloc[i - 1] * (window - 1) + data['Loss'].abs().iloc[i]) / window

    RS = classic_avg_gain / classic_avg_loss
    RSI = 100 - (100 / (1 + RS))

    fig, (ax1, ax2) = plt.subplots(
        nrows=2, 
        sharex=True, 
        figsize=(12,8), 
        gridspec_kw={'height_ratios': [3, 1]})

    # Plot price data
    ax1.plot(data.index, data[column], linewidth=3, label="Variação")
    valorAtual = data.iloc[-1][column]
    ax1.text(data.index._data[-1],valorAtual,valorAtual)       
    ax1.legend()

    # Plot RSI
    ax2.plot(data.index, RSI, color="#033660", label="RSI")
    valorRSI = RSI.iloc[-1]
    ax2.text(data.index._data[-1],valorRSI, valorRSI)
    ax2.axhline(y=limit_down, color='white', linestyle='--')
    ax2.axhline(y=limit_up, color='white', linestyle='--')
    ax2.axhspan(limit_down, limit_up, color='indigo', alpha=0.2)
    ax2.set_ylim(0, 100)
    ax2.legend()
    plt.show()

cripto = 'SOL-USD'

column_dashboard = "Adj Close"

now = datetime.today()

ontem = now - timedelta(days=2)

amanha = now + timedelta(days=1)

stock = yf.download(cripto, start=ontem, end=amanha, interval="1m")[[column_dashboard]]

plot_RSI(data=stock, column=column_dashboard, window=9, limit_up=70, limit_down=30)

