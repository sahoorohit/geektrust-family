from enum import Enum
from typing import List, Optional, Union

from constants import Responses
from person import Gender, Person
from relations import RELATION_CLASS_PICKER


class Family:

    def __init__(self):
        self.members = []
        self.__initialize_family()

    def __initialize_family(self):
        shan = Person(name="shan", gender=Gender.MALE)
        anga = Person(name="anga", gender=Gender.FEMALE)
        anga.set_spouse(spouse=shan)

        chit = Person(name="chit", gender=Gender.MALE)
        ish = Person(name="ish", gender=Gender.MALE)
        vich = Person(name="vich", gender=Gender.MALE)
        aras = Person(name="aras", gender=Gender.MALE)
        satya = Person(name="satya", gender=Gender.FEMALE)
        anga.add_children(children=[chit, ish, vich, aras, satya])

        amba = Person(name="amba", gender=Gender.FEMALE)
        lika = Person(name="lika", gender=Gender.FEMALE)
        chitra = Person(name="chitra", gender=Gender.FEMALE)
        vyan = Person(name="vyan", gender=Gender.MALE)

        amba.set_spouse(spouse=chit)
        lika.set_spouse(spouse=vich)
        chitra.set_spouse(spouse=aras)
        satya.set_spouse(spouse=vyan)

        dritha = Person(name="dritha", gender=Gender.FEMALE)
        tritha = Person(name="tritha", gender=Gender.FEMALE)
        vritha = Person(name="vritha", gender=Gender.MALE)
        amba.add_children(children=[dritha, tritha, vritha])

        jaya = Person(name="jaya", gender=Gender.MALE)
        dritha.set_spouse(spouse=jaya)

        yodhan = Person(name="yodhan", gender=Gender.MALE)
        dritha.add_child(child=yodhan)

        vila = Person(name="vila", gender=Gender.FEMALE)
        chika = Person(name="chika", gender=Gender.FEMALE)
        lika.add_children(children=[vila, chika])

        jnki = Person(name="jnki", gender=Gender.FEMALE)
        ahit = Person(name="ahit", gender=Gender.MALE)
        chitra.add_children(children=[jnki, ahit])

        arit = Person(name="arit", gender=Gender.MALE)
        jnki.set_spouse(spouse=arit)

        laki = Person(name="laki", gender=Gender.MALE)
        lavnya = Person(name="lavnya", gender=Gender.FEMALE)
        jnki.add_children(children=[laki, lavnya])

        asva = Person(name="asva", gender=Gender.MALE)
        vyas = Person(name="vyas", gender=Gender.MALE)
        atya = Person(name="atya", gender=Gender.FEMALE)
        satya.add_children(children=[asva, vyas, atya])

        satvy = Person(name="satvy", gender=Gender.FEMALE)
        krpi = Person(name="krpi", gender=Gender.FEMALE)

        satvy.set_spouse(spouse=asva)
        krpi.set_spouse(spouse=vyas)

        vasa = Person(name="vasa", gender=Gender.MALE)
        satvy.add_child(child=vasa)

        kriya = Person(name="kriya", gender=Gender.MALE)
        krithi = Person(name="krithi", gender=Gender.FEMALE)
        krpi.add_children(children=[kriya, krithi])

        self.members = [
            shan, anga,
            chit, amba, ish, vich, lika, aras, chitra, satya, vyan,
            dritha, tritha, vritha, jaya, vila, chika, arit, jnki, ahit, satvy, asva, krpi, vyas, atya,
            yodhan, laki, lavnya, vasa, kriya, krithi
        ]

    @property
    def total_members(self) -> int:
        return len(self.members)

    def member_exists(self, person_name: str) -> Optional[Person]:
        matched_member = None
        for member in self.members:
            if member.name == person_name.capitalize():
                matched_member = member
                break

        return matched_member

    def add_member(self, mother_name: str, new_member_name: str, new_member_gender: Enum) -> Enum:
        mother = self.member_exists(person_name=mother_name)
        if not mother:
            return Responses.PERSON_NOT_FOUND

        child = Person(name=new_member_name, gender=new_member_gender)
        status = mother.add_child(child=child)
        if status == Responses.CHILD_ADDITION_SUCCEEDED:
            self.members.append(child)

        return status

    def get_relationship(self, member_name: str, relation: Enum) -> Optional[Union[Enum, List]]:
        member = self.member_exists(person_name=member_name)
        if not member:
            return Responses.PERSON_NOT_FOUND

        relation_of = RELATION_CLASS_PICKER.get(relation)
        relatives = relation_of(member).relatives()
        return relatives if relatives else None
