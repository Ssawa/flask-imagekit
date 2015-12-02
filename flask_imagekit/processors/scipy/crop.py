class Crop(object):
    """
    Crops an image, cropping it to the specified width and height. You may
    optionally provide either an anchor or x and y coordinates. This processor
    functions exactly the same as ``ResizeCanvas`` except that it will never
    enlarge the image.

    """

    def __init__(self, width=None, height=None, anchor=None, x=None, y=None):
        self.width = width
        self.height = height
        self.anchor = anchor
        self.x = x
        self.y = y

    def process(self, img):
        from .resize import ResizeCanvas

        original_height, original_width, _ = img.shape
        new_width, new_height = min(original_width, self.width), \
                min(original_height, self.height)

        return ResizeCanvas(new_width, new_height, anchor=self.anchor,
                x=self.x, y=self.y).process(img)
