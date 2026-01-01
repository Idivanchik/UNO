import random
import termcolor
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
    players_number = int(input("Введите количество игроков: "))
    players = {}
    for player_index in range(players_number):
        players[player_index] = cards[0:6]
        cards = cards[6:]
    top = cards.pop(0)
    return players, top, cards


def check_players(players, players_tags):
    for p in players_tags:
        if players[p] == []:
            print(f"Победил {p + 1} игрок!")
            players.pop(p)
            players_tags.remove(p)
            return True
    return False


def print_my_cards(players, player_index):
        print(f"Ваши карты: ", end="")
        for card in players[player_index]:
            print(termcolor.colored(card[0], card[1]), end=" ")
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
    new_color = input("Введите цвет, который хотите установить (red, blue, yellow, green): ")
    while new_color not in COLORS:
        new_color = input("Такого цвета нет.\nВведите цвет, который хотите установить (red, blue, yellow, green): ")
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
    print(f"Первым ходит {termcolor.colored(a + 1, "light_yellow")} игрок.")
    input(termcolor.colored("(Нажмите Enter для начала игры)", "light_yellow"))
    os.system("cls")
    while len(players_tags) > 1:
        current_player = players_tags[a % len(players_tags)]
        input(f"\nХодит {current_player + 1} игрок.\n{termcolor.colored("(Нажмите Enter для начала хода)", "light_yellow")}")
        if skip > 0:
            print_my_cards(players, current_player)
            print(f"Верхняя карта: {termcolor.colored(top[0], top[1])}")
            print("Вы пропускаете ход.")
            skip -= 1
        elif next == 0:
            print_my_cards(players, current_player)
            print(f"Верхняя карта: {termcolor.colored(top[0], top[1])}")
            selected_cards = [players[current_player][int(x) - 1] for x in input(f"Введите через пробел номера карт, которыми ходите или нажмите {termcolor.colored("Enter", "light_yellow")} для того, чтобы взять карту: ").split()]
            while True:
                if not selected_cards:
                    new_cards, cards = ask_for_cards(cards, bank, 1)
                    for card in new_cards:
                        players[current_player].append(card)
                    print(f"Вы взяли карту {termcolor.colored(players[current_player][-1][0], players[current_player][-1][1])}, она добавлена вам в руку.")
                    print_my_cards(players, current_player)
                    print(f"Верхняя карта: {termcolor.colored(top[0], top[1])}")
                    selected_cards = [players[current_player][int(x) - 1] for x in input(f"Введите через пробел номера карт, которыми ходите или нажмите {termcolor.colored("Enter", "light_yellow")} для того, чтобы взять карту: ").split()]
                elif selected_cards[0][0] == "+4" and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    next += 4 * len(selected_cards)
                    print(f"Следующий игрок будет вынужден взять {termcolor.colored(4 * len(selected_cards), "light_yellow")} карт или превевести.")
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    top = set_new_color(top)
                    break
                elif (selected_cards[0][0] == top[0] == "+2" or (selected_cards[0][0] == "+2" and selected_cards[0][1] == top[1])) and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    next += 2 * len(selected_cards)
                    print(f"Следующий игрок будет вынужден взять {termcolor.colored(2 * len(selected_cards), "light_yellow")} карт или превевести.")
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    break
                elif (selected_cards[0][0] == top[0] == "Пропуск хода" or (selected_cards[0][0] == "Пропуск хода" and selected_cards[0][1] == top[1])) and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    print(f"Следующие {termcolor.colored(len(selected_cards), "light_yellow")} игроков пропустят ход.")
                    skip += len(selected_cards)
                    top = do_a_turn(selected_cards, players, current_player, bank, top)
                    break
                elif (selected_cards[0][0] == top[0] == "Разворот" or (selected_cards[0][0] == "Разворот" and selected_cards[0][1] == top[1])) and check_many_cards(copy.deepcopy(selected_cards[1:]), selected_cards[0]):
                    if len(selected_cards) % 2 == 0 and len(players_tags) > 2:
                        print(f"Вы бросили {termcolor.colored("чётное", "light_yellow")} количество карт. Игра пойдёт {termcolor.colored("в том же", "light_yellow")} направлении.")
                    elif len(selected_cards) % 2 == 1 and len(players_tags) > 2:
                        print(f"Вы бросили {termcolor.colored("нечётное", "light_yellow")} количество карт. Игра пойдёт {termcolor.colored("в противоположном", "light_yellow")} направлении.")
                        b = -b
                    else:
                        print("В игре два игрока, поэтому вам будет предоставлен ещё один ход после завершения данного.")
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
                    print("Эти карты не подходят.")
                    selected_cards = [players[current_player][int(x) - 1] for x in input(f"Введите через пробел номера карт, которыми ходите или нажмите {termcolor.colored("Enter", "light_yellow")} для того, чтобы взять карту: ").split()]
        else:
            print(f"Вы должны взять {termcolor.colored(next, "light_yellow")} карт или перевести.")
            print_my_cards(players, current_player)
            print(f"Верхняя карта: {termcolor.colored(top[0], top[1])}")
            selected_cards = [players[current_player][int(x) - 1] for x in input(f"\nВведите через пробел номера карт, которыми вы переводите или нажмите {termcolor.colored("Enter", "light_yellow")} для того, чтобы взять {next} карт: ").split()]
            while True:
                if not selected_cards:
                    print("Вы взяли карты: ", end="")
                    new_cards, cards = ask_for_cards(cards, bank, next)
                    for card in new_cards:
                        players[current_player].append(card)
                    for k in range(next - 1):
                        print(termcolor.colored(players[current_player][-next + k][0], players[current_player][-next + k][1]), end=" ")
                    print(termcolor.colored(players[current_player][-1][0], players[current_player][-1][1]), end=".\n")
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
                    print("Эти карты не подходят.")
                    selected_cards = [players[current_player][int(x) - 1] for x in input(f"\nВведите через пробел номера карт, которыми вы переводите или нажмите {termcolor.colored("Enter", "light_yellow")} для того, чтобы взять {next} карт: ").split()]
        input(termcolor.colored("(Нажмите Enter для завершения хода)", "light_yellow"))
        os.system("cls")
        a += b
        check_players(players, players_tags)



if __name__ == "__main__":
    main()