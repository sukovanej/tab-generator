from __future__ import annotations

from math import inf
from typing import List, Set
from itertools import product


MAX_FRETS = 14
GUITAR_STRINGS = ["E", "H", "G", "D", "A", "E"]
TONES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "H"]
OTHER_TONES = {
    "Cb": "H",
    "Db": "C#",
    "Eb": "D#",
    "Gb": "F#",
    "As": "G#",
    "Hb": "A#",
}
TONE_TO_NUMBER = {tone: i for i, tone in enumerate(TONES)}


class Tone:
    def __init__(self, tone: str) -> None:
        self.tone = tone

    def __add__(self, other: int) -> Tone:
        return Tone(
            TONES[(TONE_TO_NUMBER[self.tone] + other) % len(TONES)]
        )

    def __repr__(self) -> str:
        return self.tone

    def __eq__(self, other: Tone) -> bool:
        return self.tone == other.tone


class Chord:
    def __init__(self, chord_name: str) -> None:
        self._first_tone = Tone(chord_name)
        self._tones = (self._first_tone, self._first_tone + 4, self._first_tone + 7)

    def __repr__(self) -> str:
        return repr(self._tones)

    def __contains__(self, tone: Tone) -> bool:
        return any(tone == t for t in self._tones)


class Tab:
    def __init__(self, frets: List[int]) -> None:
        self._frets = frets

    def print(self):
        for fret, string in zip(self._frets, GUITAR_STRINGS):
            print(string + " |", end="")
            print(" - " * int(max(0, fret - 1)), end="")
            if fret > 0:
                print(" * ", end="")
            print(" - " * (MAX_FRETS - fret))
            show_numbers = [1, 3, 5, 7, 9, 12, 15]

        for i in range(MAX_FRETS):
            if i in show_numbers:
                print(f" {i} ", end="")
            else:
                print("   ", end="")
        print()


class TabCalculator:
    def __init__(self, chord_name: str) -> None:
        self._chord = Chord(chord_name)

    def generate(self, n: int = 1) -> None:
        possible_frets: List[List[int]] = [[] for _ in range(6)]

        for string, tone in enumerate(map(Tone, GUITAR_STRINGS)):
            for i in range(MAX_FRETS):
                if tone + i in self._chord:
                    possible_frets[string].append(i)

        best_tabs = self._calculate_best_tab(possible_frets, n)
        return [Tab(tab) for tab in best_tabs]

    def _calculate_best_tab(self, possible_frets: List[List[int]], n: int) -> List[List[int]]:
        tabs = [(self._calculate_distance(tab), tab) for tab in product(*possible_frets)]
        tabs.sort(key=lambda x: x[0])
        return [t[1] for t in tabs][:n]

    def _calculate_distance(self, tab: List[int]) -> int:
        distance = 0
        last_fret = tab[0]

        for fret in tab[1:]:
            distance += abs(last_fret - fret)
            last_fret = fret

        return distance


if __name__ == "__main__":
    for tone in TONES:
        print(f"tone {tone}: ")

        tabs = TabCalculator(tone).generate(2)
        for tab in tabs:
            tab.print()
            print()
