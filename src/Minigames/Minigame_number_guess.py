import random


class NumberGuesser:
    def __init__(self):
        self.target_number = None
        self.max_tries = 3
        self.players = []

    def description(self) -> str:
        """Gibt eine kurze Beschreibung des Spiels zurück."""
        return (
            "Das Spiel 'Number Guesser':\n"
            "Der erste Spieler wählt eine Zahl zwischen 1 und 10.\n"
            "Der zweite Spieler hat drei Versuche, die Zahl zu erraten.\n"
            "Nach jedem falschen Versuch gibt es einen Hinweis ('höher' oder 'niedriger').\n"
            "Errät der zweite Spieler die Zahl, gewinnt er. Andernfalls verliert er, wenn alle Versuche aufgebraucht sind."
        )

    def set_players(self, *players: str):
        if len(players) != 2:
            raise ValueError("Es müssen genau zwei Spieler teilnehmen.")
        self.players = players

    async def _play(self) -> str:
        if len(self.players) != 2:
            raise ValueError("Es müssen genau zwei Spieler gesetzt werden, bevor das Spiel gestartet wird.")


        try:
            self.target_number = int(input(f"{self.players[0]}, wähle eine Zahl zwischen 1 und 10: "))
            if not (1 <= self.target_number <= 10):
                print("Die Zahl muss zwischen 1 und 10 liegen. Das Spiel wird abgebrochen.")
                return "Spiel abgebrochen."
        except ValueError:
            print("Bitte gib eine gültige Zahl ein.")
            return "Spiel abgebrochen."

        #maximal 3 Versuche
        tries = 0
        while tries < self.max_tries:
            try:
                guess = int(input(f"{self.players[1]}, Rate die Zahl (Versuch {tries + 1} von {self.max_tries}): "))

                if guess < self.target_number:
                    print("Zu niedrig! noch einmal.")
                elif guess > self.target_number:
                    print("Zu hoch! noch einmal.")
                else:
                    return f"{self.players[1]} hat die Zahl erraten! Du hast gewonnen!"
                tries += 1
            except ValueError:
                print("Bitte gib eine gültige Zahl ein.")

        return f"{self.players[1]}, du hast leider verloren. Die richtige Zahl war {self.target_number}."


if __name__ == "__main__":
    game = NumberGuesser()
    print(game.description())

    game.set_players("Spieler 1", "Spieler 2")

    import asyncio

    result = asyncio.run(game._play())
    print(result)
