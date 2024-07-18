import config
from binance.client import Client
import time

usdtAmount = config.usdtAmount

client = Client(config.API_KEY, config.API_SECRET, tld='com')


def buscarTicks():
    ticks = []

    while True:
        try:
            list_of_tickers = client.get_all_tickers()
        except Exception as e:
            print(e)
            archivo = open("log.txt", "a")
            mensaje = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e) + "\n"
            archivo.write(mensaje)
            archivo.close()
            time.sleep(2)
        else:
            break

    for tick in list_of_tickers:
        if tick['symbol'][-4:] != 'USDT':
            continue
        ticks.append(tick['symbol'])
    return ticks


def dinero_Disponible():
    global balance
    while True:
        try:
            balance = client.get_account()
        except Exception as e:
            print(e)
            archivo = open("log.txt", "a")
            mensaje = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e) + "\n"
            archivo.write(mensaje)
            archivo.close()
            time.sleep(2)
        else:
            break
    for money in balance["balances"]:
        if money["asset"] == "USDT":
            disponible = round(float(money["free"]), 2)
            if disponible > usdtAmount:
                return True
            else:
                return False


def comprarMoneda(tick):
    while True:
        try:
            client.create_order(
                symbol=tick,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quoteOrderQty=usdtAmount)
        except Exception as e:
            print(e)
            archivo = open("log.txt", "a")
            mensaje = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e) + "\n"
            archivo.write(mensaje)
            archivo.close()
            time.sleep(2)
        else:
            break

    print("MONEDA COMPRADA CON EXITO")
