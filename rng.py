import time
import random

#Linear Congruential Generator
#Formula: X_{n+1} = (aX_{n} + c) mod n
#Where: X_{0} -> seed
#       a -> multiplier
#       c -> increment
#       m -> module
#Reference: Donald Knuth, The Art of Computer Programming, Volume 2: Seminumerical Algorithms
def lcg(seed, a, c, m, bits):
    x = seed #store seed
    result = 0
    for _ in range(bits):
        x = (a * x + c) % m #gen next sequence number
        result = (result << 1) | (x & 1) #shifts left and adds the least significant bit to result
    return result

#Lagged Fibonacci Generator
#Formula: X_{n} = (X_{n-j} o X_{n-k}) mod m
#Where  : k and j -> lags
#       : o -> operation (XOR, +, -, ...)
#       : m -> module (power of two for an easy implementation)
#Reference: Tezuka, S. Uniform Random Numbers: Theory and Practice, 1995
def lfg(seed_list, j, k, bits, m=2**32):
    state = seed_list[:] #copy the list
    result = 0
    for _ in range(bits):
        new = (state[-j] ^ state[-k]) % m #xor between numbers and module
        state.append(new) #adds a new number to the state
        result = (result << 1) | (new & 1) # shifts left and adds the least significant bit to result
    return result


def test_rng(gerador, *args, bits, n_testes=10):
    tempos = []
    for _ in range(n_testes):
        start = time.time()
        num = gerador(*args, bits)
        end = time.time()
        tempos.append(end - start)
    return (sum(tempos) / len(tempos)), num

def run_all():
    sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]
    results = []

    # LCG
    lcg_seed = 12345
    a = 1664525
    c = 1013904223
    m = 2**32

    #LFG
    lfg_seed_list = [random.randint(0, 2**32 - 1) for _ in range(17)]
    j = 5
    k = 17

    for bits in sizes:
        time_lcg, num = test_rng(lcg, lcg_seed, a, c, m, bits=bits)
        results.append({
            "Generator": "LCG",
            "Bits_size": bits,
            "Mean_time": round(time_lcg, 9),
            "Number" : num
        })

        # LFG
        time_lfg, num = test_rng(lfg, lfg_seed_list, j, k, bits=bits)
        results.append({
            "Generator": "LFG",
            "Bits_size": bits,
            "Mean_time": round(time_lfg, 9),
            "Number": num
        })

    return results


if __name__ == "__main__":
    r = run_all()
    for i in r:
        print(f"{i['Generator']} | {i['Bits_size']} bits | {i['Mean_time']} seconds | Number: {i['Number']}")