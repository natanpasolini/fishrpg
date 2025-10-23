import time
import os
import random
import math

version = "A04c"

PLAYER_STATS = {
    "rod": 0,
    "str": 0,
    "max_str": 5,
    "luck": 0,
    "max_luck": 10,
    "money": 0,
    "level": 1,
    "max_level": 30,
    "xp": 0,
    "xplvlup": 2,
    "sp": 0
}

PLAYER_INVENTORY = {
    "VARAS": ["GRAVETO"],
    "POÇÕES": []
}

RODS_STATS = {
    "GRAVETO": {"luck": 0.1,"str": 0.05},
    "VARA COMUM": {"luck": 0.3,"str": 0.15},
    "VARA INCOMUM": {"luck": 0.6,"str": 0.3}
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
        "VARA COMUM": [2,f"+{RODS_STATS['VARA COMUM']['luck']} Sorte +{RODS_STATS['VARA COMUM']['str']} Força"],
        "VARA INCOMUM": [12,f"+{RODS_STATS['VARA INCOMUM']['luck']} Sorte +{RODS_STATS['VARA INCOMUM']['str']} Força"]
    },
    "POÇÕES": {
        "Poção 1": [3,"Não faz nada ainda..."]
    }
}

def pausar_tela():
    input("Pressione qualquer tecla para continuar...")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def startup():
    limpar_tela()
    print("====================")
    print("\n  PY FISHING GAME")
    print(f"  v. {version}\n")
    print("====================")
    pausar_tela()

def refresh_player_stats():
    PLAYER_STATS["xplvlup"] = math.ceil((PLAYER_STATS["level"] + 1) * 6.85)
    level_inicial = PLAYER_STATS["level"]
    while (True):
        if PLAYER_STATS["xp"] >= PLAYER_STATS["xplvlup"] and PLAYER_STATS["level"] < PLAYER_STATS["max_level"]:
            PLAYER_STATS["level"] += 1
            PLAYER_STATS["xp"] -= PLAYER_STATS["xplvlup"]
            PLAYER_STATS["xplvlup"] = math.ceil((PLAYER_STATS["level"] + 1) * 6.85)
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
        pausar_tela()

def player_status_menu():
    print(f"NÍVEL: {PLAYER_STATS['level']}   FISH COINS: {PLAYER_STATS['money']:.2f}")
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
        barraXP = ("▮" * blocos_preenchidos) + ("▯" * blocos_vazios)
    else:
        barraXP = "▯" * tamanho_total_barra
    if PLAYER_STATS["level"] < PLAYER_STATS["max_level"]:
        print(f"XP: {barraXP}  [{PLAYER_STATS['xp']}/{PLAYER_STATS['xplvlup']}]")
    else:
        print(f"XP: LVL MAX")

def calcular_raridades():
    rod_bonus = RODS_STATS[list(RODS_STATS)[PLAYER_STATS["rod"]]]["luck"] * 1.7
    luck_bonus = PLAYER_STATS["luck"] * 3
    BONUS_TOTAL = rod_bonus + luck_bonus
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
            CHANCES["Raro"] += BONUS_RECALCULADO * 0.35
            CHANCES["Incomum"] += BONUS_RECALCULADO * 0.40
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
    indice = 0
    for i in reversed(PEIXES):
        if i == prarity:
            break
        else:
            indice += 1
    pprice = random.uniform(0,2) * (psize * 0.3) + 3 * (indice * 3)
    pxp = random.randint(BASE_XP[prarity],math.ceil(BASE_XP[prarity]*1.3))
    return prarity, psize, pxp, pprice

def pesca():
    limpar_tela()
    prarity, psize, pxp, pprice = gerar_peixe()
    if PLAYER_STATS["str"] > 0:
        if PLAYER_STATS["str"] == 1:
            tempo_r = 0.85
        else:
            tempo_r = (PLAYER_STATS["str"] * 0.5)
    else:
        tempo_r = 0.7
    tempo = (10 / tempo_r)
    print("PESCA\n")
    print("PESCANDO: ", end="")
    for i in range(10):
        print("▮", end="", flush=True)
        time.sleep(tempo / 10)
    limpar_tela()
    print("PESCA\n")
    peixe = random.randint(0,(len(PEIXES[prarity]) - 1))
    pnome = PEIXES[prarity][peixe]
    xp_extra = 0
    if pnome not in PLAYER_FISHES[prarity]:
        PLAYER_FISHES[prarity][pnome] = psize
        x = 1
        for i in reversed(PEIXES):
            if i == prarity:
                xp_extra = 2 * x
                print(f"NOVA DESCOBERTA! (+{xp_extra} XP)")
                break
            else:
                x += 1
    else:
        if psize > PLAYER_FISHES[prarity][pnome]:
            PLAYER_FISHES[prarity][pnome] = psize
            print("NOVO RECORDE!")
    print(f"[{prarity}]\n{pnome}\n{psize:.2f} cm")
    print(f"+{pxp} XP  +{pprice:.2f} FISH COINS\n")
    PLAYER_STATS["xp"] += pxp + xp_extra
    PLAYER_STATS["money"] += pprice
    pausar_tela()

def skill_menu_barras():
    if PLAYER_STATS["luck"] > 0:
            dif = (PLAYER_STATS["luck"] * 100) / PLAYER_STATS["max_luck"]
            if dif > 100:
                dif = 100
            blocos_preenchidos = int(PLAYER_STATS["max_luck"] * (dif / 100))
            if blocos_preenchidos <= 0:
                blocos_preenchidos = 1
            blocos_vazios = PLAYER_STATS["max_luck"] - blocos_preenchidos
            barraLuck = ("▮" * blocos_preenchidos) + ("▯" * blocos_vazios)
    else:
        barraLuck = "▯" * PLAYER_STATS["max_luck"]
    if PLAYER_STATS["str"] > 0:
            dif = (PLAYER_STATS["str"] * 100) / PLAYER_STATS["max_str"]
            if dif > 100:
                dif = 100
            blocos_preenchidos = int(PLAYER_STATS["max_str"] * (dif / 100))
            if blocos_preenchidos <= 0:
                blocos_preenchidos = 1
            blocos_vazios = PLAYER_STATS["max_str"] - blocos_preenchidos
            barraStr = ("▮" * blocos_preenchidos) + ("▯" * blocos_vazios)
    else:
        barraStr = "▯" * PLAYER_STATS["max_str"]
    return barraLuck, barraStr

def skill_menu():
    while(True):
        option = -1
        MELHORIAS = ["FORÇA", "SORTE"]
        MELHORIAS_STATS = ["str", "luck"]
        MELHORIAS_STATS_MAX = ["max_str", "max_luck"]
        limpar_tela()
        barraLuck, barraStr = skill_menu_barras()
        print("MELHORIAS")
        print(f"PONTOS DISPONIVEIS: {PLAYER_STATS['sp']}\n")
        print(f"[1] FORÇA: {barraStr}")
        if PLAYER_STATS["str"] < PLAYER_STATS["max_str"]:
            print(f"Custo: {1+PLAYER_STATS['str']}")
        print("Diminui o tempo de pesca.")
        print(f"[2] SORTE: {barraLuck}")
        if PLAYER_STATS["luck"] < PLAYER_STATS["max_luck"]:
            print(f"Custo: 1")
        print("Aumenta a presença de peixes de alta raridade.")
        print("[0] PARA VOLTAR")
        try:
            option = int(input("\nESCOLHA: "))
            if (option == 0):
                break
            elif (option < len(MELHORIAS) + 1):
                if (MELHORIAS_STATS[option - 1] != "luck"):
                    custo = 1 + PLAYER_STATS[MELHORIAS_STATS[option - 1]]
                else:
                    custo = 1
                if (PLAYER_STATS[MELHORIAS_STATS[option - 1]] < PLAYER_STATS[MELHORIAS_STATS_MAX[option - 1]]):
                    if (PLAYER_STATS["sp"] > 0):
                        if PLAYER_STATS["sp"] >= custo:
                            PLAYER_STATS[MELHORIAS_STATS[option - 1]] += 1
                            PLAYER_STATS["sp"] -= 1
                        else:
                            print(f"VOCÊ NÃO POSSUI {custo} PONTOS DE MELHORIA")
                            time.sleep(0.3)
                            pausar_tela()
                    else:
                        print(f"VOCÊ NÃO POSSUI {custo} PONTOS DE MELHORIA")
                        time.sleep(0.3)
                        pausar_tela()
                else:
                    print(f"VOCÊ JÁ ATINGIU O MÁXIMO DE {MELHORIAS[option - 1]}")
                    time.sleep(0.3)
                    pausar_tela()
            else:
                print("OPÇÃO INVÁLIDA")
                pausar_tela()
        except ValueError:
            option = -1

def shop_menu():
    while True:
        limpar_tela()
        print("LOJA")
        print(f"FISH COINS: {PLAYER_STATS['money']:.2f}\n")
        option = -1
        j = 0
        largura = 12
        for i in SHOP_ITEMS:
            j += 1
            if j % 2 != 0:
                espaco = largura - len(i)
                print(f"[{j}] {i}", end=f"", flush=True)
                print(" " * espaco, end="", flush=True)
            else:
                print(f"[{j}] {i}")
        if len(SHOP_ITEMS) % 2 != 0:
            print("\n[0] VOLTAR\n")
        else:
            print("[0] VOLTAR\n")
        try:
            option = int(input("ESCOLHA: "))
            if option == 0:
                break
            elif option <= len(SHOP_ITEMS):
                shop_option = list(SHOP_ITEMS)[option - 1]
                while True:
                    limpar_tela()
                    print(f"LOJA > {shop_option}")
                    print(f"FISH COINS: {PLAYER_STATS['money']:.2f}\n")
                    j = 0
                    for i in SHOP_ITEMS[shop_option]:
                        j += 1
                        if i not in PLAYER_INVENTORY[shop_option]:
                            custo = SHOP_ITEMS[shop_option][i][0]
                            fc = "FC"
                        else:
                            custo = "COMPRADO"
                            fc = ""
                        print(f"[{j}] {i} - {custo} {fc}\n{SHOP_ITEMS[shop_option][i][1]}")
                    print("[0] VOLTAR\n")
                    try:
                        option = int(input("ESCOLHA: "))
                        if option == 0:
                            break
                        elif option <= len(SHOP_ITEMS[shop_option]):
                            item = list(SHOP_ITEMS[shop_option])[option - 1]
                            if item not in PLAYER_INVENTORY[shop_option]:
                                custo = SHOP_ITEMS[shop_option][list(SHOP_ITEMS[shop_option])[option - 1]][0]
                                if PLAYER_STATS["money"] >= custo:
                                    PLAYER_STATS["money"] -= custo
                                    PLAYER_INVENTORY[shop_option].append(item)
                                    print(f"{item} ADQUIRIDO!")
                                    pausar_tela()
                                else:
                                    print("DINHEIRO INSUFICIENTE.")
                                    pausar_tela()
                            else:
                                print("VOCÊ JÁ POSSUI ESTE ITEM.")
                                pausar_tela()
                    except ValueError:
                        option = -1
        except ValueError:
            option = -1

def inventory_menu():
    while True:
        option = -1
        limpar_tela()
        print("INVENTÁRIO\n")
        j = 0
        for i in PLAYER_INVENTORY:
            j += 1
            if i != "POÇÕES":
                if i == "VARAS":
                    item_equipado = 'rod'
                print(f"[{j}] {i} [EQUIPADO: {list(RODS_STATS)[PLAYER_STATS[item_equipado]]}]")
            else:
                print(f"[{j}] {i}")
        print("[0] VOLTAR\n")
        try:
            option = int(input("ESCOLHA: "))
            if option == 0:
                break
            elif option <= len(PLAYER_INVENTORY):
                limpar_tela()
                inv_option = list(PLAYER_INVENTORY)[option - 1]
                print(f"INVENTÁRIO > {inv_option}\n")
                j = 0
                for i in PLAYER_INVENTORY[inv_option]:
                    j +=1
                    if i == "GRAVETO":
                        print(f"[{j}] {i}\nNão oferece nenhum bônus.")
                    else:
                        print(f"[{j}] {i}\n{SHOP_ITEMS[inv_option][i][1]}")
                print("[0] VOLTAR\n")
                try:
                    option = int(input("EQUIPAR: "))
                    if option == 0:
                        continue
                    elif option <= len(PLAYER_INVENTORY[inv_option]):
                        equipar = list(PLAYER_INVENTORY[inv_option])[option - 1]
                        for i in range(len(PLAYER_INVENTORY[inv_option])):
                            if list(PLAYER_INVENTORY[inv_option])[i] == equipar:
                                break
                        PLAYER_STATS["rod"] = i
                        print(f"{equipar} EQUIPADO!")
                        pausar_tela()
                    else:
                        print("OPÇÃO INVÁLIDA")
                        pausar_tela()
                except ValueError:
                    option = -1
            else:
                print("OPÇÃO INVÁLIDA.")
                pausar_tela()
        except ValueError:
            option = -1

startup()
while(True):
    option = -1
    refresh_player_stats()
    limpar_tela()
    print(f"PY FISH GAME v.{version}\n")
    player_status_menu()
    print("\n[1] PESCAR      [2] CÓDEX")
    print("[3] LOJA        [4] MELHORIAS")
    print("[5] INVENTÁRIO")
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
            pausar_tela()
        elif (option == 3):
            shop_menu()
        elif (option == 4):
            skill_menu()
        elif (option == 5):
            inventory_menu()
        elif (option == 999):
            print("\nDEBUG RARIDADES")
            CHANCES = calcular_raridades()
            print("Secreto: {}\nLendário: {}\nÉpico: {}\nRaro: {}\nIncomum: {}\nComum: {}\n".format(CHANCES["Secreto"], CHANCES["Lendário"], CHANCES["Épico"], CHANCES["Raro"], CHANCES["Incomum"], CHANCES["Comum"]))
            pausar_tela()
    except ValueError:
        option = -1