"""
Calculations to help with the pygame frame

Assumes the following layout:

------------------------------------------
|  --------------    ------------------  |
|  |   box1     |    |    box2        |  |
|  |            |    |                |  |
|  --------------    ------------------  |
|  ------------------------------------  |
|  |                                  |  |
|  |         box3                     |  |
|  |                                  |  |
|  |                                  |  |
|  |                                  |  |
|  |                                  |  |
|  ------------------------------------  |
------------------------------------------

"""


class FrameCalculator(object):
    """
    Init takes 5 args:
        frame_x : int
            the width of the pygame window
        frame_y : int
            the height of the pygame window
        padding : int
            the padding (border) between the window edge and other boxes
        box1_x : int
            the width of the top-left box
        box1_y : int
            the height of the top-left box

    Returns boxes as 4-tuples to follow the pygame.Rect class
        return (left, top, width, height)
    """
    def __init__(self, frame_x, frame_y, padding, box1_x, box1_y):
        self.padding = padding
        self._frame_xy = (frame_x, frame_y)
        self._box1_xy = (box1_x, box1_y)

    @property
    def box2_xy(self) -> (int, int):
        box2_x = self._frame_xy[0] - (4 * self.padding) - self._box1_xy[0]
        box2_y = self._box1_xy[1]
        return box2_x, box2_y

    @property
    def box3_xy(self) -> (int, int):
        box3_x = self._frame_xy[0] - (2 * self.padding)
        box3_y = self._frame_xy[1] - (4 * self.padding) - self._box1_xy[1]
        return box3_x, box3_y

    @property
    def frame(self) -> (int, int, int, int):
        left = 0
        top = 0
        width = self._frame_xy[0]
        height = self._frame_xy[1]
        return left, top, width, height

    @property
    def box1(self) -> (int, int, int, int):
        left = self.padding
        top = self.padding
        width = self._box1_xy[0]
        height = self._box1_xy[1]
        return left, top, width, height

    @property
    def box2(self) -> (int, int, int, int):
        left = (3 * self.padding) + self._box1_xy[0]
        top = self.padding
        width = self.box2_xy[0]
        height = self.box2_xy[1]
        return left, top, width, height

    @property
    def box3(self) -> (int, int, int, int):
        left = self.padding
        top = (3 * self.padding) + self._box1_xy[1]
        width = self.box3_xy[0]
        height = self.box3_xy[1]
        return left, top, width, height


if __name__ == '__main__':
    new_frame = FrameCalculator(
        frame_x=800,
        frame_y=480,
        padding=10,
        box1_x=300,
        box1_y=100
    )
    print(new_frame.frame)
    print(new_frame.box1)
    print(new_frame.box2)
    print(new_frame.box3)

    x, y = new_frame.box1[:2]
    print(x, y)
