import unittest
from typing import List

from constants import Relations, Responses
from family import Family
from person import Gender, Person


class TestFamily(unittest.TestCase):

    def setUp(self) -> None:
        self.family = Family()

    def get_names_list(self, result: List[Person]) -> List[str]:
        return [person.name for person in result]


class TestAddMember(TestFamily):
    def setUp(self) -> None:
        super(TestAddMember, self).setUp()

    def test_add_member_when_passed_mother_member_not_found(self):
        expected = Responses.PERSON_NOT_FOUND
        result = self.family.add_member(mother_name="unknown-member",
                                        new_member_name="john",
                                        new_member_gender=Gender.MALE)
        self.assertEqual(expected, result)

    def test_add_member_when_passed_mother_member_does_not_have_a_spouse(self):
        expected = Responses.CHILD_ADDITION_FAILED
        result = self.family.add_member(mother_name="atya", new_member_name="john", new_member_gender=Gender.MALE)
        self.assertEqual(expected, result)

    def test_add_member_when_passed_mother_member_is_not_a_female(self):
        expected = Responses.CHILD_ADDITION_FAILED
        result = self.family.add_member(mother_name="vyan", new_member_name="john", new_member_gender=Gender.MALE)
        self.assertEqual(expected, result)

    def test_add_member_success(self):
        total_children_of_lika = 2
        total_member = self.family.total_members
        lika = self.family.member_exists(person_name="lika")
        self.assertEqual(len(lika.children), total_children_of_lika)

        expected = Responses.CHILD_ADDITION_SUCCEEDED
        result = self.family.add_member(mother_name="lika", new_member_name="john", new_member_gender=Gender.MALE)
        self.assertEqual(expected, result)

        self.assertEqual(len(lika.children), total_children_of_lika + 1)
        self.assertEqual(self.family.total_members, total_member + 1)


class TestGetRelation(TestFamily):
    def setUp(self) -> None:
        super(TestGetRelation, self).setUp()

    def test_get_relation_when_person_not_found(self):
        expected = Responses.PERSON_NOT_FOUND
        result = self.family.get_relationship(member_name="unknown-member", relation=Relations.Mother)
        self.assertEqual(expected, result)

    def test_get_relation_when_father_not_exists(self):
        result = self.family.get_relationship(member_name="shan", relation=Relations.Father)
        self.assertIsNone(result)

    def test_get_relation_when_mother_not_exists(self):
        result = self.family.get_relationship(member_name="shan", relation=Relations.Mother)
        self.assertIsNone(result)


class TestSiblings(TestFamily):
    def setUp(self) -> None:
        super(TestSiblings, self).setUp()

        self.relation = Relations.Siblings

    def test_get_siblings_when_siblings_does_not_exists(self):
        result = self.family.get_relationship(member_name="vasa", relation=self.relation)
        self.assertIsNone(result)

    def test_get_siblings_after_adding_sibling_when_siblings_does_not_existed_initially(self):
        vasa = self.family.member_exists(person_name="vasa")
        self.family.add_member(mother_name=vasa.mother.name, new_member_name="john", new_member_gender=Gender.MALE)

        expected_names = ["John"]

        result = self.family.get_relationship(member_name=vasa.name, relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_siblings_when_siblings_exists(self):
        expected_names = ["Chit", "Vich", "Aras", "Satya"]

        result = self.family.get_relationship(member_name="ish", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_siblings_after_adding_new_siblings(self):
        ish = self.family.member_exists(person_name="ish")
        self.family.add_member(mother_name=ish.mother.name, new_member_name="john", new_member_gender=Gender.MALE)

        expected_names = ["Chit", "Vich", "Aras", "Satya", "John"]

        result = self.family.get_relationship(member_name=ish.name, relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)


class TestSon(TestFamily):
    def setUp(self) -> None:
        super(TestSon, self).setUp()

        self.relation = Relations.Son

    def test_get_son_when_son_does_not_exists(self):
        result = self.family.get_relationship(member_name="lika", relation=self.relation)
        self.assertIsNone(result)

    def test_get_son_after_adding_son_when_son_does_not_existed_initially(self):
        lika = self.family.member_exists(person_name="lika")
        self.family.add_member(mother_name=lika.name, new_member_name="john", new_member_gender=Gender.MALE)

        expected_names = ["John"]

        result = self.family.get_relationship(member_name=lika.name, relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_son_when_son_exists(self):
        expected_names = ["Asva", "Vyas"]

        result = self.family.get_relationship(member_name="satya", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_son_after_adding_new_son(self):
        anga = self.family.member_exists(person_name="anga")
        self.family.add_member(mother_name=anga.name, new_member_name="john", new_member_gender=Gender.MALE)

        expected_names = ["Chit", "Ish", "Vich", "Aras", "John"]

        result = self.family.get_relationship(member_name=anga.name, relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_son_when_using_father_name(self):
        expected_names = ["Asva", "Vyas"]

        result = self.family.get_relationship(member_name="vyan", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)


class TestDaughter(TestFamily):
    def setUp(self) -> None:
        super(TestDaughter, self).setUp()

        self.relation = Relations.Daughter

    def test_get_daughter_when_daughter_does_not_exists(self):
        result = self.family.get_relationship(member_name="dritha", relation=self.relation)
        self.assertIsNone(result)

    def test_get_daughter_after_adding_daughter_when_daughter_does_not_existed_initially(self):
        dritha = self.family.member_exists(person_name="dritha")
        self.family.add_member(mother_name=dritha.name, new_member_name="jane", new_member_gender=Gender.FEMALE)

        expected_names = ["Jane"]

        result = self.family.get_relationship(member_name=dritha.name, relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_daughter_when_daughter_exists(self):
        expected_names = ["Atya"]

        result = self.family.get_relationship(member_name="satya", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_daughter_after_adding_new_daughter(self):
        satya = self.family.member_exists(person_name="satya")
        self.family.add_member(mother_name=satya.name, new_member_name="jane", new_member_gender=Gender.FEMALE)

        expected_names = ["Atya", "Jane"]

        result = self.family.get_relationship(member_name=satya.name, relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_daughter_when_using_father_name(self):
        expected_names = ["Atya"]

        result = self.family.get_relationship(member_name="vyan", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)


class TestPaternalUncle(TestFamily):
    def setUp(self) -> None:
        super(TestPaternalUncle, self).setUp()

        self.relation = Relations.PaternalUncle

    def test_get_paternal_uncle_when_father_does_not_exists(self):
        result = self.family.get_relationship(member_name="amba", relation=self.relation)
        self.assertIsNone(result)

    def test_get_paternal_uncle_when_paternal_uncle_does_not_exists(self):
        result = self.family.get_relationship(member_name="chit", relation=self.relation)
        self.assertIsNone(result)

    def test_get_paternal_uncle_when_paternal_uncle_exists(self):
        expected_names = ["Vyas"]

        result = self.family.get_relationship(member_name="vasa", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_paternal_uncle_after_adding_new_paternal_uncle(self):
        satya = self.family.member_exists(person_name="satya")
        self.family.add_member(mother_name=satya.name, new_member_name="john", new_member_gender=Gender.MALE)

        expected_names = ["Vyas", "John"]

        result = self.family.get_relationship(member_name="vasa", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)


class TestMaternalUncle(TestFamily):
    def setUp(self) -> None:
        super(TestMaternalUncle, self).setUp()

        self.relation = Relations.MaternalUncle

    def test_get_maternal_uncle_when_mother_does_not_exists(self):
        result = self.family.get_relationship(member_name="jaya", relation=self.relation)
        self.assertIsNone(result)

    def test_get_maternal_uncle_when_maternal_uncle_does_not_exists(self):
        result = self.family.get_relationship(member_name="kriya", relation=self.relation)
        self.assertIsNone(result)

    def test_get_maternal_uncle_when_maternal_uncle_exists(self):
        expected_names = ["Ahit"]

        result = self.family.get_relationship(member_name="laki", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_maternal_uncle_after_adding_new_maternal_uncle(self):
        chitra = self.family.member_exists(person_name="chitra")
        self.family.add_member(mother_name=chitra.name, new_member_name="john", new_member_gender=Gender.MALE)

        expected_names = ["Ahit", "John"]

        result = self.family.get_relationship(member_name="laki", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)


class TestPaternalAunt(TestFamily):
    def setUp(self) -> None:
        super(TestPaternalAunt, self).setUp()

        self.relation = Relations.PaternalAunt

    def test_get_paternal_aunt_when_father_does_not_exists(self):
        result = self.family.get_relationship(member_name="jaya", relation=self.relation)
        self.assertIsNone(result)

    def test_get_paternal_aunt_when_paternal_aunt_does_not_exists(self):
        result = self.family.get_relationship(member_name="laki", relation=self.relation)
        self.assertIsNone(result)

    def test_get_paternal_aunt_when_paternal_aunt_exists(self):
        expected_names = ["Atya"]

        result = self.family.get_relationship(member_name="kriya", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_paternal_aunt_after_adding_new_paternal_aunt(self):
        satya = self.family.member_exists(person_name="satya")
        self.family.add_member(mother_name=satya.name, new_member_name="jane", new_member_gender=Gender.FEMALE)

        expected_names = ["Atya", "Jane"]

        result = self.family.get_relationship(member_name="kriya", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)


class TestMaternalAunt(TestFamily):
    def setUp(self) -> None:
        super(TestMaternalAunt, self).setUp()

        self.relation = Relations.MaternalAunt

    def test_get_maternal_aunt_when_mother_does_not_exists(self):
        result = self.family.get_relationship(member_name="jaya", relation=self.relation)
        self.assertIsNone(result)

    def test_get_maternal_aunt_when_maternal_aunt_does_not_exists(self):
        result = self.family.get_relationship(member_name="laki", relation=self.relation)
        self.assertIsNone(result)

    def test_get_maternal_aunt_when_maternal_aunt_exists(self):
        expected_names = ["Tritha"]

        result = self.family.get_relationship(member_name="yodhan", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_maternal_aunt_after_adding_new_maternal_aunt(self):
        chitra = self.family.member_exists(person_name="amba")
        self.family.add_member(mother_name=chitra.name, new_member_name="Jane", new_member_gender=Gender.FEMALE)

        expected_names = ["Tritha", "Jane"]

        result = self.family.get_relationship(member_name="yodhan", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)


class TestBrotherInLaw(TestFamily):

    def setUp(self) -> None:
        super(TestBrotherInLaw, self).setUp()

        self.relation = Relations.BrotherInLaw

    def test_get_brother_in_law_when_spouse_does_not_exist(self):
        result = self.family.get_relationship(member_name="yodhan", relation=self.relation)
        self.assertIsNone(result)

    def test_get_brother_in_law_when_spouse_does_not_have_brothers(self):
        result = self.family.get_relationship(member_name="asva", relation=self.relation)
        self.assertIsNone(result)

    def test_get_brother_in_law_when_spouse_have_brothers(self):
        expected_names = ["Ahit"]

        result = self.family.get_relationship(member_name="arit", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_brother_in_law_after_adding_brother_for_spouse(self):
        chitra = self.family.member_exists(person_name="chitra")
        self.family.add_member(mother_name=chitra.name, new_member_name="john", new_member_gender=Gender.MALE)

        expected_names = ["Ahit", "John"]

        result = self.family.get_relationship(member_name="arit", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_brother_in_law_when_sisters_does_not_exist(self):
        result = self.family.get_relationship(member_name="jnki", relation=self.relation)
        self.assertIsNone(result)

    def test_get_brother_in_law_when_sisters_does_not_have_spouse(self):
        result = self.family.get_relationship(member_name="asva", relation=self.relation)
        self.assertIsNone(result)

    def test_get_brother_in_law_when_sisters_have_spouse(self):
        expected_names = ["Jaya"]

        result = self.family.get_relationship(member_name="tritha", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)


class TestSisterInLaw(TestFamily):

    def setUp(self) -> None:
        super(TestSisterInLaw, self).setUp()

        self.relation = Relations.SisterInLaw

    def test_get_sister_in_law_when_spouse_does_not_exists(self):
        result = self.family.get_relationship(member_name="yodhan", relation=self.relation)
        self.assertIsNone(result)

    def test_get_sister_in_law_when_spouse_does_not_have_sisters(self):
        result = self.family.get_relationship(member_name="dritha", relation=self.relation)
        self.assertIsNone(result)

    def test_get_sister_in_law_when_spouse_have_sisters(self):
        expected_names = ["Atya"]

        result = self.family.get_relationship(member_name="satvy", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_sister_in_law_after_adding_sister_for_spouse(self):
        satya = self.family.member_exists(person_name="satya")
        self.family.add_member(mother_name=satya.name, new_member_name="jane", new_member_gender=Gender.FEMALE)

        expected_names = ["Atya", "Jane"]

        result = self.family.get_relationship(member_name="satvy", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)

    def test_get_sister_in_law_when_brothers_does_not_exists(self):
        result = self.family.get_relationship(member_name="vila", relation=self.relation)
        self.assertIsNone(result)

    def test_get_sister_in_law_when_brothers_does_not_have_spouse(self):
        result = self.family.get_relationship(member_name="krithi", relation=self.relation)
        self.assertIsNone(result)

    def test_get_sister_in_law_when_brothers_have_spouse(self):
        expected_names = ["Amba", "Lika", "Chitra"]

        result = self.family.get_relationship(member_name="satya", relation=self.relation)
        self.assertEqual(len(expected_names), len(result))

        result_names = self.get_names_list(result=result)
        self.assertEqual(expected_names, result_names)
