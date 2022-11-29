from PIL import Image, ExifTags  # pip install Pillow
from PIL.ExifTags import TAGS  # ^^^
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

    def get_gps_exif(image):
        data = dict()
        exif = image.getexif()
        if exif:
            # Basic exif (camera make/model, etc)
            for key, val in exif.items():
                data[ExifTags.TAGS[key]] = val

            # Aperture, shutter, flash, lens, tz offset, etc
            ifd = exif.get_ifd(0x8769)
            for key, val in ifd.items():
                data[ExifTags.TAGS[key]] = val

            # GPS Info
            ifd = exif.get_ifd(0x8825)
            for key, val in ifd.items():
                data[ExifTags.GPSTAGS[key]] = val

        filteredKeys = ['GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude']

        gps_dict = {}
        for item in data:
            if item in filteredKeys:
                gps_dict[f"{item}"] = data[f"{item}"]
        result = str(gps_dict)
        return result

    f.write("\nIF ANY GPS DATA IN DMS (degrees, minutes, seconds):\n")
    f.write(get_gps_exif(imageOpen))
    print("\nIF ANY GPS DATA IN DMS (degrees, minutes, seconds):\n")
    print(get_gps_exif(imageOpen))

    f.close()
