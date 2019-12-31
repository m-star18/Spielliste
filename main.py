import os
from PIL import Image
import PySimpleGUI as sg

FONT_SIZE = [0, 20]

GAME_NAME_DATA_NUMBER = 0
COMPANY_NAME_DATA_NUMBER = 1
DATE_BIRTH_DATA_NUMBER = 2
IMAGE_DATA_NUMBER = 3
SITE_DATA_NUMBER = 4
NUMBER_DATA_PER = 5
ONE_COLUMN_LENGTH = 10
SEARCH_NUMBER = 9999

MAX_IMAGE_WIDTH_SIZE = 1000
MAX_IMAGE_HEIGHT_SIZE = 1000


def image_resize(image, game_image_data):
    image_size = image.resize((image.width // 2, image.height // 2))
    image_size.save(game_image_data)


def open_file():
    with open('game_list.txt') as game_list:
        list_data = game_list.read().split()
    data_number = 0
    input_text = ''
    values_data = {}

    return list_data, len(list_data) // NUMBER_DATA_PER, data_number, input_text, values_data


def run_file(event_details, number, game_list_data):
    if event_details == number * NUMBER_DATA_PER + SITE_DATA_NUMBER:
        os.system("xdg-open '" + game_list_data[number * NUMBER_DATA_PER + SITE_DATA_NUMBER] + "'")
        exit()


def start_menu(sum_data_number, game_list_data, data_number, input_text, values_data):
    now_page_number = ONE_COLUMN_LENGTH * data_number
    next_page_number = sum_data_number
    previous_page = []
    next_page = []
    headings = ['ゲーム名', '詳細', '実行']

    if len(values_data) != 0 and values_data[0] == input_text:
        input_text = ''

    layout = [
        [sg.Text('検索', size=(20, 1), font=FONT_SIZE),
         sg.Input(size=(20, 1), font=FONT_SIZE, default_text=input_text),
         sg.Submit(button_text='検索', size=(20, 1), font=FONT_SIZE, key=10000)],
        [sg.Text(h, size=(20, 1), font=FONT_SIZE) for h in headings],
    ]

    for i in range(now_page_number, now_page_number + min(ONE_COLUMN_LENGTH, sum_data_number - now_page_number)):
        layout += [
            [sg.Text(game_list_data[i * NUMBER_DATA_PER], size=(20, 1), font=FONT_SIZE),
             sg.Submit(button_text='詳細', size=(20, 1), font=FONT_SIZE, key=i * NUMBER_DATA_PER + SEARCH_NUMBER),
             sg.Submit(button_text='実行', size=(20, 1), font=FONT_SIZE, key=i * NUMBER_DATA_PER + SITE_DATA_NUMBER),
             ]
        ]
    # Determine if you need a button
    if data_number > 0:
        previous_page = [sg.Submit(button_text='前の10件', size=(30, 1), font=FONT_SIZE, key='previous')]

    if sum_data_number > now_page_number + ONE_COLUMN_LENGTH:
        # Adjust the position by putting in a space
        if now_page_number == 0:
            previous_page = [sg.Text(' ', size=(32, 1), font=FONT_SIZE)]

        next_page = [sg.Submit(button_text='次の10件', size=(30, 1), font=FONT_SIZE, key='next')]
        next_page_number = now_page_number + ONE_COLUMN_LENGTH

    layout += [previous_page + next_page,
               [sg.Text('{0}件のうち、　{1}から{2}件を表示しています'.format(sum_data_number, now_page_number, next_page_number),
                        size=(40, 1), font=FONT_SIZE),
                sg.Submit(button_text='絞り込み検索', size=(20, 1), font=FONT_SIZE, key='refinement')],
               ]

    return sg.Window('Game menu').Layout(layout)


def details_menu(game_list_data, number):
    image = Image.open(game_list_data[number * NUMBER_DATA_PER + IMAGE_DATA_NUMBER])

    if image.width >= MAX_IMAGE_WIDTH_SIZE or image.height >= MAX_IMAGE_HEIGHT_SIZE:
        image_resize(image, game_list_data[number * NUMBER_DATA_PER + IMAGE_DATA_NUMBER])

    headings_details = ['ゲーム名', '会社名', '登場年月', '実行']
    layout_details = [[sg.Text(h, size=(20, 1), font=FONT_SIZE) for h in headings_details]]

    layout_details += [[sg.Text(game_list_data[number * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER], size=(20, 1), font=FONT_SIZE),
                        sg.Text(game_list_data[number * NUMBER_DATA_PER + COMPANY_NAME_DATA_NUMBER], size=(20, 1), font=FONT_SIZE),
                        sg.Text(game_list_data[number * NUMBER_DATA_PER + DATE_BIRTH_DATA_NUMBER], size=(20, 1), font=FONT_SIZE),
                        sg.Submit(button_text='実行', size=(20, 1), font=FONT_SIZE, key=number * NUMBER_DATA_PER + SITE_DATA_NUMBER),
                        ],

                       [sg.Image(game_list_data[number * NUMBER_DATA_PER + IMAGE_DATA_NUMBER]),
                        ],
                       ]

    return sg.Window(game_list_data[number * NUMBER_DATA_PER] + 'の詳細').Layout(layout_details)


def refinements_menu(game_list_data, sum_data_number):
    layout_refinements = []
    company_data = [0] * sum_data_number
    date_birth_data = ['1970', '1980', '1990', '2000', '2010']

    for i in range(sum_data_number):
        company_data[i] = game_list_data[i * NUMBER_DATA_PER + COMPANY_NAME_DATA_NUMBER]
    # To avoid duplication
    layout_refinements += [[sg.Text('会社名', size=(10, 1), font=FONT_SIZE),
                            sg.Combo(values=list(set(company_data)), size=(20, 1), font=FONT_SIZE),
                            ],
                           [sg.Text('制作年代', size=(10, 1), font=FONT_SIZE),
                            sg.Combo(values=date_birth_data, size=(20, 1), font=FONT_SIZE),
                            sg.Text('年代', size=(5, 1), font=FONT_SIZE),
                            ],
                           [sg.Text('完了!', size=(10, 1), font=FONT_SIZE),
                            sg.Submit(button_text='検索！', size=(20, 1), font=FONT_SIZE, key='refinement'),
                            ],
                           ]

    window_refinements_menu = sg.Window('絞り込み検索').Layout(layout_refinements)

    while True:
        event_refinements, value_refinements = window_refinements_menu.Read()

        if event_refinements == 'refinement':
            for i in range(2):
                if value_refinements[i] == '':
                    value_refinements[i] = 'なし'

            return value_refinements, window_refinements_menu

        elif event_refinements is None:
            return '', window_refinements_menu


def refinements_check(values_data, game_list_data, sum_data_number):
    refinements_new_game_list_data = []
    refinements_new_sum_data_number = 0
    delete_number = []

    for i in range(sum_data_number):
        # Don't search for 'なし'
        if values_data[0] != 'なし' and values_data[0] != game_list_data[i * NUMBER_DATA_PER + COMPANY_NAME_DATA_NUMBER]:
            delete_number.append(i)

        if values_data[1] != 'なし' and not (int(values_data[1]) <= int(game_list_data[i * NUMBER_DATA_PER + DATE_BIRTH_DATA_NUMBER]) <= int(values_data[1]) + 9):
            delete_number.append(i)

    delete_number = list(set(delete_number))
    for i in range(sum_data_number):
        if i not in delete_number:
            for j in range(NUMBER_DATA_PER):

                refinements_new_game_list_data += [game_list_data[i * NUMBER_DATA_PER + j]]

            refinements_new_sum_data_number += 1

    # print(refinements_new_sum_data_number, refinements_new_game_list_data, values)

    return refinements_new_game_list_data, refinements_new_sum_data_number, values_data


def search_check(values_data, game_list_data, sum_data_number):
    search_new_game_list_data = []
    search_new_sum_data_number = 0

    if values_data[0] == '':
        search_new_game_list_data = game_list_data
        search_new_sum_data_number = sum_data_number

    else:
        for i in range(sum_data_number):
            if values_data[0] in game_list_data[i * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER]:
                for j in range(NUMBER_DATA_PER):
                    search_new_game_list_data += [game_list_data[i * NUMBER_DATA_PER + j]]

                search_new_sum_data_number += 1

    return search_new_game_list_data, search_new_sum_data_number


def event_check(event, values, values_data, game_list_data, data_number, sum_data_number, window):
    refinements_game_list_data = []
    refinements_sum_data_number = 0

    if event == 10000:
        refinements_game_list_data, refinements_sum_data_number = search_check(values, game_list_data, sum_data_number)

    elif event == 'refinement':
        values, window_refinements_menu = refinements_menu(game_list_data, sum_data_number)
        window_refinements_menu.close()
        values_data = values
        refinements_game_list_data, refinements_sum_data_number, values_data = refinements_check(values_data, game_list_data, sum_data_number)

    else:
        list_values = list(values.values())
        list_values_data = list(values_data.values())
        i, j, k = 0, 0, 0

        for i in range(len(list_values_data)):
            for j in range(sum_data_number):

                for k in range(NUMBER_DATA_PER):
                    if list_values_data[i] == game_list_data[j * NUMBER_DATA_PER + k] or list_values_data[i] == 'なし':
                        refinements_game_list_data, refinements_sum_data_number, values_data = refinements_check(values_data, game_list_data, sum_data_number)
                        break

                else:
                    continue
                break

            else:
                continue
            break

        if (i + 1 == len(list_values_data) and j + 1 == sum_data_number and k + 1 == NUMBER_DATA_PER) or list_values_data == []:
            for i in range(len(list_values)):
                for j in range(sum_data_number):

                    if list_values[i] in game_list_data[j * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER]:
                        refinements_game_list_data, refinements_sum_data_number = search_check(list_values, game_list_data, sum_data_number)
                        break

    if event == 'next':
        data_number += 1

    elif event == 'previous':
        data_number -= 1

    if refinements_sum_data_number <= ONE_COLUMN_LENGTH * data_number:
        data_number = 0

    window.close()
    return data_number, values_data, start_menu(refinements_sum_data_number, refinements_game_list_data, data_number, values[0], values_data)


def main():
    game_list_data, sum_data_number, data_number, input_text, values_data = open_file()
    window = start_menu(sum_data_number, game_list_data, data_number, input_text, values_data)

    while True:
        event, values = window.Read()

        for i in range(sum_data_number):
            if event == i * NUMBER_DATA_PER + SEARCH_NUMBER:
                window_details = details_menu(game_list_data, i)

                while True:
                    event_details, values_details = window_details.Read()
                    run_file(event_details, i, game_list_data)

                    if event_details is None:
                        break

            run_file(event, i, game_list_data)

        if event is None:
            break

        data_number, values_data, window = event_check(event, values, values_data, game_list_data, data_number, sum_data_number, window)


if __name__ == "__main__":
    main()
