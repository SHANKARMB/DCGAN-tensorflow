import os
from PIL import Image


def crop(path='', ip='', height=128, width=128, name='IMG', paths=True):
    li = []
    im = Image.open(ip)
    imgwidth, imgheight = im.size
    k = 0
    image_list = []
    for i in range(0, imgheight, height):
        for j in range(0, imgwidth, width):
            box = (j, i, j + width, i + height)
            a = im.crop(box)
            filename = name + "_%s.png" % k
            image_list.append(filename)
            file_path = os.path.join(path, filename)
            a.save(file_path)
            li.append(file_path)
            k += 1
    # print('cropping images done..')
    if paths:
        return li
    else:
        return k, image_list


if '__name__' == '__main__':
    crop('/home/prime/Desktop', '/home/prime/Desktop/train_4249_0000.png', 128, 128)
