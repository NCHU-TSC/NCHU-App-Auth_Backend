from utility.status import StatusCode

import mariadb as sql
from enum import Enum

class Database:
    class LogLevel(Enum):
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARN = "WARN"
        ERROR = "ERROR"
        CRITICAL = "CRITICAL"

    MAX_LOG_LENGTH = 16000

    def __init__(self, host, port, user, pwd, db_name, states_file):
        self.connection = sql.connect(host=host, port=port, user=user, password=pwd)
        self.cursor = self.connection.cursor()
        self.cursor.execute("USE `{}`".format(db_name))

        self.__logging = True
        self.__display_log = False

        self.last_status = StatusCode(states_file)

    def __del__(self):
        self.connection.close()

    def log_config(self, logging: bool = True, display: bool = False):
        self.__logging = logging
        self.__display_log = display

    def log(self, message, level: LogLevel = LogLevel.DEBUG):
        if self.__display_log:
            print(level.value, message)
        if self.__logging:
            raw_message = "{}".format(message)
            MAX_LOG_LENGTH = 16000
            for i in range(0, len(raw_message), MAX_LOG_LENGTH):
                self.cursor.execute("INSERT INTO `log`(`level`, `message`) VALUES (?, ?)", (level.value, raw_message[i : i+MAX_LOG_LENGTH]))
            
            self.connection.commit()

        return message
    
    def getLastStatus(self):
        return self.last_status
    
    def select(self, table: str, columns: list[str], condiction: dict[str] = None, order: list[str] = None, limit: int = None):
        """
        Select data from table with specific columns and condiction.
        (Please use this method carefully, it is not safe to use this method without any validation of user input.)
        """
        query = "SELECT {} FROM `{}`".format(", ".join(columns), table)
        if condiction is not None:
            query += " WHERE {}".format(" AND ".join(["{} = ?".format(key) for key in condiction.keys()]))
        if order is not None:
            query += " ORDER BY {}".format(", ".join(order))
        if limit is not None:
            query += " LIMIT {}".format(limit)
        
        if condiction is not None:
            self.cursor.execute(query, list(condiction.values()))
        else:
            self.cursor.execute(query)
        
        return self.cursor.fetchall()
    
    def insert(self, table: str, data: dict[str]):
        keys = list(data.keys())
        values = list(data.values())
        query = "INSERT INTO `{}`({}) VALUES ({})".format(table, ", ".join(keys), ", ".join(["?" for key in keys]))
        self.cursor.execute(query, values)
        self.connection.commit()
        self.last_status.setStatus("0")
        return self.cursor.lastrowid
    
    def update(self, table: str, condiction: dict[str], data: dict[str]):
        keys = list(data.keys())
        values = list(data.values())
        condiction_keys = list(condiction.keys())
        condiction_values = list(condiction.values())
        query = "UPDATE `{}` SET {} WHERE {}".format(table, ", ".join(["{} = ?".format(key) for key in keys]), " AND ".join(["{} = ?".format(key) for key in condiction_keys]))
        self.cursor.execute(query, values + condiction_values)
        self.connection.commit()
        self.last_status.setStatus("0")
