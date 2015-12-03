from PIL import Image
import pickle
import imghdr
import os

FINGERPRINTS = '/root/pictur/pictur/static/resources/fingerprints/'
TEMP = '/root/pictur/pictur/static/resources/temp/'

def check_duplicates(image, ex):
    """compares given image to all fingerprints in folder
    and adds image fingerprint to list if not a duplicate

    returns histogram if image is different from all others
    returns none if image is a duplicate
    """

    image.save(TEMP+'temp.'+ex)
    image = Image.open(TEMP+'temp.'+ex)
    hist = create_hist(image)
    for histogram in os.listdir(FINGERPRINTS):
        hist2 = pickle.load(open(FINGERPRINTS+histogram, 'rb'))
        if(pic_compare(hist, hist2)):
            return histogram, hist
    return None, hist

    

def save_fingerprint(hist, fileName):
    """Saves the fingerprint to a pickle file in the fingerprint directory"""
    pickle.dump(hist, open(FINGERPRINTS+fileName+'.p', 'wb'))
 

def create_hist(im):
    """creates and returns a histogram fingerprint of the given number"""
    
    hist3 = im.histogram()
    im = im.convert('LA')
    hist = im.histogram()
    hist2 = list()
    size = im.width*im.height
    for i in hist:
        hist2.append(i/size)
    for i in hist3:
        hist2.append(i/size)
    return hist2

def pic_compare(hist, hist2):
    """compares 2 fingerprint
    returns 0 if different
    returns 1 if the same
    """
    count = 0
    for i, j in zip(hist, hist2):
        if(abs(i-j) > 0.0033):
            if count == 15:
                return 0
            else:
                count += 1
    return 1
