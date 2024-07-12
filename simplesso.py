from fractions import Fraction
from copy import deepcopy


def find_base(m, tipo='b'): # tipo = 'b' per base, 'c' per non base
    B = [-1, -1, -1]
    X_N = []

    for j in range(len(m[0])):
        v_colonna = [m[0][j], m[1][j], m[2][j]]
        
        if v_colonna == [1, 0, 0] and B[0] == -1:
            B[0] = j
        elif v_colonna == [0, 1, 0] and B[1] == -1:
            B[1] = j
        elif v_colonna == [0, 0, 1] and B[2] == -1:
            B[2] = j
        else:
            X_N.append(j)
    
    if tipo == 'c':
        return X_N
    else:
        return B
    
def calcola_gamma_zero(N_T, c_B, c_N): # N_T = matrice non di base, c_B = vettore variabili di base della funzione obiettivo, c_N = vettore variabili non di base della funzione obiettivo
    vet = []
    for i in range(len(N_T)):
        sum = 0
        for j in range(len(N_T[i])):
            sum += c_B[j] * N_T[i][j] 
        vet.append(c_N[i] - sum) 
    return vet

def calcola_matrice_non_di_base(m, x_N): # m = matrice, x_N = vettore delle variabili non di base
    N_T = []
    for n in x_N:
        v = []
        for i in range(len(m)):
            v.append(m[i][n])
        N_T.append(v)
    return N_T

def test_ottimo(g):
    verificato = True
    for elem in g:
        if elem < 0:
            verificato = False
    return verificato

def test_illimitatezza(g_0, N_T): # g_0 = vettore dei costi ridotti, N_T = matrice non di base
    test_tot = False
    for k in range(len(g_0)): 
        if g_0[k] < 0:
            col_neg = True
            for i in range(len(N_T[k])): 
                if N_T[k][i] > 0:
                    col_neg = False
            if col_neg == True:
                test_tot = True

    return test_tot

def criterio_uscita(indice_entrante, N_t, b):
    elementi = []
    for j in range(len(b)):
        if N_t[indice_entrante][j] > 0:
            elementi.append(b[j] / N_t[indice_entrante][j])
    return elementi.index(min(elementi))

def trasposta_matrice(m):
    m_t = []
    for j in range(len(m[0])):
        v = []
        for i in range(len(m)):
            v.append(m[i][j])
        m_t.append(v)
    return m_t

def costruzione_base_canonica(M, v_entrante, k, b, voglio_vettore =None):
    N = deepcopy(M)
    a = list(range(len(v_entrante)))
    for j in range(len(N[0])):
        N[k][j] = (Fraction(N[k][j], v_entrante[k]))
        a[k] = Fraction(b[k], v_entrante[k])

 
    for i in range(len(N)):
        if i != k:
            for j in range(len(N[i])):
                N[i][j] = Fraction(N[i][j]) + (N[k][j] * (-v_entrante[i]))
            a[i] = Fraction(b[i]) + (a[k] * (-v_entrante[i]))


    if voglio_vettore:
        return a
    else:
        return N

def nuova_coppia_vettori_indici(x_b, x_n, indice_variabile_entrante, indice_variabile_uscente):
    x_bc = deepcopy(x_b)
    x_nc = deepcopy(x_n)
    
    x_bc[indice_variabile_uscente] = x_n[indice_variabile_entrante]
    x_nc[indice_variabile_entrante] = x_b[indice_variabile_uscente]
    
    return [x_bc, x_nc]

def soluzione(x_b, b):
    soluzione = [0, 0, 0, 0, 0, 0]
    for i in range(len(b)):
        soluzione[x_b[i]] = b[i]
    return soluzione

u = [1, 2, 1, 1, 1, 1] #vettore dei costi
m = [[1, 2, 3, 1, 0, 0], [2, -1, -5, 0, 1, 0], [1, 2, -1, 0, 0, 1]] #matrice
B = [[1, 0, 0], [0, 1, 0], [0, 0, 1]] #matrice base
b = [3, 2, 1] #vettore dei termini noti

x_b = find_base(m, 'b') #vettore degli indici delle variabili di base
x_n = find_base(m, 'c') #vettore degli indici delle variabili non di base
N_t = calcola_matrice_non_di_base(m, x_n) #matrice non di base
c_b = [u[k] for k in x_b] #vettore delle variabili di base della funzione obiettivo 
c_n = [u[k] for k in x_n] #vettore delle variabili non di base della funzione obiettivo

print(f"x_b: {x_b}")
print(f"x_n: {x_n}")
print(f"c_b: {c_b}")
print(f"c_n: {c_n}")
print(f"N_t: {N_t}\n")

'''
g_0 = calcola_gamma_zero(N_t, c_b, c_n)
print(f"Gamma zero: {g_0}")

print("test di ottimalità: ", end='')
print(test_ottimo(g_0))

print("test di illimitatezza: ", end='') 
print(test_illimitatezza(g_0, N_t)) #test di illimitatezza


indice_variabile_entrante = g_0.index(min(g_0))
vettore_entrante = N_t[indice_variabile_entrante]
print(f"Indice variabile entrante: {indice_variabile_entrante}")
print(f"vettore entrante: {vettore_entrante}")
indice_variabile_uscente = criterio_uscita(indice_variabile_entrante, N_t, b)

print(f"Indice variabile uscente: {indice_variabile_uscente}")

N_1_t = []

for i in range(len(N_t)):
    if i == indice_variabile_entrante:
        N_1_t.append(B[indice_variabile_uscente])
    else:
        N_1_t.append(N_t[i])

N_1 = trasposta_matrice(N_1_t)
print("N_1:", N_1, "\n \n \n")



N_1c = costruzione_base_canonica(N_1, vettore_entrante, indice_variabile_uscente, b)
b_c = costruzione_base_canonica(N_1, vettore_entrante, indice_variabile_uscente, b, 1)

print(N_1c)
print(b_c)


coppia = nuova_coppia_vettori_indici(x_b, x_n)
x_bc = coppia[0]
x_nc = coppia[1]

print(x_bc, x_nc)
'''

def simplesso(x_b, x_n, N_t, c_b, c_n, b):

    print(f"x_b: {x_b}")
    print(f"x_n: {x_n}")
    print(f"c_b: {c_b}")
    print(f"c_n: {c_n}")
    print(f"N_t: {N_t}")
    print(f"b: {b}\n")

    g_0 = calcola_gamma_zero(N_t, c_b, c_n)
    print(f"Gamma zero: {g_0}")

    print("test di ottimalità: ", test_ottimo(g_0))


    if test_ottimo(g_0):
        return soluzione(x_b, b)

    print("test di illimitatezza: ", end='') 
    print(test_illimitatezza(g_0, N_t)) #test di illimitatezza
    if test_illimitatezza(g_0,N_t):
        return "illimitato"


    indice_variabile_entrante = g_0.index(min(g_0))
    vettore_entrante = N_t[indice_variabile_entrante]
    print(f"Indice variabile entrante: {indice_variabile_entrante}")
    print(f"vettore entrante: {vettore_entrante}")

    indice_variabile_uscente = criterio_uscita(indice_variabile_entrante, N_t, b)
    print(f"Indice variabile uscente: {indice_variabile_uscente}")

    N_1_t = [] #nuova matrice non di base trasposta

    for i in range(len(N_t)):
        if i == indice_variabile_entrante:
            N_1_t.append(B[indice_variabile_uscente])
        else:
            N_1_t.append(N_t[i])

    N_1 = trasposta_matrice(N_1_t)
    print("N_1:", N_1, "\n \n \n")



    N_c = costruzione_base_canonica(N_1, vettore_entrante, indice_variabile_uscente, b)
    b_c = costruzione_base_canonica(N_1, vettore_entrante, indice_variabile_uscente, b, 1)

    print(N_c)
    print(b_c)

    N_c_t = trasposta_matrice(N_c)
    print(N_c_t)

    coppia = nuova_coppia_vettori_indici(x_b, x_n, indice_variabile_entrante, indice_variabile_uscente)
    x_bc = coppia[0]
    x_nc = coppia[1]

    
    print(f"x_b: {x_bc}")
    print(f"x_n: {x_nc}")
    print(f"c_b: {c_b}")
    print(f"c_n: {c_n}")
    print(f"N_t: {N_c_t}")
    print(f"b: {b_c}\n")

    return simplesso(x_bc, x_nc, N_c_t, c_b, c_n, b_c)
    

soluz = simplesso(x_b, x_n, N_t, c_b, c_n, b)

print(soluz)
