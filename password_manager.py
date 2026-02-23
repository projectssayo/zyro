from debugs import *
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
import json


class PasswordChecker:
    def __init__(self, hashed_pass: str, input_pass: str, config_path="config.json"):
        self.hashed_pass = hashed_pass
        self.input_pass = input_pass

        with open(config_path) as f:
            self.PEPPER = json.load(f)["PEPPER"]

        self.ph = PasswordHasher()

    def verify(self) -> bool:
        try:
            self.ph.verify(
                self.hashed_pass,
                f"{self.input_pass}{self.PEPPER}"
            )
            green("Password verified")
            return True

        except VerificationError:
            red("Password not verified")
            return False

        except Exception as e:
            red(f"Error : {e}")
            return False


class PasswordHashing:
    def __init__(self, raw_password,config_path="config.json"):
        self.raw_password = raw_password



        with open(config_path) as f:
            self.PEPPER = json.load(f)["PEPPER"]

        self.ph = PasswordHasher()

    def encrypt(self) -> str:
        try:
            green("password encrypted")
            return self.ph.hash(f"{self.raw_password}{self.PEPPER}")
        except Exception as e:
            red("password encryption failed")
            return ""
