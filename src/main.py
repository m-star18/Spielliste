from app import App


def main():
    app = App()
    while True:
        event, values = app.window.Read()
        if event is None:
            break

        app.get_event_check(event, values)


if __name__ == "__main__":
    main()
