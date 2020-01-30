import PySimpleGUI as sg

from file import open_file
from check import event_check
from menu import main_menu, create_summary


def main(game_list_data=None, sum_number_data=0, event_data='', number_data=0, input_text='', values_data=None, genre_data=None, date_birth_data=None, company_data=None):
    if game_list_data is None:
        game_list_data, sum_number_data, event_data = open_file()

    if values_data is None:
        values_data = {}

    if (genre_data or date_birth_data or company_data) is None:
        genre_data, date_birth_data, company_data = create_summary(game_list_data, sum_number_data)

    sg.theme("Topanga")

    window = main_menu(sum_number_data, game_list_data, number_data, input_text, values_data, genre_data, date_birth_data, company_data)

    while True:
        event, values = window.Read()
        print(event, values, event_data, values_data)
        window['INPUT'].update('{0}を選択中'.format(event))

        if event is None:
            exit()

        event_data = event_check(event, values, values_data, game_list_data, number_data, event_data, sum_number_data, window)


if __name__ == "__main__":
    main()
