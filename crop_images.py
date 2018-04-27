import os
from PIL import Image


def crop(path, ip, height, width):
    li=[]
    im = Image.open(ip)
    imgwidth, imgheight = im.size
    k = 0
    for i in range(0, imgheight, height):
        for j in range(0, imgwidth, width):
            box = (j, i, j + width, i + height)
            a = im.crop(box)
            file_name = os.path.join(path, "IMG-%s.png" % k)
            a.save(file_name)
            li.append(file_name)
            k += 1
    # print('cropping images done..')
    return li


if '__name__' == '__main__':
    crop('/home/prime/Desktop', '/home/prime/Desktop/train_4249_0000.png', 128, 128)
