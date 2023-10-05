import codecs
from datetime import datetime
import json
import subprocess
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

import MePipe.settings as settings

def getMediaInfo(pipe):
    cmnd = [settings.FFPROBE_PATH, '-v', 'quiet', '-print_format', 'json', '-show_format', 'pipe:0']
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate(input=pipe)
    return json.loads(out).get('format', {})

def convertVideo(pipe, outFileName):
    outFileName = outFileName.replace('\\', '/')
    cmnd = [settings.FFMPEG_PATH, 
            '-i', 'pipe:0',
            '-c:v', 'libx264',
            '-c:a', 'copy',
            '-y',
            '' + outFileName + '',
            ]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate(input=pipe)
    return out, err

def saveImage16x9(file, path, fill_color=(0, 0, 0, 0)):
    im = Image.open(file)
    im = im.convert('RGB')   
    x, y = im.size
    size = int(max(x / 16, y / 9))
    new_im = Image.new('RGB', (size * 16, size * 9), fill_color)
    new_im.paste(im, (int((size * 16 - x) / 2), int((size * 9 - y) / 2)))
    new_im = new_im.resize((1280, 720))
    new_im.save(path, quality=95)
    return new_im

def saveVideo16x9(file, inFormat, path):
    if 'mp4' in inFormat:
        default_storage.save(path, ContentFile(file.read()))
    else:
        convertVideo(file.read(), path)

def generateURL():
    link = str(hash(str(datetime.now()) + settings.SECRET_KEY))
    return codecs.encode(link.encode(), 'base64')[:-1].decode("utf-8")

def removeVideoFiles(url):
    os.remove(os.path.join(settings.MEDIA_ROOT_THUMB, url + '.jpg'))
    os.remove(os.path.join(settings.MEDIA_ROOT_VIDEO, url + '.mp4'))