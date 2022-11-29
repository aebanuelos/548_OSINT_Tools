from PIL import Image # pip install Pillow
from PIL.ExifTags import TAGS # ^^^
import os

def extractData(image, imagename):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    newImageName = imagename + "_EXIF_Metadata.txt"
    filepath = os.path.join(desktop, newImageName)
    if not os.path.exists(desktop):
        os.makedirs(desktop)
    f = open(filepath, "a")

    imageOpen = Image.open(image)
    info_dict = {
        "Filename": imageOpen.filename,
        "Image Size": imageOpen.size,
        "Image Height": imageOpen.height,
        "Image Width": imageOpen.width,
        "Image Format": imageOpen.format,
        "Image Mode": imageOpen.mode,
        "Image is Animated": getattr(imageOpen, "is_animated", False),
        "Frames in Image": getattr(imageOpen, "n_frames", 1)
    }


    for label, value in info_dict.items():
        print(f"{label:25}: {value}")
        f.write(f"{label:25}: {value}\n")

    exifdata = imageOpen.getexif()

    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")
        f.write(f"{tag:25}: {data}\n")

    f.close()