"""
"""

import logging
from collections import deque

from .instance import Instance


logger = logging.getLogger(__name__)


class WatchList(object):

    def __init__(self, instance: Instance) -> None:
        super().__init__()
        self._instance = instance

        self._list = [deque() for _ in range(2 * len(instance.variables))]

        # Make each clause watch its first literal
        for clause in instance.clauses:
            self._list[clause[0]].append(clause)

    def __str__(self) -> str:
        parts = []
        for literal, watchers in enumerate(self._list):
            literal_string = self._instance.literal_to_string(literal)
            clauses_string = ", ".join(
                self._instance.clause_to_string(c) for c in watchers
            )
            parts.append("{}: {}".format(literal_string, clauses_string))
        return "\n".join(parts)

    @property
    def variable_count(self):
        return len(self._instance.variables)

    def update(self, false_literal, assignment):
        while self._list[false_literal]:
            clause = self._list[false_literal][0]

            for alternative in clause:
                v = alternative >> 1
                a = alternative & 1
                if assignment[v] is None or assignment[v] == a ^ 1:
                    del self._list[false_literal][0]
                    self._list[alternative].append(clause)
                    break
            else:
                logger.debug("Conflicting Clause: {}".format(
                    self._instance.clause_to_string(clause)
                ))
                return False
        return True
