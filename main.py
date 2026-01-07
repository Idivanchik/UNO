import random
from termcolor import colored
import copy
from typing import Final
import os


COLORS: Final = ["red", "blue", "green", "yellow"]


def set_up_the_game():
    common_types = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "Пропуск хода", "Разворот"]
    cards = []
    for k in range(2):
        for current_color in COLORS:
            for current_type in common_types:
                cards.append([current_type, current_color])
    for c in COLORS:
        cards.append(["0", c])
    for m in range(4):
        cards.append(["Смена цвета", "magenta"])
        cards.append(["+4", "magenta"])
    random.shuffle(cards)
    players_number = int(input("Введите количество игроков: \033[1;33m"))
    print("\033[0m", end="")
    players = {}
    for player_index in range(players_number):
        playername = input(f"Введите имя {colored(player_index + 1, "light_yellow")} игрока: \033[1;33m")
        print("\033[0m", end="")
        if playername:
            players[playername] = cards[0:6]
        else:
            players[f"{player_index + 1} {colored("игрок", "white")}"] = cards[0:6]
        cards = cards[6:]
    top = cards.pop(0)
    return players, top, cards


def check_players(players, players_tags):
    for p in players_tags:
        if players[p] == []:
            print(f"{colored(p, "light_yellow")} победил(а)!")
            players.pop(p)
            players_tags.remove(p)
            return True
    return False


def print_my_cards(players, player_index):
    print(f"Ваши карты: ", end="")
    for card in players[player_index]:
        print(colored(card[0], card[1]), end=" ")
    print()


def check_many_cards(cards, top):
    if len(cards) == 0:
        return True
    elif len(cards) == 1 and cards[0][0] == top[0]:
        return True
    elif len(cards) > 1 and cards[0][0] == top[0]:
        top = cards.pop(0)
        return check_many_cards(cards, top)
    else:
        return False


def do_a_turn(selected_cards, players, current_player, bank, top):
    for selected_card in selected_cards:
        players[current_player].remove(selected_card)
    bank.append(top)
    top = selected_cards.pop(-1)
    for card in selected_cards:
        bank.append(card)
    return top


def set_new_color(top):
    new_color = input("Введите цвет, который хотите установить (red, blue, yellow, green): \033[1;33m")
    print("\033[0m", end="")
    while new_color not in COLORS:
        new_color = input("Такого цвета нет.\nВведите цвет, который хотите установить (red, blue, yellow, green): \033[1;33m")
        print("\033[0m", end="")
    top[1] = new_color
    return top


def ask_for_cards(cards, bank, coll):
    if coll > len(cards):
        for card in bank:
            if card[0] == "+4" or card[0] == "Смена цвета":
                card[1] = "magenta"
            cards.append(card)
        bank = []
        random.shuffle(cards)
        return cards[:coll], cards
    elif coll == len(cards):
        new_cards = cards[:]
        for card in bank:
            if card[0] == "+4" or card[0] == "Смена цвета":
                card[1] = "magenta"
            cards.append(card)
        bank = []
        random.shuffle(cards)
        return new_cards, cards
    else:
        new_cards, cards = cards[:coll], cards[coll + 1:]
        return new_cards, cards


def main():
    os.system("cls")
    players, top, cards = set_up_the_game()
    players_tags = list(players.keys())
    bank = []
    a = random.randint(0, len(players_tags) - 1)
    b = 1
    next = 0
    skip = 0
    print(f"{colored(players_tags[a], "light_yellow")} ходит первым.")
    input(colored("(Нажмите Enter для начала игры)", "light_yellow"))
    os.system("cls")
    while len(players_tags) > 1:
        current_player = players_tags[a % len(players_tags)]
        flag = False
        if skip > 0:
            print(colored(current_player, "red") + colored(" пропускает ход.", "light_yellow"))
            flag = True
            skip -= 1
        elif next == 0:
            print(f"\n{colored(current_player, "light_yellow")} ходит.")
            input(colored(f"(Нажмите Enter для начала хода)", "light_yellow"))
            print()
            print_my_cards(players, current_player)
            print(f"Верхняя карта: {colored(top[0], top[1])}")
            selected_cards = [players[current_player][int(x) - 1] for x in input(f"Введите через пробел номера карт, которыми ходите или нажмите {colored("Enter", "light_yellow")} для того, чтобы взять карту: \033[1;33m").split()]
            print("\033[0m", end="")
            while True:
                if not selected_cards:
                    print()
                    new_card, cards = ask_for_cards(cards, bank, 1)
                    players[current_player].append(new_card[0])
                    print(colored("Вы взяли карту ", "light_yellow") + colored(players[current_player][-1][0], players[current_player][-1][1]) + colored(", она добавлена вам в руку.", "light_yellow"))
                    print_my_cards(players, current_player)
                    print(f"Верхняя карта: {colored(top[0], top[1])}")
                    selected_cards = [players[current_player][int(x) - 1] for x in input(f"Введите через пробел номера карт, которыми ходите или нажмите {colored("Enter", "light_yellow")} для того, чтобы взять карту: \033[1;33m").split()]
                    print("\033[0m")
                elif selected_cards[0][0] == "+4" and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    next += 4 * len(selected_cards)
                    print(colored("Следующий игрок будет вынужден взять ", "light_yellow") + colored(next, "red") + colored(" карт или превевести.", "light_yellow"))
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    top = set_new_color(top)
                    break
                elif (selected_cards[0][0] == top[0] == "+2" or (selected_cards[0][0] == "+2" and selected_cards[0][1] == top[1])) and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    next += 2 * len(selected_cards)
                    print(colored("Следующий игрок будет вынужден взять ", "light_yellow") + colored(next, "red") + colored(" карт или превевести.", "light_yellow"))
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    break
                elif (selected_cards[0][0] == top[0] == "Пропуск хода" or (selected_cards[0][0] == "Пропуск хода" and selected_cards[0][1] == top[1])) and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    skip += len(selected_cards)
                    if skip > len(players) - 1:
                        print(colored("Невозможно, чтобы следующие ", "light_yellow") + colored(skip, "red") + colored(" игроков пропустили ход.", "light_yellow"))
                        print(colored("Это число снижено до ", "light_yellow") + colored(len(players_tags) - 1, "red") + colored(" игроков.", "light_yellow"))
                        skip = len(players) - 1
                    else:
                        print(colored("Следующие ", "light_yellow") + colored(skip, "red") + colored(" игроков пропустят ход.", "light_yellow"))
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    break
                elif (selected_cards[0][0] == top[0] == "Разворот" or (selected_cards[0][0] == "Разворот" and selected_cards[0][1] == top[1])) and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    if len(selected_cards) % 2 == 0 and len(players_tags) > 2:
                        print(colored("Вы бросили ", "light_yellow") + colored("чётное", "red") + colored(" количество карт.", "light_yellow"), end=" ")
                        print(colored("Игра пойдёт ", "light_yellow") + colored("в том же", "red") + colored(" направлении.", "light_yellow"))
                    elif len(selected_cards) % 2 == 1 and len(players_tags) > 2:
                        print(colored("Вы бросили ", "light_yellow") + colored("нечётное", "red") + colored(" количество карт.", "light_yellow"), end=" ")
                        print(colored("Игра пойдёт ", "light_yellow") + colored("в противоположном", "red") + colored(" направлении.", "light_yellow"))
                        b = -b
                    else:
                        print(colored("В игре два игрока, поэтому вам будет предоставлен ещё один ход после завершения данного.", "light_yellow"))
                        a -= 1
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    break
                elif selected_cards[0][0] == "Смена цвета" and len(selected_cards) == 1:
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    top = set_new_color(top)
                    break
                elif (selected_cards[0][0] == top[0] or selected_cards[0][1] == top[1]) and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    break
                else:
                    print()
                    print(colored("Эти карты не подходят.", "light_yellow"))
                    selected_cards = [players[current_player][int(x) - 1] for x in input(f"Введите через пробел номера карт, которыми ходите или нажмите {colored("Enter", "light_yellow")} для того, чтобы взять карту: \033[1;33m").split()]
                    print("\033[0m", end="")
                    print()
        else:
            print(f"\n{colored(current_player, "light_yellow")} ходит.")
            input(colored(f"(Нажмите Enter для начала хода)", "light_yellow"))
            print()
            print(colored("Вы должны взять ", "light_yellow") + colored(next, "red") + colored(" карт или перевести.", "light_yellow"))
            print_my_cards(players, current_player)
            print(f"Верхняя карта: {colored(top[0], top[1])}")
            selected_cards = [players[current_player][int(x) - 1] for x in input(f"\nВведите через пробел номера карт, которыми вы переводите или нажмите {colored("Enter", "light_yellow")} для того, чтобы взять {next} карт: \033[1;33m").split()]
            print("\033[0m", end="")
            while True:
                print()
                if not selected_cards:
                    print(colored("Вы взяли карты: ", "light_yellow"), end="")
                    new_cards, cards = ask_for_cards(cards, bank, next)
                    for card in new_cards:
                        players[current_player].append(card)
                    for k in range(next - 1):
                        print(colored(players[current_player][-next + k][0], players[current_player][-next + k][1]), end=" ")
                    print(colored(players[current_player][-1][0], players[current_player][-1][1]), end=colored(".\n", "light_yellow"))
                    print_my_cards(players, current_player)
                    next = 0
                    break
                elif check_many_cards(copy.deepcopy(selected_cards), top):
                    if top[0] == "+2":
                        next += 2 * len(selected_cards)
                        top = do_a_turn(selected_cards, players, current_player, bank, top)
                    else:
                        next += 4 * len(selected_cards)
                        top = do_a_turn(selected_cards, players, current_player, bank, top)
                        top = set_new_color(top)
                    break
                else:
                    print(colored("Эти карты не подходят.", "light_yellow"))
                    selected_cards = [players[current_player][int(x) - 1] for x in input(f"\nВведите через пробел номера карт, которыми вы переводите или нажмите {colored("Enter", "light_yellow")} для того, чтобы взять {next} карт: \033[1;33m").split()]
                    print("\033[0m", end="")
                print()
        if not flag:
            print()
            input(colored("(Нажмите Enter для завершения хода)", "light_yellow"))
            os.system("cls")
        a += b
        check_players(players, players_tags)


if __name__ == "__main__":
    main()
