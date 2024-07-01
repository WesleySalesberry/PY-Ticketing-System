from database import create_connection, setup_database
from ui.main import MainApp


def main():
    conn = create_connection()
    setup_database(conn)

    app = MainApp(conn)
    app.mainloop()


if __name__ == "__main__":
    main()
