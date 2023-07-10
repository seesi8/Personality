import random
import re
import time
from math import sqrt

import weaviate

from Hal.Classes import Response
from Hal.Decorators import reg
from Hal.Skill import Skill

from Hal import initialize_assistant
from Memory import Weaviate
from facts import personality

assistant = initialize_assistant()


class Personality(Skill):
    def __init__(self):
        weaviate = Weaviate()

        weaviate.clear()

        def remove_whitespace(strings):
            new_strings = []
            for item in strings:
                if item:
                    new_strings.append(item)
            return [re.sub(r"\s+", " ", string) for string in new_strings]

        facts = [(item if item else None) for item in personality.split("\n")]

        facts = remove_whitespace(facts)

        weaviate.add_list(facts)

    @reg(name="Exponent")
    def ask_about_personality(self, question, num):
        """
        Get information about ballbert's personality. For example things that you like or dislike. Also like how you should act. Also you oppinions and facts about issues.

        :param integer question: What you want to know.
        :param integer num: How many facts you want.
        :return: The Facts.
        :rtype: Response
        """
        res = weaviate.get_relevant(question, num)
        return Response(succeeded=True, data=res)
