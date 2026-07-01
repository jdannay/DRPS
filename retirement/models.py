from dataclasses import dataclass

@dataclass
class Person:
    name:str
    birth_year:int
    def age(self, year:int)->int:
        return year-self.birth_year

@dataclass
class Household:
    primary:Person
    spouse:Person
