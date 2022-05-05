from __future__ import annotations

from enum import Enum

from constants import Responses


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"


class Person:

    def __init__(self, name: str, gender: Enum):
        self.name = name.capitalize()
        self.gender = gender
        self.mother = None
        self.spouse = None
        self.children = []

    def __set_mother(self, mother: Person):
        self.mother = mother

    def __is_mother(self) -> bool:
        if self.gender is Gender.FEMALE and self.spouse is not None:
            return True
        return False

    def set_spouse(self, spouse: Person):
        self.spouse = spouse
        spouse.spouse = self
        spouse.children = self.children

    @property
    def total_children(self):
        return len(self.children)

    def add_child(self, child: Person) -> Enum:
        if not self.__is_mother():
            return Responses.CHILD_ADDITION_FAILED

        self.children.append(child)
        child.__set_mother(mother=self)
        return Responses.CHILD_ADDITION_SUCCEEDED

    def add_children(self, children: list):
        for child in children:
            self.add_child(child)
