from . import settings
from sql_control.database import Database
from sql_control.utility import random_token, take_column, verify_password, hash_password_with_salt
from .type import *

import datetime as dt

class AuthDB(Database):
    def __init__(self, host=settings.host, port=settings.port, user=settings.user, pwd=settings.password, db_name=settings.db_name, states_file=settings.states_file):
        super().__init__(host, port, user, pwd, db_name, states_file)

    def check_client_exist(self, client_id: str):
        self.cursor.execute("SELECT `ID` FROM `client` WHERE `ID` = ?", (client_id,))
        if self.cursor.fetchone() is not None:
            self.last_status.setStatus("0")
            return True
        else:
            self.last_status.setStatus("1.1", (client_id,))
            return False
    
    def create_client(self, name: str, image: str, apply_by_user_id: str) -> str: # Return client_id (UUID)
        # 'image' is encoded by base64
        self.cursor.execute("INSERT INTO `client`(`Name`, `Image`, `Token`, `ApplyBy`) VALUES (?, ?, ?, ?) RETURNING `ID`", (name, image, random_token(64), apply_by_user_id))
        self.connection.commit()
        self.last_status.setStatus("0")
        return self.cursor.fetchone()[0]
    
    def remove_client(self, client_id: str):
        def_client = self.get_default_client()
        if client_id == def_client.id:
            self.last_status.setStatus("1.2", (client_id,))
            return

        self.cursor.execute("DELETE FROM `client` WHERE `ID` = ?", (client_id,))
        self.connection.commit()
        self.last_status.setStatus("0")
    
    def refresh_client(self, client_id: str):
        self.cursor.execute("UPDATE `client` SET `Token` = ? WHERE `ID` = ?", (random_token(64), client_id))
        self.connection.commit()
        self.last_status.setStatus("0")

    def get_clients(self, keys: list) -> list[list]:
        return self.select('client', keys)

    def get_clients_by_applyby(self, apply_by: str) -> list[str]:
        self.cursor.execute("SELECT `ID` FROM `client` WHERE `ApplyBy` = ?", (apply_by,))
        return take_column(self.cursor.fetchall(), 0)
    
    def get_data_by_client(self, client_id: str, key: str):
        self.cursor.execute(f"SELECT `{key}` FROM `client` WHERE `ID` = ?", (client_id,))
        return self.cursor.fetchone()[0]
    
    def update_data_by_client(self, client_id: str, key: str, value):
        self.cursor.execute(f"UPDATE `client` SET `{key}` = ? WHERE `ID` = ?", (value, client_id))
        self.connection.commit()
        self.last_status.setStatus("0")

    def get_token_by_client(self, client_id: str) -> str:
        return self.get_data_by_client(client_id, "Token")

    def verify_client(self, client_id: str, client_token: str):
        self.cursor.execute("SELECT `ID` FROM `client` WHERE `ID` = ? AND `Token` = ?", (client_id, client_token))
        if self.cursor.fetchone() is not None:
            self.last_status.setStatus("0")
            return True
        else:
            self.last_status.setStatus("1")
            return False
        
    def verify_client_by_applyby(self, client_id: str, apply_by: str):
        self.cursor.execute("SELECT `ID` FROM `client` WHERE `ID` = ? AND `ApplyBy` = ?", (client_id, apply_by))
        if self.cursor.fetchone() is not None:
            self.last_status.setStatus("0")
            return True
        else:
            self.last_status.setStatus("4", (client_id, apply_by))
            return False
        
    def get_client_content(self, client_id: str) -> Client | None:
        self.cursor.execute("SELECT `ID`, `Name`, `Image` FROM `client` WHERE `ID` = ?", (client_id,))
        result = self.cursor.fetchone()
        if result is not None:
            self.last_status.setStatus("0")
            return Client(*result)
        else:
            self.last_status.setStatus("1.1", (client_id,))
            return None
        
    def get_default_client(self) -> Client:
        return self.get_client_content(settings.default_client_id)
        
    def get_client_by_auth_code(self, auth_code: str) -> str:
        self.cursor.execute("SELECT `Client_ID` FROM `authenticating` WHERE `ID` = ?", (auth_code,))
        return self.cursor.fetchone()[0]
        
    def generate_auth_code(self, client_id: str = '', redirect_url: str = '') -> str:
        auth_code = random_token(64)
        expire_time = dt.datetime.now() + dt.timedelta(minutes=30)
        self.cursor.execute("INSERT INTO `authenticating`(`ID`, `State`, `Redirect_URL`, `Expire`, `Client_ID`) VALUES (?, ?, ?, ?, ?)", (auth_code, 'Unused', redirect_url, expire_time, client_id))
        self.connection.commit()
        self.last_status.setStatus("0")
        return auth_code
    
    def verify_auth_code(self, auth_code: str) -> bool: # Check expire time
        self.cursor.execute("SELECT `Expire`, `State` FROM `authenticating` WHERE `ID` = ?", (auth_code,))
        result = self.cursor.fetchone()
        if result is not None:
            if result[0] > dt.datetime.now() and result[1] == 'Unused':
                self.last_status.setStatus("0")
                self.update("authenticating", {"ID": auth_code}, {"State": "Used"})
                return True
            else:
                self.last_status.setStatus("3.2", (auth_code,))
                return False
        else:
            self.last_status.setStatus("3.1", (auth_code,))
            return False

    def get_redirect_url(self, auth_code: str) -> str:
        self.cursor.execute("SELECT `Redirect_URL` FROM `authenticating` WHERE `ID` = ?", (auth_code,))
        return self.cursor.fetchone()[0]
    
    def get_data_by_auth_email(self, auth_code: str, key: str):
        self.cursor.execute(f"SELECT `{key}` FROM `authenticating_email` WHERE `ID` = ?", (auth_code,))
        return self.cursor.fetchone()[0]
    
    def can_auth_email(self, account_id: str) -> bool:
        # Check if the newest generated auth id is expired in the table 'authenticating_email'
        self.cursor.execute("SELECT `Expire` FROM `authenticating_email` WHERE `CreateBy` = ? ORDER BY `Expire` DESC LIMIT 1", (account_id,))
        result = self.cursor.fetchone()
        if result is not None:
            if result[0] > dt.datetime.now():
                self.last_status.setStatus("0")
                return True
            else:
                waiting_time = (dt.datetime.now() - result[0]).seconds // 60
                self.last_status.setStatus("7.1", (waiting_time,))
                return False
            
    def generate_auth_email_code(self, account_id: str, email: str) -> str:
        auth_code = random_token(64)
        expire_time = dt.datetime.now() + dt.timedelta(minutes=120)
        self.cursor.execute("INSERT INTO `authenticating_email`(`ID`, `Expire`, `CreateBy`, `Email`) VALUES (?, ?, ?, ?, ?)", (auth_code, expire_time, account_id, email))
        self.connection.commit()
        self.last_status.setStatus("0")
        return auth_code
    
    def verify_auth_email_code(self, auth_code: str) -> bool:
        self.cursor.execute("SELECT `Expire` FROM `authenticating_email` WHERE `ID` = ?", (auth_code,))
        result = self.cursor.fetchone()
        if result is not None:
            if result[0] > dt.datetime.now():
                self.last_status.setStatus("0")
                return True
            else:
                self.last_status.setStatus("7.2", (auth_code,))
                return False
        else:
            self.last_status.setStatus("7.2")
            return False

    def exist_google_user(self, google_id: str) -> bool:
        self.cursor.execute("SELECT `ID` FROM `google_user` WHERE `ID` = ?", (google_id,))
        self.last_status.setStatus("0")
        return self.cursor.fetchone() is not None
    
    def add_google_user(self, guser: GoogleUser):
        self.cursor.execute("INSERT INTO `google_user`(`ID`, `Email`, `Name`, `Locale`, `Picture_URL`) VALUES (?, ?, ?, ?, ?)", (guser.id, guser.email, guser.name, guser.locale, guser.picture))
        self.connection.commit()
        self.last_status.setStatus("0")

    def update_google_user(self, guser: GoogleUser):
        self.cursor.execute("UPDATE `google_user` SET `Email` = ?, `Name` = ?, `Locale` = ?, `Picture_URL` = ? WHERE `ID` = ?", (guser.email, guser.name, guser.locale, guser.picture, guser.id))
        self.connection.commit()
        self.last_status.setStatus("0")

    def create_account(self) -> str:
        self.cursor.execute("INSERT INTO `account`(`Token`, `Resource_Token`) VALUES (?, ?) RETURNING `ID`", (random_token(128), random_token(64)))
        self.connection.commit()
        self.last_status.setStatus("0")
        return self.cursor.fetchone()[0]
    
    def set_password(self, account_id: str, password: str):
        hashed_password, salt = hash_password_with_salt(password)
        self.cursor.execute("UPDATE `account` SET `Password` = ?, `Password_Salt` = ? WHERE `ID` = ?", (hashed_password, salt, account_id))
        self.connection.commit()
        self.last_status.setStatus("0")

    def update_account(self, account_id: str, key: str, value):
        self.cursor.execute(f"UPDATE `account` SET `{key}` = ? WHERE `ID` = ?", (value, account_id))
        self.connection.commit()
        self.last_status.setStatus("0")

    def remove_account(self, account_id: str):
        # check if account is manager. if so, the count of manager must be more than 1
        if self.get_data_by_account(account_id, "Role") == "Manager":
            self.cursor.execute("SELECT COUNT(*) FROM `account` WHERE `Role` = 'Manager'")
            if self.cursor.fetchone()[0] == 1:
                self.last_status.setStatus("6", (account_id,))
                return

        self.cursor.execute("DELETE FROM `account` WHERE `ID` = ?", (account_id,))
        self.connection.commit()
        self.last_status.setStatus("0")

    def update_password(self, account_id: str, old: str, new: str):
        if self.verify_account_with_id(account_id, old):
            self.set_password(account_id, new)
            self.last_status.setStatus("0")
            return True
        else:
            self.last_status.setStatus("2")
            return False
    
    def verify_account(self, account_id: str, account_token: str) -> bool:
        self.cursor.execute("SELECT `ID` FROM `account` WHERE `ID` = ? AND `Token` = ?", (account_id, account_token))
        if self.cursor.fetchone() is not None:
            self.last_status.setStatus("0")
            return True
        else:
            self.last_status.setStatus("2.1", (account_id,))
            return False
        
    def verify_account_with_id(self, account_id: str, password: str) -> bool:
        self.cursor.execute("SELECT `Password`, `Password_Salt` FROM `account` WHERE `ID` = ?", (account_id,))
        result = self.cursor.fetchone()
        if result is None:
            self.last_status.setStatus("2")
            return False
        else:
            hashed_password = result[0]
            salt = result[1]
            if verify_password(password, hashed_password, salt):
                self.last_status.setStatus("0")
                return True
            else:
                self.last_status.setStatus("2")
                return False

    def verify_account_with_email(self, email: str, password: str) -> bool:
        self.cursor.execute("SELECT `Password`, `Password_Salt` FROM `account` WHERE `Email` = ?", (email,))
        result = self.cursor.fetchone()
        if result is None:
            self.last_status.setStatus("2")
            return False
        else:
            hashed_password = result[0]
            salt = result[1]
            if verify_password(password, hashed_password, salt):
                self.last_status.setStatus("0")
                return True
            else:
                self.last_status.setStatus("2")
                return False

    def verify_account_with_loginid(self, login_id: str, password: str) -> bool:
        self.cursor.execute("SELECT `Password`, `Password_Salt` FROM `account` WHERE `Login_ID` = ?", (login_id,))
        result = self.cursor.fetchone()
        if result is None:
            self.last_status.setStatus("2")
            return False
        else:
            hashed_password = result[0]
            salt = result[1]
            if verify_password(password, hashed_password, salt):
                self.last_status.setStatus("0")
                return True
            else:
                self.last_status.setStatus("2")
                return False
            
    def get_role(self, account_id: str) -> str:
        self.cursor.execute("SELECT `Role` FROM `account` WHERE `ID` = ?", (account_id,))
        return self.cursor.fetchone()[0]
    
    def get_accounts(self, keys: list) -> list[list]:
        return self.select('account', keys)
    
    def get_account_by_google_id(self, google_id: str) -> str:
        self.cursor.execute("SELECT `ID` FROM `account` WHERE `Google_ID` = ?", (google_id,))
        return self.cursor.fetchone()[0]

    def get_account_by_email(self, email: str) -> str:
        self.cursor.execute("SELECT `ID` FROM `account` WHERE `Email` = ?", (email,))
        return self.cursor.fetchone()[0]
    
    def get_account_by_loginid(self, login_id: str) -> str:
        self.cursor.execute("SELECT `ID` FROM `account` WHERE `Login_ID` = ?", (login_id,))
        return self.cursor.fetchone()[0]
    
    def get_token(self, account_id: str) -> str:
        self.cursor.execute("SELECT `Token` FROM `account` WHERE `ID` = ?", (account_id,))
        return self.cursor.fetchone()[0]
    
    def get_resource_token(self, account_id: str) -> str:
        self.cursor.execute("SELECT `Resource_Token` FROM `account` WHERE `ID` = ?", (account_id,))
        return self.cursor.fetchone()[0]
    
    def get_data_by_account(self, account_id: str, key: str):
        self.cursor.execute(f"SELECT `{key}` FROM `account` WHERE `ID` = ?", (account_id,))
        return self.cursor.fetchone()[0]
    
    def update_data_by_account(self, account_id: str, key: str, value):
        self.cursor.execute(f"UPDATE `account` SET `{key}` = ? WHERE `ID` = ?", (value, account_id))
        self.connection.commit()
        self.last_status.setStatus("0")

    def link_account_google_user(self, account_id: str, google_id: str):
        self.cursor.execute("UPDATE `account` SET `Google_ID` = ? WHERE `ID` = ?", (google_id, account_id))
        self.connection.commit()
        self.last_status.setStatus("0")

    def unlink_account_google_user(self, account_id: str):
        self.cursor.execute("UPDATE `account` SET `Google_ID` = NULL WHERE `ID` = ?", (account_id,))
        self.connection.commit()
        self.last_status.setStatus("0")

    def check_google_user_link_account(self, google_id: str) -> bool:
        self.cursor.execute("SELECT `ID` FROM `account` WHERE `Google_ID` = ?", (google_id,))
        self.last_status.setStatus("0")
        return self.cursor.fetchone() is not None
