"""
"""

import logging
from .instance import Instance
from .watchlist import WatchList


logger = logging.getLogger(__name__)


class SATSolver(object):

    def __init__(self, instance: Instance):
        super().__init__()
        self._watchlist = WatchList(instance)

    def recursive_solve(self):
        assignment = [None] * self._watchlist.variable_count
        yield from self._solve(assignment, 0)

    def _solve(self, assignment, d):
        if d == self._watchlist.variable_count:
            yield assignment
            return

        for a in [0, 1]:
            logger.debug('Trying {} = {}'.format(
                self._watchlist._instance.variables[d], a
            ))
            assignment[d] = a
            false_literal = (d << 1) | a
            if self._watchlist.update(false_literal, assignment):
                for a in self._solve(assignment, d + 1):
                    yield a

        assignment[d] = None
