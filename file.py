import os

from const import (
    GAME_NAME_DATA_NUMBER,
    IMAGE_DATA_NUMBER,
    SITE_DATA_NUMBER,
    NUMBER_DATA_PER,
)


def image_resize(image, game_list_data, number):
    image_size = image.resize((500, 500))
    image_size.save(game_list_data[number * NUMBER_DATA_PER + IMAGE_DATA_NUMBER])


def open_file(event='', event_data=''):
    with open('game_list.txt') as game_list:
        list_data = game_list.read().split()

    if event == '削除':
        list_data = delete_file(list_data, event_data)

    return list_data, len(list_data) // NUMBER_DATA_PER, event_data


def run_file(event_details, number, game_list_data):
    if event_details == number * NUMBER_DATA_PER + SITE_DATA_NUMBER:
        os.system("xdg-open '" + game_list_data[number * NUMBER_DATA_PER + SITE_DATA_NUMBER] + "'")
        exit()


def delete_file(list_data, event_data):
    delete_line = []
    # Recreate the deleted list if any strings are in the list
    for i in range(len(list_data) // NUMBER_DATA_PER):
        if event_data != list_data[i * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER]:
            for j in range(NUMBER_DATA_PER):
                delete_line.append(list_data[i * NUMBER_DATA_PER + j])
    # Take the list line by line and output it to a file
    with open('game_list.txt', 'w', encoding='utf-8') as game_list:
        for i in range(len(delete_line) // NUMBER_DATA_PER):
            for j in range(NUMBER_DATA_PER):
                game_list.write(delete_line[i * NUMBER_DATA_PER + j] + ' ')

            game_list.write('\n')

    with open('game_list.txt') as game_list:
        list_data = game_list.read().split()

    return list_data


def add_file(values_add, game_list_data, sum_number_data):
    with open('game_list.txt', 'w', encoding='utf-8') as game_list:
        for i in range(sum_number_data):
            for j in range(NUMBER_DATA_PER):
                game_list.write(game_list_data[i * NUMBER_DATA_PER + j] + ' ')

            game_list.write('\n')

        for i in range(NUMBER_DATA_PER):
            game_list.write(values_add[i] + ' ')

        game_list.write('\n')
