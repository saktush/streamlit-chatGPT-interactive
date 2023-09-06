import sqlite3


class LocalDB:
    def __init__(self, db_file: str) -> None:
        """
        Constructor for the LocalDB class.

        Args:
            db_file (str): The path to the SQLite database file.
        """
        self.__db_file = db_file

    def __enter__(self):
        """
        Method to establish a connection to the SQLite database.

        Returns:
            cursor: The SQLite database cursor.
        """
        self.conn = sqlite3.connect(self.__db_file)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        """
        Method to commit the changes and close the database connection.

        Args:
            type: The type of exception (if any).
            value: The exception instance (if any).
            traceback: The traceback object (if any).
        """
        self.conn.commit()
        self.conn.close()
