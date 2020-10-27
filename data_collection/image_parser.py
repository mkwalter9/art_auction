## Created mkwalter9 10/11/20
import os, sys
import requests as r
import shutil

IMAGES_DIR = 'images'

class ImageError(Exception):
    def __init__(self, imageurl):
        print('Image {} Couldn\'t be retreived'.format())

class ImageFetcher:

    def __init__(self, artist):
        artist = artist.replace(' ','_').lower()
        self.filedir = "{}/{}".format(IMAGES_DIR,artist)
        self.__checkdir__()

    def __checkdir__(self):
        if not os.path.exists(IMAGES_DIR): os.mkdir(IMAGES_DIR)
        if not os.path.exists(self.filedir): os.mkdir(self.filedir)

    def fetch_image(self, image_url):
        if image_url == '': return '' # if no image available
        filename = "{}/{}".format(self.filedir, image_url.split("/")[-1])

        # Open the url image, set stream to True, this will return the stream content.
        res = r.get(image_url, stream = True)

        # Check if the image was retrieved successfully
        if res.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            res.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(res.raw, f)

            print('Image successfully Downloaded: ',filename)
        else:
            raise ImageError(filename)
            print('Image Couldn\'t be retreived')
        return filename
