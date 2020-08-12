from file import add_file, open_file, run_file, sum_number_data
from menu import add_menu, create_summary, details_menu
from const import (
    GAME_NAME_DATA_NUMBER,
    GENRE_NAME_DATA_NUMBER,
    DATE_BIRTH_DATA_NUMBER,
    COMPANY_NAME_DATA_NUMBER,
    IMAGE_DATA_NUMBER,
    SITE_DATA_NUMBER,
    NUMBER_DATA_PER,
)


def search_check(values, values_data, game_list_data, event):
    from main import main
    search_new_game_list_data = []
    game_list_number_data = GAME_NAME_DATA_NUMBER

    if event == 'search':
        if values[game_list_number_data] == '':
            main()

    else:
        game_list_number_data = event
        values_data = values[game_list_number_data]

    for i in range(sum_number_data(game_list_data)):
        if values[game_list_number_data] in game_list_data[i * NUMBER_DATA_PER + game_list_number_data]:
            for j in range(NUMBER_DATA_PER):
                search_new_game_list_data += [game_list_data[i * NUMBER_DATA_PER + j]]

    return search_new_game_list_data, values_data


def event_check(event, values, values_data, game_list_data, number_data, event_data, window):
    from main import main
    sum_number = sum_number_data(game_list_data)
    edit_data = []

    if event == 'next':
        number_data += 1
        window.close()
        main(game_list_data=game_list_data, values_data=values_data, number_data=number_data)

    elif event == 'previous':
        number_data -= 1
        window.close()
        main(game_list_data=game_list_data, values_data=values_data, number_data=number_data)

    elif event == '再読込':
        window.close()
        main()

    for i in range(sum_number):
        if event == game_list_data[i * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER]:
            event_data = event
            window['INPUT'].update(f'{event}を選択中')

        elif event_data == game_list_data[i * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER]:
            if event == '詳細':
                window_details = details_menu(game_list_data, i)

                while True:
                    event_details, values_details = window_details.Read()
                    run_file(event_details, i, game_list_data, window_details)

                    if event_details is None:
                        break

                break

            elif event == '削除':
                list_data, event_data = open_file(event=event, event_data=event_data)
                window.close()
                main()

            elif event == '編集':
                for j in range(NUMBER_DATA_PER):
                    edit_data.append(game_list_data[i * NUMBER_DATA_PER + j])
                # Editing is the same as the add menu
                event = '追加'
                break

    if event == 'search' or event == GENRE_NAME_DATA_NUMBER or event == DATE_BIRTH_DATA_NUMBER or event == COMPANY_NAME_DATA_NUMBER:
        window.close()
        game_list_data, event_data = open_file(event=event, event_data=event_data)
        search_game_list_data, values_data = search_check(values, values_data, game_list_data, event)
        main(game_list_data=search_game_list_data, values_data=values_data)

    elif event == '追加':
        item_name = ['タイトル', 'ジャンル', '発売年', '会社名', '最高得点', '画像ファイル', '実行ファイル']
        window_add = add_menu(item_name, edit_data)

        while True:
            event_add, values_add = window_add.Read()

            if event_add is None or event_add == 'Exit':
                break

            if values_add[SITE_DATA_NUMBER] == '':
                values_add[SITE_DATA_NUMBER] = 'site'

            if event_add == 'edit':
                if values_add[IMAGE_DATA_NUMBER] == '':
                    values_add[IMAGE_DATA_NUMBER] = edit_data[IMAGE_DATA_NUMBER]

                if values_add[SITE_DATA_NUMBER] == '':
                    values_add[SITE_DATA_NUMBER] = edit_data[SITE_DATA_NUMBER]

            for i in range(NUMBER_DATA_PER):
                if values_add[i] == '':
                    window_add['INPUT'].update(f'{item_name[i]}は必須項目です')
                    break
            else:
                if event_add == '追加':
                    add_file(values_add, game_list_data)
                    window_add.close()
                    window.close()
                    main()

                elif event_add == 'edit':
                    event = '削除'
                    list_data, event_data = open_file(event=event, event_data=event_data)
                    add_file(values_add, game_list_data)
                    window_add.close()
                    window.close()
                    main()

    elif event == '詳細' or event == '追加' or event == '編集' or event == '削除':
        window['INPUT'].update('ゲームを選択してください')

    return event_data
