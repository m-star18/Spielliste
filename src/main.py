from app import App


def main():
    app = App()
    while True:
        event, values = app.window.Read()
        app.get_event_check(event)

        if event is None:
            break


if __name__ == "__main__":
    main()
