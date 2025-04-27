import time
import random
from rng import lcg, lfg
from prime import miller_rabin, fermat_test

# Números primos conhecidos
primos_reais = [3, 17, 101, 7919, 524287]

# Falsos primos
falsos_primos = [
    294409,     
    410041,     
    825265,     
    321197185,  
    499001,     
    10991262241 
]

def encontrar_primo(bits, gerador_nome, metodo_primalidade, max_tentativas=1000000):
    for tentativa in range(max_tentativas):
        # Para o LCG: nova seed a cada tentativa
        if gerador_nome == "LCG":
            seed = random.getrandbits(32)
            a = 1635186
            c = 1568161531
            m = 2**128
            numero = lcg(seed, a, c, m, bits)

        # Para o LFG: nova seed list a cada tentativa
        elif gerador_nome == "LFG":
            seed_list = [random.getrandbits(32) for _ in range(17)]
            j = 5
            k = 16
            numero = lfg(seed_list, j, k, bits)

        # Garante que é ímpar e que o bit mais significativo está em 1
        numero |= 1
        numero |= (1 << (bits - 1))

        if metodo_primalidade(numero, k=10):
            return numero, tentativa + 1

    return None, max_tentativas


def gerar_primos_com_tempo():
    resultados = []
    sizes = [512, 1024, 2048, 4096]

    for bits in sizes:
        for gerador in ["LFG"]:
            for metodo_nome, metodo in [
                ("Miller-Rabin", miller_rabin),
                ("Fermat", fermat_test)
            ]:
                inicio = time.time()
                primo, tentativas = encontrar_primo(bits, "LFG", metodo)
                fim = time.time()

                resultados.append({
                    "Gerador": "LFG",
                    "Bits": bits,
                    "Método": metodo_nome,
                    "Primo encontrado": str(primo),
                    "Tentativas": tentativas,
                    "Tempo (s)": round(fim - inicio, 6)
                })

    return resultados


for numero in falsos_primos:
    print(f"Testando {numero}:")
    if fermat_test(numero):
        print("  Fermat: Possível primo")
    else:
        print("  Fermat: Comprovadamente composto.")

    if miller_rabin(numero):
        print("  Miller-Rabin: Possível primo")
    else:
        print("  Miller-Rabin: Comprovadamente composto.")


#if __name__ == "__main__":
#    resultados = gerar_primos_com_tempo()
#    for r in resultados:
#        print(f"{r['Gerador']} | {r['Bits']} bits | {r['Método']} | "
#              f"Tentativas: {r['Tentativas']} | Tempo: {r['Tempo (s)']}s\n"
#              f"Primo encontrado: {r['Primo encontrado']}...\n")

