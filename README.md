# 🎣 Py Fishing Game
Um simples e viciante jogo de pesca via terminal, desenvolvido em Python.

### 🌟 Funcionalidades
- **Sistema de Níveis e XP**: Ganhe experiência a cada peixe capturado e suba de nível para desbloquear melhorias.

- **Atributos e Melhorias**: Distribua pontos de habilidade para aumentar sua Força (pesca mais rápida) e Sorte (maior chance de peixes raros).

- **Inventário e Equipamentos**: Gerencie suas Varas e Poções. Equipe varas melhores para aumentar seus atributos.

- **Loja Completa**: Use seus Fish Coins ganhos para comprar novas varas e poções que auxiliam na sua jornada.

- **Múltiplas Raridades de Peixes**: Peixes são categorizados em raridades: Comum, Incomum, Raro, Épico, Lendário e até Secreto!

- **Códex de Peixes**: Um registro de todas as suas descobertas! O jogo salva seus maiores recordes de tamanho para cada espécie.

- **Itens Especiais**: Algumas varas especiais podem ser encontradas durante a pesca.

- **Sistema de Poções**: Utilize poções para obter bônus temporários de Sorte, Força ou para aumentar o tamanho dos peixes capturados.

- **Sistema de Save Local**: O jogo armazena o seu progresso em um arquivo json dentro da pasta saves.

### 🎮 Como Jogar
Baixe a Release mais recente em: https://github.com/natanpasolini/fishrpg/releases

#### OU

Clone o repositório:
```
git clone https://github.com/natanpasolini/fishrpg
```
Navegue até o diretório do projeto:
```
cd fishrpg
```
Execute o jogo:
```
python main.py
```

### 🛠️ Estrutura do Código
O jogo é construído em um único arquivo Python e utiliza dicionários para gerenciar os dados do jogador, itens, peixes e probabilidades.

- PLAYER_STATS: Armazena todos os atributos do jogador (nível, XP, dinheiro, etc.).

- PLAYER_INVENTORY: Controla os itens que o jogador possui.

- RODS_STATS, PEIXES, BASE_CHANCES: Dicionários que servem como "banco de dados" para os itens e mecânicas do jogo.

- Funções de Menu (main_menu, shop_menu, etc.): Controlam a navegação e a lógica da interface do usuário no terminal.

- Funções de Gameplay (pesca, calcular_raridades, gerar_peixe): Contêm a lógica principal do jogo.

- São utilizadas as seguintes bibliotecas: Math, Random, Os e Time.