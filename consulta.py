import pandas as pd
import numpy as np
import schedule as sc
import yfinance as yf
import time as tm
from datetime import datetime, timedelta
pd.options.mode.chained_assignment = None  # default='warn'

def tarefa():
    cripto = 'SOL-USD'

    column = "Adj Close"

    now = datetime.today()

    ontem = now - timedelta(days=1)

    amanha = now + timedelta(days=1)

    data = yf.download(cripto, start=ontem, end=amanha, interval="1m")[[column]]

    window = 14

    data['Variation'] = data[column].diff()
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

    # Plot price data
    valorAtual = data.iloc[-1][column]
    print("Valor Atual")
    print(valorAtual)
    # Plot RSI

    valorRSI = RSI.iloc[-1]
    print("Valor RSI")
    print(valorRSI)

sc.every().second.do(tarefa)

while True:
    sc.run_pending()
    tm.sleep(1)