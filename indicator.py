class Pacman:
    def __init__(self, width=3, frames="Cc", fillers=" ·", borders="[]"):
        self._width = width
        self._frames = frames
        self._fillers = fillers
        self._borders = borders
        self._pos = 0
        self._lastlen = 0

    def update(self, status=""):
        self._pos = (self._pos + 1) % self._width
        if status:
            self._lastlen = self._width + len(status) + 3
        else:
            self._lastlen = self._width + 2
        print(
            self._borders[0],
            self._fillers[0] * self._pos,
            self._frames[self._pos % len(self._frames)],
            self._fillers[1] * (self._width - self._pos - 1),
            self._borders[1],
            " " if status else "",
            status if status else "",
            "\b" * self._lastlen,
            sep="", end="", flush=True
        )

    def clear(self):
        print(
            " " * self._lastlen,
            "\b" * (self._lastlen + 1),
            end="", flush=True
        )
