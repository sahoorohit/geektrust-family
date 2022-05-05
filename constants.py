from enum import Enum


class Responses(Enum):
    CHILD_ADDITION_FAILED = "CHILD_ADDITION_FAILED"
    CHILD_ADDITION_SUCCEEDED = "CHILD_ADDITION_SUCCEEDED"
    PERSON_NOT_FOUND = "PERSON_NOT_FOUND"


class Relations(Enum):
    Mother = "Mother"
    Father = "Father"
    Siblings = "Siblings"
    Brother = "Brother"
    Sister = "Sister"
    Son = "Son"
    Daughter = "Daughter"
    BrotherInLaw = "Brother-In-Law"
    SisterInLaw = "Sister-In-Law"
    MaternalAunt = "Maternal-Aunt"
    PaternalAunt = "Paternal-Aunt"
    MaternalUncle = "Maternal-Uncle"
    PaternalUncle = "Paternal-Uncle"


class Operations(Enum):
    ADD_CHILD = "ADD_CHILD"
    GET_RELATIONSHIP = "GET_RELATIONSHIP"
