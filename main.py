import time
import os
import random
import math

version = "A01C"

PLAYER_STATS = {
    "rod": 1,
    "str": 0.5,
    "luck": 1,
    "speed": 0.5,
    "money": 5,
    "level": 1,
    "xp": 0,
    "xplvlup": 2,
    "sp": 0
}

BASE_CHANCES = {
    "Secret": 0.01,
    "Legendary": 0.1,
    "Epic": 2,
    "Rare": 7.9,
    "Uncommon": 20,
    "Common": 69.99
}

PEIXES = {
    "Secret": ["Megalodonte (Filhote)","Enguia Elétrica Titânica"],
    "Legendary": ["Pirarucu","Dourado (Rei do Rio)","Garoupa-verdadeira","Tubarão (Filhote)"],
    "Epic": ["Peixe Borboleta","Corvina","Robalo","Tainha"],
    "Rare": ["Pescadinha","Traíra","Parati"],
    "Uncommon": ["Peixe Palhaco","Manjuba","Neon Cardinal","Peixe Agulhinha"],
    "Common": ["Alga","Larva","Camarão","Lambari"]
}

FISHES_SIZES = {
    "Secret": [500,1000],
    "Legendary": [100,130],
    "Epic": [40,60],
    "Rare": [12,40],
    "Uncommon": [5,9],
    "Common": [0,4]
}

PLAYER_FISHES = {}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def startup():
    limpar_tela()
    print("====================")
    print("\n  PY FISHING GAME")
    print(f"  v. {version}\n")
    print("====================")
    os.system("pause")
    limpar_tela()

def player_status_menu():
    PLAYER_STATS["xplvlup"] = math.ceil((PLAYER_STATS["level"] + 1) * 3.75)
    print(f"NÍVEL: {PLAYER_STATS['level']}   DINHEIRO: {PLAYER_STATS['money']}")
    barraXP = ""
    tamanho_total_barra = 16
    if PLAYER_STATS["xp"] > 0:
        dif = (PLAYER_STATS["xp"] * 100) / PLAYER_STATS["xplvlup"]
        blocos_preenchidos = int(tamanho_total_barra * (dif / 100))
        if blocos_preenchidos <= 0:
            blocos_preenchidos = 1
        blocos_vazios = tamanho_total_barra - blocos_preenchidos
        barraXP = ("■" * blocos_preenchidos) + ("□" * blocos_vazios)
    else:
        barraXP = "□" * tamanho_total_barra
    print(f"XP: {barraXP} {PLAYER_STATS['xp']}/{PLAYER_STATS['xplvlup']}")

def calcular_raridades():
    rod_bonus = PLAYER_STATS["rod"] * 0.3
    str_bonus = PLAYER_STATS["str"] * 0.05
    luck_bonus = PLAYER_STATS["luck"] * 0.2
    BONUS_TOTAL = rod_bonus + str_bonus + luck_bonus
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

def gerar_peixe():
    CHANCES = calcular_raridades()
    prarity = ""
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
    psize = random.uniform(FISHES_SIZES[prarity][0],FISHES_SIZES[prarity][1])
    return prarity, psize

def pesca():
    limpar_tela()
    prarity, psize = gerar_peixe()
    tempo = int((random.uniform(1,5) / (PLAYER_STATS["str"] + PLAYER_STATS["speed"])))
    print("PESCA\n")
    print("PESCANDO: ", end="")
    for i in range(tempo):
        print("■", end="", flush=True)
        time.sleep(tempo / 10)
        if i == tempo - 1:
            print("\n")
    peixe = random.randint(0,(len(PEIXES[prarity]) - 1))
    peixeNome = PEIXES[prarity][peixe]
    if peixeNome not in PLAYER_FISHES:
        print("NOVA DESCOBERTA!")
        PLAYER_FISHES[peixeNome] = psize
    else:
        if psize > PLAYER_FISHES[peixeNome]:
            PLAYER_FISHES[peixeNome] = psize
            print("NOVO RECORDE!")
    print(f"[{prarity}]\n{peixeNome}\n{psize:.2f} cm")
    os.system("pause")

startup()
while(True):
    option = -1
    limpar_tela()
    print(f"PY FISH GAME v.{version}\n")
    player_status_menu()
    print("\n[1] PESCA       [2] CÓDEX")
    print("[3] LOJA        [4] HABILIDADES")
    print("[0] SAIR")
    try:
        option = int(input("\nESCOLHA: "))
        if (option == 0):
            print("OBRIGADO POR JOGAR!\n")
            break
        elif (option == 1):
            pesca()
        elif (option == 2):
            print("CÓDEX DE PEIXES")
            for i in reversed(PEIXES):
                j = PEIXES[i]
                print(f"{str(i).upper()}")
                for i in range(len(j)):
                    if j[i] in PLAYER_FISHES:
                        print(f"[{j[i]} - {PLAYER_FISHES[j[i]]:.2f} cm]", end=" ", flush=True)
                    else:
                        print("??????", end=" ", flush=True)
                print("")
            os.system("pause")
        elif (option == 3):
            print("NÃO DISPONÍVEL NESTA VERSÃO")
            os.system("pause")
        elif (option == 4):
            print("NÃO DISPONÍVEL NESTA VERSÃO")
            os.system("pause")
        elif (option == 999):
            print("\nDEBUG RARIDADES")
            CHANCES = calcular_raridades()
            print("Secret: {}\nLegendary: {}\nEpic: {}\nRare: {}\nUncommon: {}\nCommon: {}\n".format(CHANCES["Secret"], CHANCES["Legendary"], CHANCES["Epic"], CHANCES["Rare"], CHANCES["Uncommon"], CHANCES["Common"]))
            os.system("pause")
    except ValueError:
        option = -1