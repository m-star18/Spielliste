from app import App


def main():
    app = App()
    while True:
        event, values = app.window.Read()
        app.window['INPUT'].update('{0}を選択中'.format(event))
        app.get_event_check(event)

        if event is None:
            break


if __name__ == "__main__":
    main()
