from PIL import Image
import os
import MePipe.settings as settings

def cropAndSaveImage6x1(file, path, fill_color=(0, 0, 0, 0)):
    im = Image.open(file)
    im = im.convert('RGBA')   
    x, y = im.size
    size = int(min(x / 6, y))
    st_x, st_y = (x / 2 - size * 3, y / 2 - size / 2)
    end_x, end_y = (st_x + size * 6, st_y + size)
    new_im = im.crop((st_x, st_y, end_x, end_y))
    new_im.save(path)
    return new_im

def renameCreator(oldName, newName):
    if oldName == newName:
        return
    os.rename(
        os.path.join(settings.MEDIA_ROOT_CBG, oldName + '.png'), 
        os.path.join(settings.MEDIA_ROOT_CBG, newName + '.png'), 
        )
    os.rename(
        os.path.join(settings.MEDIA_ROOT_CPFP, oldName + '.png'), 
        os.path.join(settings.MEDIA_ROOT_CPFP, newName + '.png'), 
        )