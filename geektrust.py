import sys
from enum import Enum

from constants import Operations, Relations
from family import Family
from person import Gender


def show(output):
    if not output:
        print(None)

    elif isinstance(output, Enum):
        print(output.value)

    elif isinstance(output, list):
        for person in output:
            print(person.name, end=' ')
        print()


def main():
    input_file = sys.argv[1]

    with open(input_file) as file:
        lines = file.readlines()

    family = Family()
    for line in lines:
        line = line.rstrip()
        words = line.split()

        output = None
        if words[0] == Operations.ADD_CHILD.value:
            output = family.add_member(mother_name=words[1],
                                       new_member_name=words[2],
                                       new_member_gender=Gender(words[3]))

        elif words[0] == Operations.GET_RELATIONSHIP.value:
            output = family.get_relationship(member_name=words[1],
                                             relation=Relations(words[2]))

        show(output)


if __name__ == "__main__":
    main()
