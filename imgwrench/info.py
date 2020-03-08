# -*- coding: utf-8 -*-

'''Image meta information.'''


class ImageInfo:
    '''Container for image meta information'''

    def __init__(self, path, index, exif, xmp):
        self.path = path
        self.fname = self.path.name
        self.index = int(index)
        self.exif = exif
        self.xmp = xmp

    def __str__(self):
        return str(self.path)
