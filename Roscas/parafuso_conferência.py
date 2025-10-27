import numpy as np
from typing import Literal
import sys

import warnings
from colorama import Fore, Style, init

init(autoreset=True)  # automatically resets color after each print

def parafuso_conferencia(
    d : int,
    passo : float,
    classe : Literal['4.6','4.8','5.8','8.8','9.8','10.9','12.9'],
    tipo : Literal['ISO','UNS'],
    N : int = None,
    
    F_t : float = 0.0,
    F_c : float = 0.0,
    Ki : int = 0.21,
    ):
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
    else:
        print(f'{Fore.RED}{Style.BRIGHT}ERRO:{Style.NORMAL} Classe fornecida ({classe} inválida)')
        print(f'{Fore.CYAN}{Style.BRIGHT}Sugestão:{Style.NORMAL} Utilize uma das seguintes opções:'+
              f'\'4.6\',\'4.8\',\'5.8\',\'8.8\',\'9.8\',\'10.9\',\'12.9\'')
        sys.exit(0)
    
    
    # ====== Check definição de tipo =====
    if tipo not in ("ISO", "UNS"):
        print(f'{Fore.RED}{Style.BRIGHT}ERRO:{Style.NORMAL} Tipo fornecido ({classe} inválido)')
        raise ValueError("Tipo fornecido inválido")
    
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
        raise ValueError('Para parafuso UNS é necessário fornecer o número de filetes')
    else:
        d_p = d - x1/N # mm - diâmetro primitivo da rosca UNS
        d_r = d - x2/N # mm - diâmetro menor da rosca UNS


    print(f'Dp é: {d_p:.2f}')
    print(f'Dr é: {d_r:.2f}')
    
    # ===== Área sob-tração (Eq.15-2 - Norton) =====
    A_t = np.pi/4 * ( (d_p + d_r)/2 )**2 # mm²
    print(f'Área transversal é: {A_t:.2f}')

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
        
    # ====== Cálculo Tensão ======
    if F_t != 0 and F_c == 0:
        sigma_n = calc_tensão(F_t,A_t)
        sf_t_esc = calc_fs(sigma_n,Sy)
        sf_t_rup = calc_fs(sigma_n,Sut)
        
        if sf_t_esc >= 1:
            print(f'O coeficiente de segurança para a carga de tração'
                +f'com relação à tensão de escoamento é: {sf_t_esc:.2f}')
        elif sf_t_esc <= 1 and sf_t_rup >= 1:
            print(f'O coeficiente de segurança para a carga de tração'
                +f'com relação à tensão de escoamento é: {sf_t_esc:.2f}')
            print(f'O coeficiente de segurança para a carga de tração'
                +f'com relação à tensão de ruptura é: {sf_t_rup:.2f}')   
            print(f'{Fore.YELLOW}{Style.BRIGHT}ATENÇÃO:{Style.NORMAL} O parafuso irá escoar em tração,\n'
                  +'realize a substituição em caso de desmontagem da junta')    
        else:
            print(f'{Fore.YELLOW}{Style.BRIGHT}ATENÇÃO:{Style.NORMAL}O parafuso irá falhar em tração')
            
            # Para montagens carregadas de forma estática, uma pré-carga que gera uma tensão no parafuso de até 90% da resistência de 
            # prova é utilizada alguma vezes. Para juntas carregadas dinamicamente (carga de 
            # fadiga), uma pré-carga de 75% ou mais da resistência de prova é comumente utilizada.
            
            coef = 0.9
            
            Fi = A_t*Sy*coef
            
            print(f'{Fore.CYAN}Força de tração máxima sugerida: {Fi:.2f} N\n'
                  +f'(baseada em {coef*100}% da tensão de prova ({Sp} MPa)')
    elif F_t == 0 and F_c != 0:
        tau = calc_tensão(F_c,As)
        Syc = 0.577*Sy
        sf = calc_fs(tau,Syc)
        if sf >= 1:
            print(f'O coeficiente de segurança para a carga de cisalhamento' 
                +f'com relação à tensão de escoamento é: {sf:.2f}')
        else:
            print(f'{Fore.RED}{Style.BRIGHT}ERRO: {Style.NORMAL}O parafuso irá escoar em cisalhamento, reconsidere o projeto\n'
                 +f'{Fore.CYAN}{Style.BRIGHT}SUGESTÃO:{Style.NORMAL} utilize pinos para distribuir a carga de cisalhamento')
        
    else:
        sigma_n = calc_tensão(F_t,A_t)
        tau = calc_tensão(F_c,As)
        Seq = vonMises(sx=sigma_n,txy=tau)
        sf_eq = calc_fs(Seq,Sy)
    
        if sf_eq >= 1:
                print(f'O coeficiente de segurança para a carga de tração '
                    +f'com relação à teoria de vonMises é: {sf_eq:.2f}')
        else:
            print(f'{Fore.RED}{Style.BRIGHT}ATENÇÃO:{Style.NORMAL} O parafuso irá falhar com a carga')
    
    return
    
    
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


parafuso_conferencia(
    d = 6,
    passo = 1,
    classe = '10.8',
    tipo = 'ISO',
    F_t = 3389.22,
    F_c = 4883.00)