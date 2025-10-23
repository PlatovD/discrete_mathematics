import enum


@enum.unique
class Direction(enum.IntEnum):
    LEFT = -1
    RIGHT = 1
    STAY = 0

    @classmethod
    def get_by_char(cls, char: str):
        match char.lower():
            case 'l':
                return cls.LEFT
            case 'r':
                return cls.RIGHT
            case 's':
                return cls.STAY
