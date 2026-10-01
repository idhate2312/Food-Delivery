# Paste the completed class definitions here.
from abc import ABC, abstractmethod

class User(ABC):

    def __init__(self, name, phone):
        self._name = name
        self._phone = phone
        self._wallet_balance = 0

    def add_to_wallet(self, amount):
        if amount > 0:
            self._wallet_balance += amount

    @abstractmethod
    def notify(self, message):
        pass

    @abstractmethod
    def display_profile(self):
        pass
