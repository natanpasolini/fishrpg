import time
import os
import random
import math

version = "A03a"

PLAYER_STATS = {
    "rod": 1,
    "str": 1,
    "luck": 1,
    "speed": 1,
    "money": 0,
    "level": 1,
    "max_level": 30,
    "xp": 0,
    "xplvlup": 2,
    "sp": 0,
    "sp_bought": 0
}

BASE_CHANCES = {
    "Secreto": 0.01,
    "Lendário": 0.1,
    "Épico": 2,
    "Raro": 7.9,
    "Incomum": 20,
    "Comum": 69.99
}

BASE_XP = {
    "Secreto": 100,
    "Lendário": 30,
    "Épico": 24,
    "Raro": 9,
    "Incomum": 3,
    "Comum": 1
}

PEIXES = {
    "Secreto": ["Megalodonte (Filhote)","Enguia Elétrica Titânica"],
    "Lendário": ["Pirarucu","Dourado (Rei do Rio)","Garoupa-verdadeira","Tubarão (Filhote)"],
    "Épico": ["Peixe Borboleta","Corvina","Robalo","Tainha"],
    "Raro": ["Pescadinha","Traíra","Parati"],
    "Incomum": ["Peixe Palhaco","Manjuba","Neon Cardinal","Peixe Agulhinha"],
    "Comum": ["Alga","Larva","Camarão","Lambari"]
}

FISHES_SIZES = {
    "Secreto": [500,1000],
    "Lendário": [100,130],
    "Épico": [40,60],
    "Raro": [12,40],
    "Incomum": [5,9],
    "Comum": [0,4]
}

PLAYER_FISHES = {
    "Secreto": {},
    "Lendário": {},
    "Épico": {},
    "Raro": {},
    "Incomum": {},
    "Comum": {}
}

SHOP_ITEMS = {
    "VARAS": {
        "Vara1": 10,
        "Vara2": 2
    },
    "POÇÕES": {
        "Poção 1": 2,
        "Poção 2": 4,
        "Poção 3": 0
    },
    "PONTOS": 100
}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def startup():
    limpar_tela()
    print("====================")
    print("\n  PY FISHING GAME")
    print(f"  v. {version}\n")
    print("====================")
    os.system("pause")

def refresh_player_stats():
    PLAYER_STATS["xplvlup"] = math.ceil((PLAYER_STATS["level"] + 1) * 3.75)
    level_inicial = PLAYER_STATS["level"]
    while (True):
        if PLAYER_STATS["xp"] >= PLAYER_STATS["xplvlup"] and PLAYER_STATS["level"] < PLAYER_STATS["max_level"]:
            PLAYER_STATS["level"] += 1
            PLAYER_STATS["xp"] -= PLAYER_STATS["xplvlup"]
            PLAYER_STATS["xplvlup"] = math.ceil((PLAYER_STATS["level"] + 1) * 3.75)
        else:
            level_final = PLAYER_STATS["level"]
            break
    if level_inicial != level_final:
        skill_points = 0
        for i in range(level_final - level_inicial):
            skill_points += 1
        limpar_tela()
        PLAYER_STATS["sp"] += skill_points
        print("LEVEL UP!")
        print(f"{level_inicial} --> {level_final}")
        print(f"+{skill_points} SKILL POINTS")
        time.sleep(0.4)
        os.system("pause")
    

def player_status_menu():
    print(f"NÍVEL: {PLAYER_STATS['level']}   FISH COINS: {PLAYER_STATS['money']}")
    barraXP = ""
    tamanho_total_barra = 16
    if PLAYER_STATS["xp"] > 0:
        dif = (PLAYER_STATS["xp"] * 100) / PLAYER_STATS["xplvlup"]
        if dif > 100:
            dif = 100
        blocos_preenchidos = int(tamanho_total_barra * (dif / 100))
        if blocos_preenchidos <= 0:
            blocos_preenchidos = 1
        blocos_vazios = tamanho_total_barra - blocos_preenchidos
        barraXP = ("■" * blocos_preenchidos) + ("□" * blocos_vazios)
    else:
        barraXP = "□" * tamanho_total_barra
    if PLAYER_STATS["level"] < PLAYER_STATS["max_level"]:
        print(f"XP: {barraXP} {PLAYER_STATS['xp']}/{PLAYER_STATS['xplvlup']}")
    else:
        print(f"XP: LVL MAX")

def calcular_raridades():
    rod_bonus = PLAYER_STATS["rod"] * 0.3
    str_bonus = PLAYER_STATS["str"] * 0.05
    luck_bonus = PLAYER_STATS["luck"] * 0.75
    BONUS_TOTAL = rod_bonus + str_bonus + luck_bonus
    CHANCES = BASE_CHANCES.copy()
    CHANCES["Comum"] = max(7, BASE_CHANCES["Comum"] - BONUS_TOTAL)
    BONUS_RECALCULADO = BASE_CHANCES["Comum"] - CHANCES["Comum"]
    if PLAYER_STATS["rod"] > 2:
        CHANCES["Incomum"] = max(10, BASE_CHANCES["Incomum"] - (BONUS_TOTAL - CHANCES["Comum"]))
        BONUS_RECALCULADO = (BASE_CHANCES["Comum"] - CHANCES["Comum"]) + (BASE_CHANCES["Incomum"] - CHANCES["Incomum"])
    if BONUS_RECALCULADO > 0:
        if PLAYER_STATS["rod"] < 2:
            CHANCES["Secreto"] += BONUS_RECALCULADO * 0.03
            CHANCES["Lendário"] += BONUS_RECALCULADO * 0.07
            CHANCES["Épico"] += BONUS_RECALCULADO * 0.15
            CHANCES["Raro"] += BONUS_RECALCULADO * 0.30
            CHANCES["Incomum"] += BONUS_RECALCULADO * 0.45
        else:
            CHANCES["Secreto"] += BONUS_RECALCULADO * 0.1
            CHANCES["Lendário"] += BONUS_RECALCULADO * 0.19
            CHANCES["Épico"] += BONUS_RECALCULADO * 0.25
            CHANCES["Raro"] += BONUS_RECALCULADO * 0.46
    return CHANCES

def gerar_peixe():
    CHANCES = calcular_raridades()
    prarity = ""
    x = random.uniform(0,100)
    if x <= CHANCES["Secreto"]:
        prarity = "Secreto"
    elif x <= CHANCES["Secreto"] + CHANCES["Lendário"]:
        prarity = "Lendário"
    elif x <= CHANCES["Secreto"] + CHANCES["Lendário"] + CHANCES["Épico"]:
        prarity = "Épico"
    elif x <= CHANCES["Secreto"] + CHANCES["Lendário"] + CHANCES["Épico"] + CHANCES["Raro"]:
        prarity = "Raro"
    elif x <= CHANCES["Secreto"] + CHANCES["Lendário"] + CHANCES["Épico"] + CHANCES["Raro"] + CHANCES["Incomum"]:
        prarity = "Incomum"
    else:
        prarity = "Comum"
    psize = random.uniform(FISHES_SIZES[prarity][0],FISHES_SIZES[prarity][1])
    pxp = random.randint(BASE_XP[prarity],math.ceil(BASE_XP[prarity]*1.3)) * PLAYER_STATS["rod"]
    return prarity, psize, pxp

def pesca():
    limpar_tela()
    prarity, psize, pxp = gerar_peixe()
    tempo = int((random.uniform(1,5) / (((PLAYER_STATS["str"] * 0.2) + (PLAYER_STATS["speed"] * 0.2))) * 2))
    print("PESCA\n")
    print("PESCANDO: ", end="")
    for i in range(5):
        print("■", end="", flush=True)
        time.sleep(tempo / 10)
    limpar_tela()
    print("PESCA\n")
    peixe = random.randint(0,(len(PEIXES[prarity]) - 1))
    pnome = PEIXES[prarity][peixe]
    if pnome not in PLAYER_FISHES[prarity]:
        PLAYER_FISHES[prarity][pnome] = psize
        x = 1
        for i in reversed(PEIXES):
            if i == prarity:
                xp_extra = 2 * x
                pxp += xp_extra
                print(f"NOVA DESCOBERTA! (+{xp_extra} XP)")
                break
            else:
                x += 1
    else:
        if psize > PLAYER_FISHES[prarity][pnome]:
            PLAYER_FISHES[prarity][pnome] = psize
            print("NOVO RECORDE!")
    print(f"[{prarity}]\n{pnome}\n{psize:.2f} cm")
    print(f"+{pxp} XP\n")
    PLAYER_STATS["xp"] += pxp
    os.system("pause")

def skill_menu():
    while(True):
        option = -1
        MELHORIAS = ["FORÇA", "VELOCIDADE", "SORTE"]
        MELHORIAS_STATS = ["str", "speed", "luck"]
        limpar_tela()
        print("MELHORIAS")
        print(f"PONTOS DISPONIVEIS: {PLAYER_STATS['sp']}\n")
        print(f"[1] FORÇA: {PLAYER_STATS['str']}\nDiminui a dificuldade de puxar um peixe de alta raridade")
        print(f"[2] VELOCIDADE: {PLAYER_STATS['speed']}\nDiminui o tempo de pesca")
        print(f"[3] SORTE: {PLAYER_STATS['luck']}\nAumenta a presença de peixes de alta raridade")
        print("[0] PARA VOLTAR")
        try:
            option = int(input("\nESCOLHA: "))
            if (option == 0):
                break
            elif (PLAYER_STATS["sp"] > 0):
                if (option <= 3):
                    try:
                        pontos = int(input("\nPONTOS A ATRIBUIR: "))
                        if pontos > PLAYER_STATS["sp"]:
                            print(f"VOCÊ NÃO TEM {pontos} PONTOS DISPONIVEIS.")
                            os.system("pause")
                        if pontos == 0:
                            continue
                        elif pontos <= PLAYER_STATS["sp"]:
                            limpar_tela()
                            print(f"ATRIBUIR {pontos} EM {MELHORIAS[option - 1]}?")
                            try:
                                confirmacao = str(input("\n[S/N]: "))
                                if confirmacao.upper() == "S":
                                    PLAYER_STATS[MELHORIAS_STATS[option - 1]] += pontos
                                    PLAYER_STATS["sp"] -= pontos
                                elif confirmacao.upper() == "N":
                                    break
                            except ValueError:
                                confirmacao = ""
                    except ValueError:
                        pontos = -1
        except ValueError:
            option = -1

def shop_menu():
    while True:
        limpar_tela()
        print("LOJA")
        print(f"FISH COINS: {PLAYER_STATS['money']}\n")
        option = -1
        j = 0
        largura = 12
        o_pontos = -1
        for i in SHOP_ITEMS:
            j += 1
            if j % 2 != 0:
                espaco = largura - len(i)
                print(f"[{j}] {i}", end=f"", flush=True)
                print(" " * espaco, end="", flush=True)
            else:
                print(f"[{j}] {i}")
        print("\n[0] VOLTAR\n")
        try:
            option = int(input("ESCOLHA: "))
            if option == 0:
                break
            elif option <= len(SHOP_ITEMS):
                shop_option = list(SHOP_ITEMS)[option - 1]
                if shop_option != "Pontos":
                    for i in SHOP_ITEMS[shop_option]:
                        print(i, SHOP_ITEMS[shop_option][i])
                else:
                    while True:
                        limpar_tela()
                        if PLAYER_STATS["sp_bought"] >= 1:
                            preco_ponto = math.ceil(100 * (PLAYER_STATS["sp_bought"] * 1.3))
                        else:
                            preco_ponto = math.ceil(100 * (1 * 1.3))
                        print("PONTO DE MELHORIA")
                        print(f"FISH COINS: {PLAYER_STATS['money']}\n")
                        print(f"[PREÇO ATUAL: {preco_ponto}]\n")
                        print("O PREÇO AUMENTA EXPONENCIALMENTE A CADA PONTO COMPRADO!")
                        print("DIGITE A QUANTIDADE QUE DESEJA COMPRAR (0 RETORNA)\n")
                        try:
                            option = int(input("QUANTIDADE: "))
                            if option == 0:
                                break
                            elif option > 0:
                                limpar_tela()
                                x = PLAYER_STATS["sp_bought"]
                                y = option
                                for i in range(y):
                                    x += 1
                                preco_ponto = math.ceil(100 * (x * 1.3))
                                print("PONTO DE MELHORIA\n")
                                print(f"FISH COINS: {PLAYER_STATS['money']}\n")
                                print(f"COMPRAR {y} PONTOS POR [{preco_ponto} FC]?")
                                try:
                                    option = str(input("[S/N]: "))
                                    option = option.upper()
                                    if option == "S":
                                        if PLAYER_STATS["money"] >= preco_ponto:
                                            PLAYER_STATS["money"] -= preco_ponto
                                            PLAYER_STATS["sp"] += y
                                        else:
                                            print("VOCÊ NÃO TEM DINHEIRO SUFICIENTE")
                                            time.sleep(0.4)
                                    elif option == "N":
                                        continue
                                except ValueError:
                                    option = -1
                        except ValueError:
                            option = -1
        except ValueError:
            option = -1

startup()
while(True):
    option = -1
    refresh_player_stats()
    limpar_tela()
    print(f"PY FISH GAME v.{version}\n")
    player_status_menu()
    print("\n[1] PESCA       [2] CÓDEX")
    print("[3] LOJA        [4] MELHORIAS")
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
                print(f"{str(i).upper()} [{len(PLAYER_FISHES[i])}/{len(PEIXES[i])}]")
                for k in range(len(j)):
                    if j[k] in PLAYER_FISHES[i]:
                        print(f"[{j[k]} - {PLAYER_FISHES[i][j[k]]:.2f} cm]", end=" ", flush=True)
                print("")
            os.system("pause")
        elif (option == 3):
            shop_menu()
        elif (option == 4):
            skill_menu()
        elif (option == 999):
            print("\nDEBUG RARIDADES")
            CHANCES = calcular_raridades()
            print("Secreto: {}\nLendário: {}\nÉpico: {}\nRaro: {}\nIncomum: {}\nComum: {}\n".format(CHANCES["Secreto"], CHANCES["Lendário"], CHANCES["Épico"], CHANCES["Raro"], CHANCES["Incomum"], CHANCES["Comum"]))
            os.system("pause")
    except ValueError:
        option = -1