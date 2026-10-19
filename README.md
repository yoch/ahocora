# ahocora

A pure-Python implementation of the **Aho-Corasick** algorithm for
multi-pattern string matching: add a set of words to an automaton, build it
once, then find every occurrence of every word in a text in a single pass.

- One file (`ahocora.py`), standard library only, no C extension to compile.
- Reports all matches, including overlapping ones, as `(word, start_index)` pairs.
- Works on strings, or on any sequence of hashable symbols (for example lists of tokens).
- Two modes: failure links (default, less memory) or a fully deterministic
  automaton (no failure links at search time, but it can use much more memory).

## Install

There is no package. Copy [`ahocora.py`](ahocora.py) into your project
(Python 3, no dependencies).

## Usage

```python
>>> from ahocora import AC
>>> ac = AC()
>>> for word in ['he', 'she', 'his', 'hers']:
...     ac.add(word)
>>> ac.build()
>>> sorted(ac.search('ushers'))
[('he', 2), ('hers', 2), ('she', 1)]

```

`search()` is a generator. It yields each match when its last character is
read, so matches come in order of their end position. Matches that end at
the same position come in no particular order.

Words and texts can be sequences of tokens instead of characters. Words
must be hashable, so use tuples:

```python
>>> ac = AC()
>>> ac.add(('new', 'york'))
>>> ac.add(('york',))
>>> ac.build()
>>> sorted(ac.search('i love new york city'.split()))
[(('new', 'york'), 2), (('york',), 3)]

```

### API

- `AC()` creates an empty automaton.
- `add(word)` adds a non-empty word. All words must be added before `build()`.
- `build(deterministic=False)` finishes the automaton. Call it once, before
  searching. With `deterministic=True`, it adds the missing transitions so
  that searching never follows failure links. Searching can then be faster,
  but memory use can grow a lot. The default is the safe choice.
- `search(text)` yields `(word, index)` pairs, where `index` is the
  position of the word's first character in `text`.

Wrong usage (adding a word after `build()`, adding an empty word, searching
before `build()`) is rejected with `assert`, so it is not checked under
`python -O`.

## Complexity

In the default mode, building takes time linear in the total length of the
words, plus the merging of output sets. Searching reads each symbol of the
text once (failure links add amortized constant work per symbol), so a search
runs in time linear in the length of the text plus the number of matches.

## Related

[pyahocorasick](https://github.com/WojciechMula/pyahocorasick) is an
Aho-Corasick library for Python built mainly as a C extension. `ahocora` is
a small pure-Python alternative for when you would rather not depend on a
compiled extension, or want code that is short enough to read.

The implementation was originally inspired by
[this article](https://medium.com/100-days-of-algorithms/day-34-aho-corasick-4b9f439d4712)
from the *100 days of algorithms* series.

## Tests

The examples in this README are doctests:

```bash
python -m doctest -v README.md
```

## License

[GPL-3.0](LICENSE).
