from PIL import Image

def cropAndSaveImage6x1(file, path, fill_color=(0, 0, 0, 0)):
    im = Image.open(file)
    im = im.convert('RGB')   
    x, y = im.size
    size = int(min(x / 6, y))
    st_x, st_y = (x / 2 - size * 3, y / 2 - size / 2)
    end_x, end_y = (st_x + size * 6, st_y + size)
    new_im = im.crop((st_x, st_y, end_x, end_y))
    new_im.save(path, quality=95)
    return new_im