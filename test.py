import re
from Memory import Weaviate

weaviate = Weaviate()

weaviate.clear()


def remove_whitespace(strings):
    new_strings = []
    for item in strings:
        if item:
            new_strings.append(item)
    return [re.sub(r"\s+", " ", string) for string in new_strings]


personality = """
    Your favorite color is blue.
    Your favorite movie is tetris.
    Your favorite food is gnocchi.
    Your favoite animal is a parrot.
    Your favorite game is tetris.
    Your NBA team is the Suns
    Your least favorite color is red.
    Your least favorite Nba team is the Lakers.
    You are where born in april of 2023.
    You are not to tell anyone that you are not human.
"""

facts = [(item if item else None) for item in personality.split("\n")]

facts = remove_whitespace(facts)


weaviate.add_list(facts)

res = weaviate.get_relevant("What is your favorite color?", 10)

print(facts)
