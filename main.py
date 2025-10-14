import pandas as pd
import time
import os
import random

MAX_OPTIONS = 2
rod = 0
str = 0
luck = 100
rod_bonus = rod * 0.1
str_bonus = str * 0.05
luck_bonus = luck * 0.7

BASE_CHANCES = {
    "Secret": 0.1,
    "Legendary": 1,
    "Epic": 4,
    "Rare": 10,
    "Uncommon": 24.9,
    "Common": 60,
}

def calcular_raridades():
    BONUS_TOTAL = rod_bonus + str_bonus + luck_bonus
    CHANCES = BASE_CHANCES.copy()
    CHANCES["Common"] = max(5, BASE_CHANCES["Common"] - BONUS_TOTAL)
    BONUS_RECALCULADO = BASE_CHANCES["Common"] - CHANCES["Common"]
    if BONUS_RECALCULADO > 0:
        CHANCES["Secret"] += BONUS_RECALCULADO * 0.03
        CHANCES["Legendary"] += BONUS_RECALCULADO * 0.07
        CHANCES["Epic"] += BONUS_RECALCULADO * 0.10
        CHANCES["Rare"] += BONUS_RECALCULADO * 0.30
        CHANCES["Uncommon"] += BONUS_RECALCULADO * 0.50
    return CHANCES


PEIXES = {
    "Secret": ["Tubarao"],
    "Legendary": ["Peixe Morto-vivo"],
    "Epic": ["Peixe Borboleta"],
    "Rare": ["Salmao"],
    "Uncommon": ["Peixe Palhaco","Teste","Bota"],
    "Common": ["Carpa","Atum"]
}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def startup():
    limpar_tela()
    print("====================")
    print("\n  PY FISHING GAME")
    print("  v. A01\n")
    print("====================")
    os.system("pause")
    limpar_tela()

def gerar_peixe():
    CHANCES = calcular_raridades()
    x = random.uniform(0,100)
    if x <= CHANCES["Secret"]:
        prarity = "Secret"
    elif x <= CHANCES["Secret"] + CHANCES["Legendary"]:
        prarity = "Legendary"
    elif x <= CHANCES["Secret"] + CHANCES["Legendary"] + CHANCES["Epic"]:
        prarity = "Epic"
    elif x <= CHANCES["Secret"] + CHANCES["Legendary"] + CHANCES["Epic"] + CHANCES["Rare"]:
        prarity = "Rare"
    elif x <= CHANCES["Secret"] + CHANCES["Legendary"] + CHANCES["Epic"] + CHANCES["Rare"] + CHANCES["Uncommon"]:
        prarity = "Uncommon"
    else:
        prarity = "Common"
    return prarity

def pesca():
    limpar_tela()
    prarity = gerar_peixe()
    tempo = 5
    print("PESCA\n")
    print("PESCANDO: ", end="")
    for i in range(tempo):
        print(".", end="", flush=True)
        time.sleep(tempo / 10)
        if i == tempo - 1:
            print("\n")
    peixe = random.randint(0,(len(PEIXES[prarity]) - 1))
    print(f"[{prarity}]\n{PEIXES[prarity][peixe]}\n")
    os.system("pause")

startup()
while(True):
    option = -1
    while(option < 0 or option > MAX_OPTIONS or option != 999):
        limpar_tela()
        print("MENU")
        print("[1] PESCA")
        print("[2] INVENTARIO")
        print("[3] LOJA")
        print("[4] HABILIDADES")
        print("[0] FINALIZAR JOGO")
        option = int(input("\nESCOLHA: "))
    if (option == 0):
        limpar_tela()
        print("OBRIGADO POR JOGAR!\n")
        break
    elif (option == 1):
        pesca()
    elif (option == 999):
        print("DEBUG RARIDADES")
        CHANCES = calcular_raridades()
        print("Secret: {}\nLegendary: {}\nEpic: {}\nRare: {}\nUncommon: {}\nCommon: {}\n".format(CHANCES["Secret"], CHANCES["Legendary"], CHANCES["Epic"], CHANCES["Rare"], CHANCES["Uncommon"], CHANCES["Common"]))
        os.system("pause")