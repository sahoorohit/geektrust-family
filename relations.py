from abc import ABC, abstractmethod
from typing import List, Optional

from constants import Relations
from person import Gender, Person


class BaseRelation(ABC):
    def __init__(self, person: Person):
        self.person = person

    @abstractmethod
    def relatives(self) -> List[Person]:
        pass


class MotherOf(BaseRelation):
    def relatives(self) -> Optional[Person]:
        return self.person.mother


class FatherOf(BaseRelation):
    def relatives(self) -> Optional[Person]:
        mother = self.person.mother
        if not mother:
            return None

        return mother.spouse


class SiblingsOf(BaseRelation):
    def relatives(self) -> List[Person]:
        mother = self.person.mother
        if not mother:
            return []

        siblings = [child for child in mother.children if child.name != self.person.name]
        return siblings


class BrothersOf(BaseRelation):
    def relatives(self) -> List[Person]:
        siblings = SiblingsOf(self.person).relatives()
        brothers = [sibling for sibling in siblings if sibling.gender == Gender.MALE]
        return brothers


class SistersOf(BaseRelation):
    def relatives(self) -> List[Person]:
        siblings = SiblingsOf(self.person).relatives()
        sisters = [sibling for sibling in siblings if sibling.gender == Gender.FEMALE]
        return sisters


class SonsOf(BaseRelation):
    def relatives(self) -> List[Person]:
        sons = [child for child in self.person.children if child.gender == Gender.MALE]
        return sons


class DaughtersOf(BaseRelation):
    def relatives(self) -> List[Person]:
        daughters = [child for child in self.person.children if child.gender == Gender.FEMALE]
        return daughters


class PaternalUnclesOf(BaseRelation):
    def relatives(self) -> List[Person]:
        father = FatherOf(self.person).relatives()
        if not father:
            return []

        paternal_uncles = BrothersOf(father).relatives()
        return paternal_uncles


class PaternalAuntsOf(BaseRelation):
    def relatives(self) -> List[Person]:
        father = FatherOf(self.person).relatives()
        if not father:
            return []

        paternal_aunts = SistersOf(father).relatives()
        return paternal_aunts


class MaternalUnclesOf(BaseRelation):
    def relatives(self) -> List[Person]:
        mother = self.person.mother
        if not mother:
            return []

        maternal_uncles = BrothersOf(mother).relatives()
        return maternal_uncles


class MaternalAuntsOf(BaseRelation):
    def relatives(self) -> List[Person]:
        mother = self.person.mother
        if not mother:
            return []

        maternal_aunts = SistersOf(mother).relatives()
        return maternal_aunts


class BrothersInLawOf(BaseRelation):
    def relatives(self) -> List[Person]:
        brothers_in_law = []

        spouse = self.person.spouse
        if spouse:
            brothers_of_spouse = BrothersOf(spouse).relatives()
            brothers_in_law.extend(brothers_of_spouse)

        sisters = SistersOf(self.person).relatives()
        husbands_of_sisters = [sister.spouse for sister in sisters if sister.spouse]

        brothers_in_law.extend(husbands_of_sisters)
        return brothers_in_law


class SistersInLawOf(BaseRelation):
    def relatives(self) -> List[Person]:
        sisters_in_law = []

        brothers = BrothersOf(self.person).relatives()
        wives_of_brothers = [brother.spouse for brother in brothers if brother.spouse]
        sisters_in_law.extend(wives_of_brothers)

        spouse = self.person.spouse
        if spouse:
            sisters_of_spouse = SistersOf(spouse).relatives()
            sisters_in_law.extend(sisters_of_spouse)

        return sisters_in_law


RELATION_CLASS_PICKER = {
    Relations.Mother: MotherOf,
    Relations.Father: FatherOf,
    Relations.Siblings: SiblingsOf,
    Relations.Brother: BrothersOf,
    Relations.Sister: SistersOf,
    Relations.Son: SonsOf,
    Relations.Daughter: DaughtersOf,
    Relations.BrotherInLaw: BrothersInLawOf,
    Relations.SisterInLaw: SistersInLawOf,
    Relations.MaternalAunt: MaternalAuntsOf,
    Relations.PaternalAunt: PaternalAuntsOf,
    Relations.MaternalUncle: MaternalUnclesOf,
    Relations.PaternalUncle: PaternalUnclesOf
}
