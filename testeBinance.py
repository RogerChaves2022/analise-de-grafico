import ccxt
import pandas as pd
import ta
import ta.momentum
import time as tm
import schedule as sc

api_key = ""
private_key = ""

binance = ccxt.binance({'apiKey':api_key, 'secret':
                private_key, 'enableRateLimit': True})

def get_rsi(symbol, interval, period=14):
    ohlcv = binance.fetch_ohlcv(symbol, interval)

    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open','high','low','close','volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')

    df['rsi'] = ta.momentum.RSIIndicator(df['close'],window=period).rsi()

    return df[['timestamp','close','rsi']]

#coin = "SOLUSDT"

def tarefa():

    try:
        
        #obtendo saldo
        balance = binance.fetch_balance()
        
        #filtrando saldo diferentes de zero
        non_zero_balances = {asset:details for asset, details in balance['total'].items() if details > 0}
        print("Valores na carteira",non_zero_balances)
        #obtendo preços em brl
        ticker = binance.fetch_tickers()
        brl_tickers = {symbol: ticker[symbol] for symbol in ticker if symbol.endswith('/BRL')}
        sol_tickers = {symbol: ticker[symbol] for symbol in ticker if symbol.__eq__('SOL/USDT')}
        price_solana = sol_tickers['SOL/USDT']['last'] * 1
        

        #convertendo saldos para BRL
        balance_brl = {}
        for asset, amount in non_zero_balances.items():
            symbol = f'{asset}/BRL'
            if symbol in brl_tickers:
                price = brl_tickers[symbol]['last']
                balance_brl[asset] = amount * price
            else:
                balance_brl[asset] = "No BRL market available"
    
        print("Valores em real",balance_brl)

        timeframe = "1m"
        rsi_data = get_rsi("SOLUSDT", timeframe)
        rsi_solana = rsi_data.iloc[-1]["rsi"]
        
        print("Preço da solana ", price_solana)
        print("RSI SOLANA", rsi_solana)
    except ccxt.NetworkError as e:
        print(f"Erro de rede: {e}")
    except ccxt.ExchangeError as e:
        print(f"Erro da Exchange: {e}")
    except Exception as e:
        print(f"Erro genérico: {e}")

sc.every().second.do(tarefa)

while True:
    sc.run_pending()
    tm.sleep(1)