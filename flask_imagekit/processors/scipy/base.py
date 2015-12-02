class Anchor(object):
    """
    Defines all the anchor points needed by the various processor classes.

    """
    TOP_LEFT = 'tl'
    TOP = 't'
    TOP_RIGHT = 'tr'
    BOTTOM_LEFT = 'bl'
    BOTTOM = 'b'
    BOTTOM_RIGHT = 'br'
    CENTER = 'c'
    LEFT = 'l'
    RIGHT = 'r'

    _ANCHOR_PTS = {
        TOP_LEFT: (0, 0),
        TOP: (0.5, 0),
        TOP_RIGHT: (1, 0),
        LEFT: (0, 0.5),
        CENTER: (0.5, 0.5),
        RIGHT: (1, 0.5),
        BOTTOM_LEFT: (0, 1),
        BOTTOM: (0.5, 1),
        BOTTOM_RIGHT: (1, 1),
    }

    @staticmethod
    def get_tuple(anchor):
        """Normalizes anchor values (strings or tuples) to tuples.

        """
        # If the user passed in one of the string values, convert it to a
        # percentage tuple.
        if anchor in Anchor._ANCHOR_PTS.keys():
            anchor = Anchor._ANCHOR_PTS[anchor]
        return anchor
