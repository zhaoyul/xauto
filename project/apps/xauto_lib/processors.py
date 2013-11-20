from PIL import Image
from math import floor

def pad(im, requested_size, opts):
    """
    sorl.thumbnail custom processor which pads images to fill required size.
    """
    if "pad" in opts and im.size != requested_size:
        canvas = Image.new("RGBA", requested_size, (255, 255, 255, 1))

        left = floor((requested_size[0] - im.size[0]) / 2)
        top = floor((requested_size[1] - im.size[1]) / 2)

        canvas.paste(im, (left, top))

        im = canvas

    return im
pad.valid_options = ('pad',)
