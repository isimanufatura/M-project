#%%
import numpy as np
import pandas as pd
from typing import Literal

import warnings
import sys

from colorama import Fore, Style, init
init(autoreset=True)  # automatically resets color after each print

# ----------------------------------------------------------
def calc_tensão(F,A):
    sigma = F/A
    return sigma

def calc_fs(sigma,sigma_esc):
    sf = sigma_esc/sigma
    return sf

def vonMises(
    sx:float=0.0,
    sy:float=0.0,
    sz:float=0.0,
    txy:float=0.0,
    tyz:float=0.0,
    tzx:float=0.0
):
    Seq = np.sqrt(((sx-sy)**2+(sy-sz)**2+(sz-sx)**2+6*(txy**2+tyz**2+tzx**2))/2)
    return Seq
# ----------------------------------------------------------

tipo = 'ISO'
#tipo = 'UNS'

# ----------------------------------------------------------

if tipo == 'ISO':
    # Valori standard definiti ISO
    d_std = [3,3.5,4,5,6,7,8,10,12,14,16,18,20,22,24,27,30,33,36,39]
    classe_std = ['4.6','4.8','5.8','8.8','9.8','10.9','12.9']
    grau_SAE_std = ['1','2','4','5','5.2','7','8','8.2']

    passo_rosca_grossa = [0.5,0.6,0.7,0.8,1.0,1.0,1.25,150,175,2.0,2.0,2.5,
                        2.5,2.5,3.0,3.0,3.5,3.5,4.0,4.0]
    passo_rosca_fina = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,
                        1.0,1.25,1.25,1.5,1.5,1.5,1.5,1.5,2.0,2.0,2.0,2.0,3.0,3.0]
    print(f'Lunghezza rosca_grossa: {len(passo_rosca_grossa)}')
    print(f'Lunghezza rosca_fina: {len(passo_rosca_fina)}')
    
elif tipo == 'UNS':
    # Valori standard definiti UNS
    d_std = [0.0730,0.086,0.099,0.112,0.125,0.1380,0.164,0.19,0.2160,0.25,0.3125,
            0.3750,0.4375,0.5,0.562,0.6250,0.75,0.875,1.0,1.125,1.25,1.375,1.5,1.75,
            2.0,2.25,2.5,2.753,3.0,3.25,3.5,3.75,4.0]

    N_rosca_grossa = [64,56,48,40,40,32,32,24,24,20,18,16,14,13,12,11,10,
                    9,8,7,7,6,6,5,4.5,4.5,4,4,4,4,4,4,4]

    N_rosca_fina = [72,64,56,48,44,40,36,32,28,28,24,
                    24,20,20,18,18,16,14,2,12,12,12,12,
                    np.nan,np.nan,np.nan,np.nan,np.nan,
                    np.nan,np.nan,np.nan,np.nan,np.nan]
    print(f'Lunghezza rosca_grossa: {len(N_rosca_grossa)}')
    print(f'Lunghezza rosca_fina: {len(N_rosca_fina)}')
else:
    print(f'{Fore.RED}{Style.BRIGHT}ERRO:{Style.NORMAL} Tipo fornecido ({tipo} inválido)')
    raise ValueError("Tipo fornecido inválido")

# ====== Check definição de Classe =====
#faixa_diametros = {
#    '4.6'    : (5.0,36.0),
#    '4.8'    : (1.6,16.0),
#    '5.8'    : (5.0,24.0),
#    '8.8'    : (3.0,36.0),
#    '9.8'    : (1.6,16.0),
#    '10.9'   : (5.0,36.0),
#    '12.9'   : (1.6,36.0),
#}
#
#if classe in faixa_diametros:
#    d_min, d_max = faixa_diametros[classe]
#    if not (d_min <= d <= d_max):
#        warnings.warn(
#            f"Para a classe {classe}, o diâmetro deve estar entre {d_min} e {d_max} mm."
#        )
#        df.loc[i,'Aplicável?'] = f"🟡Para a classe {classe}, o diâmetro deve estar entre {d_min} e {d_max} mm."
#        continue

# ----------------------------------------------------------

# ----------------------------------------------------------
# Definire valori min e massimi
d_min = 4
d_max = 6

classe_min = '5.8'
classe_max = '9.8'

n_min = 4
n_max = 6

# ----------------------------------------------------------
# Definizioni generali

passo = passo_rosca_grossa

# ----------------------------------------------------------

# Liste di tutti i valori selezionati
d = []
p = []
p_type = []
for i in range(d_std.index(d_min),
               d_std.index(d_max)+1):
    d.append(d_std[i])
    print(f'i: {i}')
    if passo_rosca_grossa[i] != np.nan:
        p.append(passo_rosca_grossa[i])
        p_type.append('Rosca Grossa')
        print(f'Rosca grossa {i}')
    else:
        continue
    if passo_rosca_fina[i] != np.nan:
        p.append(passo_rosca_fina[i])
        p_type.append('Rosca Fina')
        print(f'Rosca grossa {i}')
    else:
        continue
         
    
classe = []
for i in range(classe_std.index(classe_min),
               classe_std.index(classe_max)+1):
    classe.append(classe_std[i])
    
numero = []
a = n_min
for i in range(n_min,n_max+1):
    numero.append(a)
    a += 1
    
print(f'd:{d}')
print(f'p:{p}')
print(f'classe:{classe}')
print(f'numero:{numero}')

# ----------------------------------------------------------
# Creando tutte le opzioni

combination = []
#for i,j in zip(d,p):
#    for k in classe:
#        for l in numero:
#            a = (i,j,k,l)
#            combination.append(a)

for i,j,k in zip(d,p,p_type):
    for l in classe:
        for m in numero:
            a = (i,j,k,l,m)
            combination.append(a)

print(combination)
print(f'Lunghezza di comination: {len(combination)}')

# ----------------------------------------------------------
# Creando il dataframe

df = pd.DataFrame(combination, columns=['Diâmetro','Passo','Tipo passo','Classe','Número'])
print(df)

#a = df.iloc[1]['Número']
#print(a)
#print(type(a))
#
#print(df.shape[0])
#
#df['Aplicável?'] = 1
#print(df)

# ----------------------------------------------------------
#%%
F_t = 5e4
F_c = 2e3

for i in range(df.shape[0]):
    d = df['Diâmetro'].iloc[i]
    passo = df['Passo'].iloc[i]
    classe = df['Classe'].iloc[i]
    num = df['Número'].iloc[i]
    
    print(f'i:{i}')
    print(f'diametro:{d}')
    print(f'passo:{passo}')
    print(f'classe:{classe}')

    tipo = 'ISO'
    N = 3 #*

    '''
    Parâmetros
    ----------
    d : int (número inteiro)
        Diâmetro nominal do parafuso em mm
    passo : float (número decimal)
        Passo do parafuso em mm
    classe : str (linha de escrita)
        Classe do parafuso, utilizada para extrair as propriedades do material
        Utilizar uma das seguintes entradas: '4.6','4.8','5.8','8.8','9.8','10.9','12.9'
    tipo : str (linha de escrita)
        Tipo de rosca do parafuso
        Utilizar uma das seguintes entradas: 'ISO','UNS'
    N : int (optional)
        Número de filetes por polegadas
        (Somente para rosca tipo 'UNS')
    F_t : float (optional)
        Força de tração aplicada no parafuso em N
    F_c : float (optional)
        Força de cisalhamento aplicada no parafuso em N
    Ki : float (optional)
        Coeficiente de torque
        Considera o atrito entre os filetes para a pré-carga do parafuso
        Valor padrão de 0.21

    '''

    # ====== Check definição de Classe =====
    faixa_diametros = {
        '4.6'    : (5.0,36.0),
        '4.8'    : (1.6,16.0),
        '5.8'    : (5.0,24.0),
        '8.8'    : (3.0,36.0),
        '9.8'    : (1.6,16.0),
        '10.9'   : (5.0,36.0),
        '12.9'   : (1.6,36.0),
    }

    if classe in faixa_diametros:
        d_min, d_max = faixa_diametros[classe]
        if not (d_min <= d <= d_max):
            warnings.warn(
                f"Para a classe {classe}, o diâmetro deve estar entre {d_min} e {d_max} mm."
            )
            df.loc[i,'Aplicável?'] = f"🟡Para a classe {classe}, o diâmetro deve estar entre {d_min} e {d_max} mm."
            continue

    else:
        print(f'{Fore.RED}{Style.BRIGHT}ERRO:{Style.NORMAL} Classe fornecida ({classe} inválida)')
        print(f'{Fore.CYAN}{Style.BRIGHT}Sugestão:{Style.NORMAL} Utilize uma das seguintes opções:'+
                f'\'4.6\',\'4.8\',\'5.8\',\'8.8\',\'9.8\',\'10.9\',\'12.9\'')
        #sys.exit(0)
        df.loc[i,'Aplicável?'] = f'🔴{Fore.RED}{Style.BRIGHT}ERRO:{Style.NORMAL} Classe fornecida ({classe} inválida)'
        continue


    # ====== Check definição de tipo =====
    if tipo not in ("ISO", "UNS"):
        print(f'{Fore.RED}{Style.BRIGHT}ERRO:{Style.NORMAL} Tipo fornecido ({classe} inválido)')
        df.loc[i,'Aplicável?'] = f"🔴Tipo de rosca fornecido inválido"
        continue
        #raise ValueError("Tipo fornecido inválido")

    # Resistência mínima de prova (Tabela 15-7)
    # Utilizada como limite de pré-carga

    sigma_crit = {
        # Classe : 
        # Resistência mínima de prova & Resistência mínima de escoamento & Resistência mínima à tração
        '4.6'    : (225,240,400),
        '4.8'    : (310,340,420),
        '5.8'    : (380,420,520),
        '8.8'    : (600,660,830),
        '9.8'    : (650,720,900),
        '10.9'   : (830,940,1040),
        '12.9'   : (970,1100,1220),
    }

    Sp, Sy, Sut = sigma_crit[classe]

    # ====== Cálculo diâmetros parafuso ====== 
    x1 = 0.649519
    x2 = 1.226869

    if tipo == 'ISO':
        d_p = d - x1*passo # mm - diâmetro primitivo da rosca ISO
        d_r = d - x2*passo # mm - diâmetro menor da rosca ISO
    elif N == None:
        df.loc[i,'Aplicável?'] = f"🔴Para parafuso UNS é necessário fornecer o número de filetes"
        #raise ValueError('Para parafuso UNS é necessário fornecer o número de filetes')
    else:
        d_p = d - x1/N # mm - diâmetro primitivo da rosca UNS
        d_r = d - x2/N # mm - diâmetro menor da rosca UNS


    print(f'Dp é: {d_p:.2f}')
    print(f'Dr é: {d_r:.2f}')

    # ===== Área sob-tração (Eq.15-2 - Norton) =====
    A_t = np.pi/4 * ( (d_p + d_r)/2 )**2 # mm²
    print(f'Área transversal é: {A_t:.2f}')
    A_t = A_t * num # modificação para junta parafusada
    print(f'Área transversal de todos os parafusos é: {A_t:.2f}')

    # ===== Área sob-cisalhamento  =====

    wi = 0.80
    wo = 0.88

    As_i = np.pi*d_r*wi*passo
    As_o = np.pi*d*wo*passo

    if As_i < As_o:
        As = As_i
        print('As_i menor')
    else:
        As = As_o
        print('As_o menor')
    
    As = As * num
    
    # ====== Cálculo Tensão ======
    if F_t != 0 and F_c == 0:
        sigma_n = calc_tensão(F_t,A_t)
        sf_t_esc = calc_fs(sigma_n,Sy)
        sf_t_rup = calc_fs(sigma_n,Sut)
        
        if sf_t_esc >= 1:
            print(f'O coeficiente de segurança para a carga de tração'
                +f'com relação à tensão de escoamento é: {sf_t_esc:.2f}')
        elif sf_t_esc <= 1 and sf_t_rup >= 1:
            print(f'🟢{Fore.GREEN} O coeficiente de segurança para a carga de tração'
                +f'com relação à tensão de escoamento é: {sf_t_esc:.2f}')
            print(f'🟢{Fore.GREEN} O coeficiente de segurança para a carga de tração'
                +f'com relação à tensão de ruptura é: {sf_t_rup:.2f}')   
            print(f'🟡{Fore.YELLOW}{Style.BRIGHT}ATENÇÃO:{Style.NORMAL} O parafuso irá escoar em tração,\n'
                    +'realize a substituição em caso de desmontagem da junta')
            df.loc[i,'Aplicável?'] = (
                f'🟢O coeficiente de segurança para a carga de tração'+
                f'com relação à tensão de escoamento é: {sf_t_esc:.2f}\n'+
                f'🟢O coeficiente de segurança para a carga de tração'+
                f'com relação à tensão de ruptura é: {sf_t_rup:.2f}\n'+
                f'🟡 ATENÇÃO: O parafuso irá escoar em tração,\n'
                +'realize a substituição em caso de desmontagem da junta'
            )
            
        else:
            print(f'🟡{Fore.YELLOW}{Style.BRIGHT}ATENÇÃO:{Style.NORMAL}O parafuso irá falhar em tração')
            
            # Para montagens carregadas de forma estática, uma pré-carga que gera uma tensão no parafuso de até 90% da resistência de 
            # prova é utilizada alguma vezes. Para juntas carregadas dinamicamente (carga de 
            # fadiga), uma pré-carga de 75% ou mais da resistência de prova é comumente utilizada.
            
            coef = 0.9
            
            Fi = A_t*Sy*coef
            
            print(f'🔵{Fore.CYAN}Força de tração máxima sugerida: {Fi:.2f} N\n'
                    +f'(baseada em {coef*100}% da tensão de prova ({Sp} MPa)')
            df.loc[i,'Aplicável?'] = (
                f'🟡 ATENÇÃO: O parafuso irá falhar em tração\n' +
                f'🔵 Força de tração máxima sugerida: {Fi:.2f} N\n' +
                f'(baseada em {coef*100}% da tensão de prova ({Sp} MPa)'
            )
            
    elif F_t == 0 and F_c != 0:
        tau = calc_tensão(F_c,As)
        Syc = 0.577*Sy
        sf = calc_fs(tau,Syc)
        if sf >= 1:
            print(f'🟢 O coeficiente de segurança para a carga de cisalhamento' 
                +f'com relação à tensão de escoamento é: {sf:.2f}')
            df.loc[i,'Aplicável?'] = (
                f'🟢 O coeficiente de segurança para a carga de cisalhamento' 
                +f'com relação à tensão de escoamento é: {sf:.2f}'
            )
            
        else:
            print(f'{Fore.RED}{Style.BRIGHT}ERRO: {Style.NORMAL}O parafuso irá escoar em cisalhamento, reconsidere o projeto\n'
                    +f'{Fore.CYAN}{Style.BRIGHT}SUGESTÃO:{Style.NORMAL} utilize pinos para distribuir a carga de cisalhamento')
            df.loc[i,'Aplicável?'] = (
                f'🔴 ERRO: {Style.NORMAL}O parafuso irá escoar em cisalhamento, reconsidere o projeto\n'
                +f'🔵 SUGESTÃO:{Style.NORMAL} utilize pinos para distribuir a carga de cisalhamento'
            )
        
    else:
        sigma_n = calc_tensão(F_t,A_t)
        tau = calc_tensão(F_c,As)
        Seq = vonMises(sx=sigma_n,txy=tau)
        sf_eq = calc_fs(Seq,Sy)

        if sf_eq >= 1:
                print(f'🟢 O coeficiente de segurança para a carga de tração '
                    +f'com relação à teoria de vonMises é: {sf_eq:.2f}')
                df.loc[i,'Aplicável?'] = (
                    '🟢 O coeficiente de segurança para a carga de tração '
                    +f'com relação à teoria de vonMises é: {sf_eq:.2f}'
                )
        else:
            print(f'🔴{Fore.RED}{Style.BRIGHT}ATENÇÃO:{Style.NORMAL} O parafuso irá falhar com a carga')
            df.loc[i,'Aplicável?'] = (
                f'🔴ATENÇÃO: O parafuso irá falhar com a carga'
            )

print(df)

# %%
