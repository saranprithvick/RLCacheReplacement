from abc import ABC, abstractmethod

class BasePolicy(ABC):
    @abstractmethod
    def access(self,block):
        pass
    @abstractmethod
    def victim(self):
        pass
    @abstractmethod
    def remove(self,block):
        pass
    @abstractmethod
    def insert(self,block):
        pass 