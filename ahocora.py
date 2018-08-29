# -*- coding: utf-8 -*-


"""
Author: J. Melka

Aho-Corasick Efficient String Matching Automata

This pure python implementation is originally inspired by:
https://medium.com/100-days-of-algorithms/day-34-aho-corasick-4b9f439d4712

The code is intended to be simple but efficient.
"""


from collections import deque, defaultdict
from itertools import count


class AC:
    """
    Aho-Corasick Efficient String Matching Automata.
    """

    def __init__(self):
        """
        Init the automata.
        """

        self.G = defaultdict(count(1).__next__)  # transitions
        self.O = defaultdict(set)                # outputs
        self.F = {}                              # failure
        self._W = defaultdict(set)               # alphabet
        self._built = False


    def add(self, word):
        """
        Adding a new word to the automata.

        This must be done before building the automata.
        """

        assert not self._built, "adding new words after building is not allowed"

        state = 0
        # add transitions between states
        for c in word:
            self._W[state].add(c)
            state = self.G[state, c]

        assert state != 0, "unable to add empty words"

        # add output
        self.O[state].add(word)


    def build(self):
        """
        Finish the automata building.

        This function must be called once before searching.
        """

        # optimization
        W = self._W
        G = self.G
        F = self.F
        O = self.O
        getG = G.get

        # disable defaultdict behavior
        self.G.default_factory = None

        queue = deque()

        # initial states
        for a in W[0]:
            s = G[0, a]
            queue.append(s)
            F[s] = 0

        while queue:
            r = queue.popleft()

            if r not in W:  # don't overpopulate W
                continue

            # for each letter in alphabet
            for a in W[r]:
                # next state
                s = G[r, a]
                queue.append(s)

                # find fallback state
                state = F[r]
                while state != 0 and (state, a) not in G:
                    state = F[state]

                #assert state==0 or (state, a) in G

                fs = getG((state, a), 0)
                F[s] = fs
                if fs in O:
                    out = O[s]      # retrieve or create output ensemble
                    out |= O[fs]    # union with this output

        # remove unused
        del self._W

        # disable defaultdict behavior
        self.O.default_factory = None

        self._built = True


    def search(self, text):
        """
        Search for words into the text or iterable.

        This generator yields (word, index) pairs.
        """

        assert self._built, "you need to build the automata before searching"

        #optimization
        F = self.F
        G = self.G
        O = self.O
        getG = G.get

        state = 0

        for i, c in enumerate(text, 1):
            # fallback
            while state != 0 and (state, c) not in G:
                state = F[state]

            # transition
            state = getG((state, c), 0)

            # output
            if state in O:
                for w in O[state]:
                    yield w, i - len(w)
