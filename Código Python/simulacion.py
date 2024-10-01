import numpy as np
from scipy.stats import wald, genhyperbolic
import argparse

def intervalo_entre_arribos():
    loc = -3.302065280807085
    scale = 26.272413492938348
    return max(wald.rvs(loc=loc, scale=scale), 0)

def tiempo_de_atencion():
    p = -1.2013473124553011
    a = 1.8163181809574367
    b = 1.8163181809574356
    loc = 275.05572981182365
    scale = 188.90036583768813
    return max(genhyperbolic.rvs(p=p, a=a, b=b, loc=loc, scale=scale), 0)

def cantidad_hilos_desocupados(instancia: list[int], t: int):
    return sum(1 for hilo in instancia if hilo <= t)

def min_instancia(instancias: list[list[int]], t: int) -> int:
    return max(range(len(instancias)), key=lambda i: cantidad_hilos_desocupados(instancias[i], t))

def min_hilo(instancia: list[int], t: int) -> int:
    return instancia.index(min(instancia))

def cantidad_hilos_ocupados(instancia: list[int], t: int) -> int:
    return sum(1 for hilo in instancia if hilo > t)

def crear_instancia(instancias: list[list[int]], cantidad_hilos: int, tiempo: int):
    instancias.append([tiempo] * cantidad_hilos)

def simular(ch: int, cimin: int, cimax: int, tf: int):
    tpll = 0
    strt = 0
    nt = 0
    ce = 0
    cia = cimin
    cil_max = cia
    instancias = []

    for _ in range(cimin):
        instancias.append([0] * ch)

    while True:
        t = tpll
        ia = intervalo_entre_arribos()
        tpll = t + ia

        i = min_instancia(instancias, t)
        j = min_hilo(instancias[i], t)

        tiempo_comprometido = instancias[i][j]
        ta = tiempo_de_atencion()

        if t < tiempo_comprometido:
            ce += 1
            strt += (tiempo_comprometido - t) + ta 
            instancias[i][j] += ta
        else:
            strt += ta 
            instancias[i][j] = t + ta

            hilos_ocupados = cantidad_hilos_ocupados(instancias[i], t)

            if hilos_ocupados == int(ch/2) and cia < cimax:
                crear_instancia(instancias, ch, t)
                cia += 1

                if cia > cil_max:
                    cil_max = cia
        
        nt += 1
        print(f"La ejecución de la simulación va al {"{:.2f}".format(t*100/tf)}%", end="\r")

        if t > tf:
            break

    trp = strt / nt
    pse = ce * 100/ nt

    print("------------------- Fin de la simulación -------------------")
    print(f"Para los siguientes valores de entrada:")
    print(f"- Cantidad de Hilos por instancia:{ch}")
    print(f"- Cantidad mínima de instancias en ejecución: {cimin}")
    print(f"- Cantidad máxima de instancais en ejecución: {cimax}")
    print("\n")
    print(f"Se obtuvieron los siguientes resultados:")
    print(f"El tiempo de respuesta promedio en milisegundos es: {trp}")
    print(f"Máxima cantidad de instancias levantadas en simultáneo: {cil_max}")
    print(f"Porcentaje de solicitudes que tuvieron que esperar: {pse}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulador de llegada de instancias.")
    parser.add_argument('--ch', type=int, required=True, help='Cantidad de hilos')
    parser.add_argument('--cimax', type=int, required=True, help='Cantidad máxima de instancias')
    parser.add_argument('--cimin', type=int, required=True, help='Cantidad mínima de instancias')
    parser.add_argument('--tf', type=int, required=True, help='Tiempo final de la simulación')

    args = parser.parse_args()

    simular(args.ch, args.cimin, args.cimax, args.tf)
