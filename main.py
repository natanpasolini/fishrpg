import time
import os
import random
import math
import json

version = "B03"

PLAYER_STATS = {
    "rod": 0,
    "str": 0,
    "max_str": 5,
    "luck": 0,
    "max_luck": 10,
    "money": 0,
    "level": 0,
    "max_level": 40,
    "xp": 0,
    "xplvlup": 2,
    "sp": 0,
    "potion_level": 1,
    "max_plevel": 5
}

PLAYER_INVENTORY = {
    "VARAS": ["GRAVETO"],
    "POÇÕES": {}
}

POTIONS_IN_USE = {
    "POÇÃO DA SORTE": [f"♧ {PLAYER_STATS['potion_level']}", 0],
    "POÇÃO DE FORÇA": [f"⛨ {PLAYER_STATS['potion_level']}", 0],
    "POÇÃO DE TAMANHO": [f"⇪ {PLAYER_STATS['potion_level']}", 0]
}

RODS_STATS = {
    "GRAVETO": {"luck": 0,"str": 0},
    "VARA SIMPLES": {"luck": 0.5,"str": 0.5},
    "VARA INCOMUM": {"luck": 1.2,"str": 1.6},
    "VARA RARA": {"luck": 2,"str": 2.3},
    "VARA ÉPICA": {"luck": 3,"str": 3},
    "VARA LENDÁRIA": {"luck": 5,"str": 5},
    "VARA SECRETA": {"luck": 10,"str": 10}
}

ITEMS_DESC = {
    "GRAVETO": f"NÃO OFERECE NENHUM BÔNUS",
    "VARA SIMPLES": f"+{RODS_STATS['VARA SIMPLES']['luck']} SORTE +{RODS_STATS['VARA SIMPLES']['str']} FORÇA",
    "VARA INCOMUM": f"+{RODS_STATS['VARA INCOMUM']['luck']} SORTE +{RODS_STATS['VARA INCOMUM']['str']} FORÇA",
    "VARA RARA": f"+{RODS_STATS['VARA RARA']['luck']} SORTE +{RODS_STATS['VARA RARA']['str']} FORÇA",
    "VARA ÉPICA": f"+{RODS_STATS['VARA ÉPICA']['luck']} SORTE +{RODS_STATS['VARA ÉPICA']['str']} FORÇA",
    "VARA LENDÁRIA": f"+{RODS_STATS['VARA LENDÁRIA']['luck']} SORTE +{RODS_STATS['VARA LENDÁRIA']['str']} FORÇA",
    "VARA SECRETA": f"+{RODS_STATS['VARA SECRETA']['luck']} SORTE +{RODS_STATS['VARA SECRETA']['str']} FORÇA",
    "POÇÃO DA SORTE": f"+{PLAYER_STATS['potion_level']} SORTE",
    "POÇÃO DE FORÇA": f"+{PLAYER_STATS['potion_level']} FORÇA",
    "POÇÃO DE TAMANHO": f"+{PLAYER_STATS['potion_level'] * 1.5} TAMANHO DE PEIXES"
}

BASE_CHANCES = {
    "Secreto": 0.2,
    "Lendário": 0.7,
    "Épico": 3,
    "Raro": 8,
    "Incomum": 20,
    "Comum": 68.1
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
        "VARA SIMPLES": [6,f"{ITEMS_DESC['VARA SIMPLES']}"],
        "VARA INCOMUM": [30,f"{ITEMS_DESC['VARA INCOMUM']}"],
        "VARA RARA": [90,f"{ITEMS_DESC['VARA RARA']}"]
    },
    "POÇÕES": {
        "POÇÃO DA SORTE": [70,f"{ITEMS_DESC["POÇÃO DA SORTE"]}"],
        "POÇÃO DE FORÇA": [50,f"{ITEMS_DESC["POÇÃO DE FORÇA"]}"],
        "POÇÃO DE TAMANHO": [200,f"{ITEMS_DESC["POÇÃO DE TAMANHO"]}"]
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
    for key in POTIONS_IN_USE:
        emoji = POTIONS_IN_USE[key][0].split()[0]
        POTIONS_IN_USE[key][0] = f"{emoji} {PLAYER_STATS['potion_level']}"
    for i in ITEMS_DESC:
        if i.split()[0] == "POÇÃO":
            if i.split()[2] == "TAMANHO":
                modificador = 1.5
            else:
                modificador = 1
            ITEMS_DESC[i] = ITEMS_DESC[i].replace(f"{ITEMS_DESC[i].split()[0]}", f"+{PLAYER_STATS['potion_level'] * modificador}")
    for i in SHOP_ITEMS["POÇÕES"]:
        SHOP_ITEMS["POÇÕES"][i][1] = f"{ITEMS_DESC[i]}"

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
    potions = POTIONS_IN_USE
    j = 0
    pUse = 0
    for i in potions:
        if potions[i][1] > 0:
            pUse += 1
    for i in potions:
        if potions[i][1] > 0:
            j += 1
            if j != pUse:
                print(f"[{potions[i][0]} x{potions[i][1]}]", end=" ", flush=True)
            else:
                print(f"[{potions[i][0]} x{potions[i][1]}]")

def calcular_raridades():
    rod_bonus = RODS_STATS[list(RODS_STATS)[PLAYER_STATS["rod"]]]["luck"] * 1.7
    luck_bonus = PLAYER_STATS["luck"] * 3
    if POTIONS_IN_USE["POÇÃO DA SORTE"][1] >= 1:
        POTIONS_IN_USE["POÇÃO DA SORTE"][1] -= 1
        luck_bonus += PLAYER_STATS["potion_level"] * 3
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
    if POTIONS_IN_USE["POÇÃO DE TAMANHO"][1] >= 1:
        POTIONS_IN_USE["POÇÃO DE TAMANHO"][1] -= 1
        psize *= PLAYER_STATS["potion_level"] * 1.5
    indice = 0
    for i in reversed(PEIXES):
        if i == prarity:
            break
        else:
            indice += 1
    pprice = random.uniform(0,2) * (psize * 0.3) + 3 * (indice * 3)
    pxp = random.randint(BASE_XP[prarity],math.ceil(BASE_XP[prarity]*1.3))
    return prarity, psize, pxp, pprice

def pesca_especiais(prarity):
    item_pescado = False
    if prarity == "Épico":
        if "VARA ÉPICA" not in PLAYER_INVENTORY["VARAS"]:
            x = random.randint(0,100)
            if x <= 30:
                item_pescado = True
                PLAYER_INVENTORY["VARAS"].append("VARA ÉPICA")
                print("VOCÊ ENCONTROU A VARA ÉPICA!")
            else:
                item_pescado = False
    elif prarity == "Lendário":
        if "VARA LENDÁRIA" not in PLAYER_INVENTORY["VARAS"]:
            x = random.randint(0,100)
            if x <= 30:
                item_pescado = True
                PLAYER_INVENTORY["VARAS"].append("VARA LENDÁRIA")
                print("VOCÊ ENCONTROU A VARA LENDÁRIA!")
            else:
                item_pescado = False
    elif prarity == "Secreto":
        if "VARA SECRETA" not in PLAYER_INVENTORY["VARAS"]:
            x = random.randint(0,100)
            if x <= 50:
                item_pescado = True
                PLAYER_INVENTORY["VARAS"].append("VARA SECRETA")
                print("VOCÊ ENCONTROU A VARA SECRETA!")
            else:
                item_pescado = False
    return item_pescado

def pesca():
    limpar_tela()
    prarity, psize, pxp, pprice = gerar_peixe()
    if PLAYER_STATS["str"] > 0:
        if PLAYER_STATS["str"] == 1:
            tempo_r = 0.85
        else:
            if POTIONS_IN_USE["POÇÃO DE FORÇA"][1] >= 1:
                POTIONS_IN_USE["POÇÃO DE FORÇA"][1] -= 1
                adicionais = RODS_STATS[list(RODS_STATS)[PLAYER_STATS["rod"]]]["str"] + PLAYER_STATS["potion_level"]
            else:
                adicionais = RODS_STATS[list(RODS_STATS)[PLAYER_STATS["rod"]]]["str"]
            tempo_r = (PLAYER_STATS["str"] + adicionais) * 0.5
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
    item_pescado = pesca_especiais(prarity)
    if item_pescado == False:
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
    if PLAYER_STATS["potion_level"] > 0:
            dif = (PLAYER_STATS["potion_level"] * 100) / PLAYER_STATS["max_plevel"]
            if dif > 100:
                dif = 100
            blocos_preenchidos = int(PLAYER_STATS["max_plevel"] * (dif / 100))
            if blocos_preenchidos <= 0:
                blocos_preenchidos = 1
            blocos_vazios = PLAYER_STATS["max_plevel"] - blocos_preenchidos
            barraPotion = ("▮" * blocos_preenchidos) + ("▯" * blocos_vazios)
    else:
        barraPotion = "▯" * PLAYER_STATS["max_plevel"]
    return barraLuck, barraStr, barraPotion

def skill_menu():
    while(True):
        option = -1
        MELHORIAS = ["FORÇA", "SORTE", "POÇÃO"]
        MELHORIAS_STATS = ["str", "luck", "potion_level"]
        MELHORIAS_STATS_MAX = ["max_str", "max_luck", "max_plevel"]
        limpar_tela()
        barraLuck, barraStr, barraPotion = skill_menu_barras()
        print("MELHORIAS")
        print(f"PONTOS DISPONIVEIS: {PLAYER_STATS['sp']}\n")
        if PLAYER_STATS["str"] < PLAYER_STATS["max_str"]:
            print(f"[1] FORÇA: {barraStr} [{1+PLAYER_STATS['str']}]")
        else:
            print(f"[1] FORÇA: {barraStr}")
        print("Diminui o tempo de pesca.")
        if PLAYER_STATS["luck"] < PLAYER_STATS["max_luck"]:
            print(f"[2] SORTE: {barraLuck} [1]")
        else:
            print(f"[2] SORTE: {barraLuck}")
        print("Aumenta a presença de peixes de alta raridade.")
        if PLAYER_STATS["potion_level"] < PLAYER_STATS["max_plevel"]:
            print(f"[3] POÇÕES: {barraPotion} [{2+PLAYER_STATS['potion_level']}]")
        else:
            print(f"[3] POÇÕES: {barraPotion}")
        print("Aumenta o nível das poções.")
        print("[0] PARA VOLTAR")
        try:
            option = int(input("\nESCOLHA: "))
            if (option == 0):
                break
            elif (option < len(MELHORIAS) + 1):
                if (MELHORIAS_STATS[option - 1] == "str"):
                    custo = 1 + PLAYER_STATS[MELHORIAS_STATS[option - 1]]
                elif (MELHORIAS_STATS[option - 1] == "potion_level"):
                    custo = 2 + PLAYER_STATS[MELHORIAS_STATS[option - 1]]
                else:
                    custo = 1
                if (PLAYER_STATS[MELHORIAS_STATS[option - 1]] < PLAYER_STATS[MELHORIAS_STATS_MAX[option - 1]]):
                    if (PLAYER_STATS["sp"] > 0):
                        if PLAYER_STATS["sp"] >= custo:
                            PLAYER_STATS[MELHORIAS_STATS[option - 1]] += 1
                            PLAYER_STATS["sp"] -= custo
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
                        if i not in PLAYER_INVENTORY[shop_option] or shop_option == "POÇÕES":
                            custo = SHOP_ITEMS[shop_option][i][0]
                            fc = "FC"
                        elif shop_option != "POÇÕES":
                            custo = "COMPRADO"
                            fc = ""
                        if shop_option == "POÇÕES":
                            nome = i + f" {PLAYER_STATS['potion_level']}"
                        else:
                            nome = i
                        print(f"[{j}] {nome} - {custo} {fc}\n{SHOP_ITEMS[shop_option][i][1]}")
                    print("[0] VOLTAR\n")
                    try:
                        option = int(input("ESCOLHA: "))
                        if option == 0:
                            break
                        elif option <= len(SHOP_ITEMS[shop_option]):
                            item = list(SHOP_ITEMS[shop_option])[option - 1]
                            if shop_option != "POÇÕES":
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
                            else:
                                custo = SHOP_ITEMS[shop_option][list(SHOP_ITEMS[shop_option])[option - 1]][0]
                                qtd = 1
                                if PLAYER_STATS["money"] >= custo * qtd:
                                    PLAYER_STATS["money"] -= custo * qtd
                                    item = item.replace(f" {PLAYER_STATS['potion_level']}", "")
                                    if item not in PLAYER_INVENTORY[shop_option]:
                                        PLAYER_INVENTORY[shop_option][item] = 0
                                    PLAYER_INVENTORY[shop_option][item] += 1
                                    print(f"{qtd}x {item} ADQUIRIDO!")
                                    pausar_tela()
                                else:
                                    print("DINHEIRO INSUFICIENTE.")
                                    pausar_tela()
                    except ValueError:
                        option = -1
        except ValueError:
            option = -1

def codex_menu():
    while True:
        limpar_tela()
        print("INVENTÁRIO > CÓDEX\n")
        k = 0
        largura = 12
        for i in reversed(PEIXES):
            j = PEIXES[i]
            k += 1
            if k % 2 != 0:
                espaco = largura - len(i)
                print(f"[{k}] {str(i).upper()} [{len(PLAYER_FISHES[i])}/{len(PEIXES[i])}]", end=f"", flush=True)
                print(" " * espaco, end="", flush=True)
            else:
                print(f"[{k}] {str(i).upper()} [{len(PLAYER_FISHES[i])}/{len(PEIXES[i])}]")
        print("[0] VOLTAR\n")
        try:
            option = int(input("ESCOLHA: "))
            if option == 0:
                break
            if option <= len(PEIXES):
                limpar_tela()
                codex_option = list(reversed(PEIXES))[option - 1]
                print(f"INVENTÁRIO > CÓDEX > {codex_option.upper()}\n")
                for i in PEIXES[codex_option]:
                    if i in PLAYER_FISHES[codex_option]:
                        print(f"[{i} - {PLAYER_FISHES[codex_option][i]:.2f} cm]", end=" ", flush=True)
                print("\n[0] VOLTAR\n")
                try:
                    option = int(input("ESCOLHA: "))
                    if option == 0:
                        pass
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
        codex_number = len(PLAYER_INVENTORY) + 1
        print(f"[{codex_number}] CÓDEX")
        print("[0] VOLTAR\n")
        try:
            option = int(input("ESCOLHA: "))
            if option == 0:
                break
            elif option == codex_number:
                codex_menu()
            elif option <= len(PLAYER_INVENTORY):
                inv_option = list(PLAYER_INVENTORY)[option - 1]
                while True:
                    limpar_tela()
                    print(f"INVENTÁRIO > {inv_option}\n")
                    j = 0
                    for i in PLAYER_INVENTORY[inv_option]:
                        j +=1
                        if inv_option != "POÇÕES":
                            print(f"[{j}] {i}\n{ITEMS_DESC[i]}")
                        else:
                            if PLAYER_INVENTORY[inv_option][i] > 0:
                                print(f"[{j}] {PLAYER_INVENTORY[inv_option][i]}x {i} {PLAYER_STATS['potion_level']}\n{ITEMS_DESC[i.replace(f" {PLAYER_STATS['potion_level']}", "")]}")
                    print("[0] VOLTAR\n")
                    try:
                        if inv_option != "POÇÕES":
                            option = int(input("EQUIPAR: "))
                        else:
                            option = int(input("USAR: "))
                        if option == 0:
                            break
                        elif option <= len(PLAYER_INVENTORY[inv_option]):
                            if inv_option != "POÇÕES":
                                equipar = list(PLAYER_INVENTORY[inv_option])[option - 1]
                                for i in range(len(RODS_STATS)):
                                    if list(RODS_STATS)[i] == equipar:
                                        break
                                PLAYER_STATS["rod"] = i
                                print(f"{equipar} EQUIPADO!")
                                break
                            else:
                                equipar = list(PLAYER_INVENTORY[inv_option])[option - 1]
                                equipar = equipar.replace(f" {PLAYER_STATS['potion_level']}", "")
                                qtd = 1
                                PLAYER_INVENTORY[inv_option][equipar] -= qtd
                                POTIONS_IN_USE[equipar][1] += 1
                                print(f"{qtd}x {equipar} USADA!")
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

def salvar_jogo():
    pasta_save = "saves"
    caminho_arquivo = os.path.join(pasta_save, "save.json")
    os.makedirs(pasta_save, exist_ok=True)
    dados_para_salvar = {
        "PLAYER_STATS": PLAYER_STATS,
        "PLAYER_INVENTORY": PLAYER_INVENTORY,
        "PLAYER_FISHES": PLAYER_FISHES,
        "POTIONS_IN_USE": POTIONS_IN_USE
    }
    try:
        with open(caminho_arquivo, "w") as arquivo_save:
            json.dump(dados_para_salvar, arquivo_save, indent=4)
        print("JOGO SALVO COM SUCESSO!")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o jogo: {e}")
    pausar_tela()

def carregar_jogo():
    global PLAYER_STATS, PLAYER_INVENTORY, PLAYER_FISHES, POTIONS_IN_USE
    caminho_arquivo = os.path.join("saves", "save.json")
    try:
        with open(caminho_arquivo, "r") as arquivo_save:
            dados_carregados = json.load(arquivo_save)
            PLAYER_STATS.update(dados_carregados["PLAYER_STATS"])
            PLAYER_INVENTORY.update(dados_carregados["PLAYER_INVENTORY"])
            PLAYER_FISHES.update(dados_carregados["PLAYER_FISHES"])
            POTIONS_IN_USE.update(dados_carregados["POTIONS_IN_USE"])
            print("SAVE CARREGADO COM SUCESSO!")
            time.sleep(1.5)
    except FileNotFoundError:
        print("Nenhum save encontrado.")
        time.sleep(1.5)
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o jogo: {e}")
        time.sleep(1.5)

startup()
while(True):
    option = -1
    refresh_player_stats()
    limpar_tela()
    print(f"PY FISH GAME v.{version}\n")
    player_status_menu()
    print("\n[1] PESCAR      [2] INVENTÁRIO")
    print("[3] LOJA        [4] MELHORIAS")
    print("[5] SALVAR      [6] CARREGAR")
    print("[0] SAIR")
    try:
        option = int(input("\nESCOLHA: "))
        if (option == 0):
            print("OBRIGADO POR JOGAR!\n")
            break
        elif (option == 1):
            pesca()
        elif (option == 2):
            inventory_menu()
        elif (option == 3):
            shop_menu()
        elif (option == 4):
            skill_menu()
        elif (option == 5):
            salvar_jogo()
        elif (option == 6):
            carregar_jogo()
    except ValueError:
        option = -1