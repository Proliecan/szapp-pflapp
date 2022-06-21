import sqlite3

class Connector:
    def __init__(self, db_name) -> None:
        self.connection = None
        self.cursor = None
        self.db_name = db_name
        self.is_connected = False

    # connect to the given DB
    def connect(self) -> None:
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row

            self.cursor = self.connection.cursor()

            self.is_connected = True
        
            print("DB connected!")
        except sqlite3.Error as e:
            print(e)

    # cursor execute class
    # needs more parameter to specify the SQL Query 
    # or: have SQL Query as parameter itself?
    def read_data(self, table: str) -> sqlite3.Cursor:
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor

    # writes data to DB from ESPs
    def write_data(self, data: list, columns: list, table: str) -> None:
        self.cursor.execute(f"""
                INSERT INTO {table} ({columns[0]}, {columns[1]}, {columns[2]}) VALUES ('{data[0]}', '{data[1]}', '{data[2]}');
            """)
        self.connection.commit()


    # closes the connection to the DB
    def close(self) -> None:
        self.connection.close()
        self.is_connected = False
        print("DB closed!")

    # destructor 
    def __del__(self) -> None:
        if self.is_connected:
            self.close()
        print("DB Connection closed, Object will be deleted")

    # string method, fancy printing
    def __str__(self) -> str:
        return f"Connector for DB: {self.db_name}\nis connected: {self.is_connected}"


if __name__ == "__main__":
    test_connector = Connector("database.db")
    print(test_connector)
    del test_connector

# ---------------
# Beschreibung:
# durch cursor.execute() mit SQL Befehl werden die Daten die gequeriet werden im cursor Objekt gespeichert
# Aufruf durch loop über cursor Objekt und row[SPALTENNAME]

# Tabellen: 
# 1. PLANTS
# 2. HUMIDITY

# Aufbau 1. PLANTS
# 4 Spalten: ID, Room, Name, Species

# Aufbau 2. HUMIDITY
# 3 Spalten: pId (Pflanzen ID), DateTime (YYYY-MM-DD HH:MM:SS.SSS), Humidity (in % INTEGER 0-100)


# Plan:
# 1. MOCK-Daten in DB zum Testen ✔
# 2. Auslesen testen

# Eindeutige Identifikation der einzelnen ESPs und Verbindung zwischen Plants Tabelle (eindeutige Identifikation) und den ESPs
# wenn manuell eine neue Pflanze hinzugefügt wird, wie wird das mit dem ESP verbunden?
# -----------------