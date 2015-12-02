from .base import Anchor


class Resize(object):
    """
    Resizes an image to the specified width and height.

    """
    def __init__(self, width, height, upscale=True):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.
        :param upscale: Should the image be enlarged if smaller than the dimensions?

        """
        self.width = width
        self.height = height
        self.upscale = upscale

    def process(self, img):
        from scipy.misc import imresize
        if self.upscale or (self.width < img.size[0] and self.height < img.size[1]):
            img = imresize(img, (self.width, self.height))
        return img


class ResizeCanvas(object):
    """
    Resizes the canvas, using the provided background color if the new size is
    larger than the current image.

    """
    def __init__(self, width, height, color=None, anchor=None, x=None, y=None):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.
        :param color: The background color to use for padding.
        :param anchor: Specifies the position of the original image on the new
            canvas. Valid values are:

            - Anchor.TOP_LEFT
            - Anchor.TOP
            - Anchor.TOP_RIGHT
            - Anchor.LEFT
            - Anchor.CENTER
            - Anchor.RIGHT
            - Anchor.BOTTOM_LEFT
            - Anchor.BOTTOM
            - Anchor.BOTTOM_RIGHT

            You may also pass a tuple that indicates the position in
            percentages. For example, ``(0, 0)`` corresponds to "top left",
            ``(0.5, 0.5)`` to "center" and ``(1, 1)`` to "bottom right". This is
            basically the same as using percentages in CSS background positions.

        """
        if x is not None or y is not None:
            if anchor:
                raise Exception('You may provide either an anchor or x and y'
                        ' coordinate, but not both.')
            else:
                self.x, self.y = x or 0, y or 0
                self.anchor = None
        else:
            self.anchor = anchor or Anchor.CENTER
            self.x = self.y = None

        self.width = width
        self.height = height

    def process(self, img):
        original_height, original_width, _ = img.shape

        if self.anchor:
            anchor = Anchor.get_tuple(self.anchor)
            trim_x, trim_y = self.width - original_width, \
                    self.height - original_height
            x = int(float(trim_x) * float(anchor[0]))
            y = int(float(trim_y) * float(anchor[1]))
        else:
            x, y = self.x, self.y

        x, y = -x, -y

        new_img = img[x:x+self.height, y:y+self.width]

        return new_img


class ResizeToCover(object):
    """
    Resizes the image to the smallest possible size that will entirely cover the
    provided dimensions. You probably won't be using this processor directly,
    but it's used internally by ``ResizeToFill`` and ``SmartResize``.

    """
    def __init__(self, width, height, upscale=True):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.

        """
        self.width, self.height = width, height
        self.upscale = upscale

    def process(self, img):
        original_height, original_width = img.size
        ratio = max(float(self.width) / original_width,
                float(self.height) / original_height)
        new_width, new_height = (int(round(original_width * ratio)),
                int(round(original_height * ratio)))
        img = Resize(new_width, new_height, upscale=self.upscale).process(img)
        return img


class ResizeToFill(object):
    """
    Resizes an image, cropping it to the exact specified width and height.

    """

    def __init__(self, width=None, height=None, anchor=None, upscale=True):
        """
        :param width: The target width, in pixels.
        :param height: The target height, in pixels.
        :param anchor: Specifies which part of the image should be retained
            when cropping.
        :param upscale: Should the image be enlarged if smaller than the dimensions?

        """
        self.width = width
        self.height = height
        self.anchor = anchor
        self.upscale = upscale

    def process(self, img):
        from .crop import Crop
        img = ResizeToCover(self.width, self.height,
                            upscale=self.upscale).process(img)
        return Crop(self.width, self.height,
                    anchor=self.anchor).process(img)
