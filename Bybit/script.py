import config
import time
from pybit.unified_trading import HTTP

usdtAmount = config.usdtAmount
token = ''  # Dejar en blanco si quieres que compre caulquier moneda, si no especificarla

session = HTTP(
    testnet=False,
    api_key=config.api_key,
    api_secret=config.api_secret,
)


def buscarTicks():
    ticks = []

    while True:
        try:
            list_of_tickers = session.get_tickers(category="spot")
        except Exception as e:
            print(e)
            archivo = open("log.txt", "a")
            mensaje = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e) + "\n"
            archivo.write(mensaje)
            archivo.close()
            time.sleep(2)
        else:
            break

    for tick in list_of_tickers['result']['list']:
        if tick['symbol'][-4:] != 'USDT':
            continue
        ticks.append(tick['symbol'])
    return ticks


def dinerodisponible():
    global balance
    while True:
        try:
            balance = session.get_wallet_balance(accountType="SPOT", coin="USDT")
        except Exception as e:
            print(e)
            archivo = open("log.txt", "a")
            mensaje = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e) + "\n"
            archivo.write(mensaje)
            archivo.close()
            time.sleep(2)
        else:
            break

    balance = round(float(balance['result']['list'][0]['coin'][0]['free']), 2)

    if balance >= usdtAmount:
        return True
    else:
        return False


def comprarmoneda(tick):
    try:
        session.place_order(category="spot", symbol=tick, side="Buy", orderType="Market", qty=str(usdtAmount), marketUnit='quoteCoin')
    except Exception as e:
        print(e)
        archivo = open("log.txt", "a")
        mensaje = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()) + ' ERROR: ' + str(e) + "\n"
        archivo.write(mensaje)
        archivo.close()
        time.sleep(2)

    print("MONEDA COMPRADA CON EXITO")


ticks = buscarTicks()
# ticks.remove('XRPUSDT') para hacer prueba de compra
ticksNumber = len(ticks)
print("NUMERO DE TICKS en BYBIT: " + str(ticksNumber))


while 1:
    actualTicks = buscarTicks()
    if ticksNumber < len(actualTicks):
        for tick in actualTicks:
            if tick not in ticks:
                print("NUEVA MONEDA ENCONTRADA: " + str(tick))
                ticks.append(tick)
                ticksNumber = len(ticks)
                if dinerodisponible():
                    if token == '':
                        comprarmoneda(tick)
                    else:
                        if token == tick:
                            comprarmoneda(tick)
                        else:
                            print('ESTE TOKEN NO ES: ' + token)
    print('Buscando token nuevo...')
    time.sleep(1)
