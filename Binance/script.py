from functions import *

ticks = buscarTicks()
# ticks.remove("XRPUSDT")
ticksNumber = len(ticks)
print("NUMERO DE TICKS: " + str(ticksNumber))

while 1:
    actualTicks = buscarTicks()
    if ticksNumber < len(actualTicks):
        for tick in actualTicks:
            if tick not in ticks:
                print("NUEVA MONEDA ENCONTRADA: " + str(tick))
                ticks.append(tick)
                ticksNumber = len(ticks)
                if dinero_Disponible():
                    comprarMoneda(tick)
                else:
                    print("DINERO DISPONIBLE INSUFICIENTE")
                    input("PRESIONE ENTER PARA CONTINUAR...")
                    exit()
                print("NUMERO DE TICKS: " + str(ticksNumber))
    time.sleep(1)
