import PySimpleGUI as sg
import os

FONT_SIZE = [0, 20]


def run_file(event_details, number, game_list_data):
    if event_details == number * 5 + 4:
        os.system("xdg-open '" + game_list_data[number * 5 + 4] + "'")
        exit()


def open_file():
    with open('game_list.txt') as game_list:
        list_data = game_list.read().split()
    data_number = 0

    return list_data, len(list_data), data_number


def start_menu(len_data, game_list_data, data_number):
    now_page_number = 10 * data_number
    previous_page = []
    next_page = []
    headings = ['ゲーム名', '詳細', '実行']
    layout = [[sg.Text(h, size=(20, 1), font=FONT_SIZE) for h in headings]]

    for i in range(now_page_number, now_page_number + min(10, len_data // 5 - now_page_number)):
        layout += [
            [sg.Text(game_list_data[i * 5], size=(20, 1), font=FONT_SIZE),
             sg.Submit(button_text='詳細', size=(20, 1), font=FONT_SIZE, key=i * 5),
             sg.Submit(button_text='実行', size=(20, 1), font=FONT_SIZE, key=i * 5 + 4),
             ]
        ]
    # Determine if you need a button
    if data_number > 0:
        previous_page = [sg.Submit(button_text='前の10件', size=(30, 1), font=FONT_SIZE, key='previous')]

    if len_data // 5 > now_page_number + 10:
        # Adjust the position by putting in a space
        if now_page_number == 0:
            previous_page = [sg.Text(' ', size=(32, 1), font=FONT_SIZE)]

        next_page = [sg.Submit(button_text='次の10件', size=(30, 1), font=FONT_SIZE, key='next')]

    layout += [previous_page + next_page]

    return sg.Window('Game').Layout(layout)


def details_menu(game_list_data, number):
    headings_details = ['ゲーム名', '会社名', '登場年月', '実行']
    layout_details = [[sg.Text(h, size=(20, 1), font=[0, 15]) for h in headings_details]]

    layout_details += [[sg.Text(game_list_data[number * 5], size=(20, 1), font=FONT_SIZE),
                        sg.Text(game_list_data[number * 5 + 1], size=(20, 1), font=FONT_SIZE),
                        sg.Text(game_list_data[number * 5 + 2], size=(20, 1), font=FONT_SIZE),
                        sg.Submit(button_text='実行', size=(20, 1), font=FONT_SIZE, key=number * 5 + 4),
                        ],

                       [sg.Image(game_list_data[number * 5 + 3], size=(1100, 147)),
                        ],
                       ]

    return sg.Window('b').Layout(layout_details)


def event_check(event, len_data, game_list_data, data_number, window):
    if event == 'next':
        data_number += 1

    elif event == 'previous':
        data_number -= 1

    window.close()
    return start_menu(len_data, game_list_data, data_number), data_number


def main():
    game_list_data, len_data, data_number = open_file()
    window = start_menu(len_data, game_list_data, data_number)

    while True:
        event, values = window.Read()
        window, data_number = event_check(event, len_data, game_list_data, data_number, window)

        for i in range(len_data // 5):
            if event == i * 5:
                window_details = details_menu(game_list_data, i)

                while True:
                    event_details, values_details = window_details.Read()
                    run_file(event_details, i, game_list_data)

                    if event_details is None:
                        break

            run_file(event, i, game_list_data)

        if event is None:
            break


if __name__ == "__main__":
    main()
