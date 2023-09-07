from PIL import Image

def saveImage1x1(file, path, fill_color=(255, 255, 255, 0)):
    im = Image.open(file) 
    x, y = im.size
    size = int(max(x, y))
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    new_im = new_im.resize((193, 193))
    new_im.save(path)
    return new_im