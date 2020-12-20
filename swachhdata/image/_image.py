import numpy as np

from bs4 import BeautifulSoup
import requests
import urllib

import cv2

from tqdm.auto import tqdm


class ImageNet:
    """Fetch Images and Labels from ImageNet:
    
    Parameters
    ----------
    img_shape: tuple (rows, cols, colors)
    total_img = int, default=None
    img_per_cat = int, default=None
    verbose: int (0, 1, -1), default=0

    Attributes
    ----------
    images_ : numpy.array of images
    labels_ : list of labels
    
    Examples
    --------
    >>> from swachhdata.image import ImageNet
    >>> indt = {'Automobile': 'n02814533'}
    >>> imgnet = ImageNet(img_shape=(32, 32, 3), total_img=100, verbose=1)
    >>> images, labels = imgnet.fetch(indt)
    """

    def __init__(self, img_shape, total_img=None, img_per_cat=None, verbose=0):
        self.__nos = total_img
        self.__nos_cat = img_per_cat
        self.__shape = img_shape
        self.__verbose = verbose
        self.__verbose_status = True
        if self.__verbose == -1:
            self.__verbose_status = False
        self.__urls = None
        self.images_ = None
        self.labels_ = []
    
    def __url_to_image(self, url):
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype='uint8')
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    
    def __get_imagelist(self, wnid):
        img_list = requests.get(f'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={wnid}')
        img_soup = BeautifulSoup(img_list.content, 'html.parser')
        img_str = str(img_soup)
        self.__urls = img_str.split('\r\n')

    def __count_nos_images(self, INdict):
        if self.__nos == None:
            try:
                self.__nos == self.__nos_cat * len(INdict)
            except:
                print(f'total_img and img_per_cat missing from arguments!, Please enter any one')
        else:
            self.__nos_cat = self.__nos // len(INdict)
        
        self.images_ = np.zeros((self.__nos, self.__shape[0], self.__shape[1], self.__shape[2]))
    
    def fetch(self, INdict):
        """Fetches Images from ImageNet
        Parameters
        ----------
        INdict : python dictionary

        Returns
        -------
        images : numpy.array of images
        labels : list of labels
        """
        id = 0
        self.__count_nos_images(INdict)
        for synset, wnid in INdict.items():
            self.__get_imagelist(wnid)
            snum = i = 0
            if self.__verbose in [-1, 1]:
                progress = tqdm(total=self.__nos_cat, position=0, leave=self.__verbose_status)
                progress.set_postfix({f'{synset}': wnid})
            while snum < self.__nos_cat:
                try:
                    img = self.__url_to_image(self.__urls[i])
                    img = cv2.resize(img, (self.__shape[0], self.__shape[1]))
                    self.images_[id] = img
                    self.labels_.append(synset)
                    id, snum = id + 1, snum + 1
                    if self.__verbose in [-1, 1]:
                        progress.update(1)
                except:
                    None
                i += 1
        return self.images_, self.labels_