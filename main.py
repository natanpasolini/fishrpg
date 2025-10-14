import pandas as pd
import time
import os
import random

MAX_OPTIONS = 2

PLAYER_STATS = {
    "rod": 1,
    "str": 0,
    "luck": 0,
    "speed": 0,
}

BASE_CHANCES = {
    "Secret": 0.1,
    "Legendary": 1,
    "Epic": 4,
    "Rare": 10,
    "Uncommon": 24.9,
    "Common": 60,
}

PEIXES = {
    "Secret": ["Tubarao"],
    "Legendary": ["Peixe Morto-vivo"],
    "Epic": ["Peixe Borboleta"],
    "Rare": ["Salmao"],
    "Uncommon": ["Peixe Palhaco","Bota"],
    "Common": ["Carpa","Atum"]
}

def calcular_raridades():
    rod_bonus = PLAYER_STATS["rod"] * 0.3
    str_bonus = PLAYER_STATS["str"] * 0.05
    luck_bonus = PLAYER_STATS["luck"] * 0.2
    BONUS_TOTAL = rod_bonus + str_bonus + luck_bonus
    print(BONUS_TOTAL)
    CHANCES = BASE_CHANCES.copy()
    CHANCES["Common"] = max(7, BASE_CHANCES["Common"] - BONUS_TOTAL)
    BONUS_RECALCULADO = BASE_CHANCES["Common"] - CHANCES["Common"]
    if PLAYER_STATS["rod"] > 2:
        CHANCES["Uncommon"] = max(10, BASE_CHANCES["Uncommon"] - (BONUS_TOTAL - CHANCES["Common"]))
        BONUS_RECALCULADO = (BASE_CHANCES["Common"] - CHANCES["Common"]) + (BASE_CHANCES["Uncommon"] - CHANCES["Uncommon"])
    if BONUS_RECALCULADO > 0:
        if PLAYER_STATS["rod"] < 2:
            CHANCES["Secret"] += BONUS_RECALCULADO * 0.03
            CHANCES["Legendary"] += BONUS_RECALCULADO * 0.07
            CHANCES["Epic"] += BONUS_RECALCULADO * 0.15
            CHANCES["Rare"] += BONUS_RECALCULADO * 0.30
            CHANCES["Uncommon"] += BONUS_RECALCULADO * 0.45
        else:
            CHANCES["Secret"] += BONUS_RECALCULADO * 0.1
            CHANCES["Legendary"] += BONUS_RECALCULADO * 0.19
            CHANCES["Epic"] += BONUS_RECALCULADO * 0.25
            CHANCES["Rare"] += BONUS_RECALCULADO * 0.46
    return CHANCES

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
    while(option < 0):
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
        print("\nDEBUG RARIDADES")
        CHANCES = calcular_raridades()
        print("Secret: {}\nLegendary: {}\nEpic: {}\nRare: {}\nUncommon: {}\nCommon: {}\n".format(CHANCES["Secret"], CHANCES["Legendary"], CHANCES["Epic"], CHANCES["Rare"], CHANCES["Uncommon"], CHANCES["Common"]))
        os.system("pause")