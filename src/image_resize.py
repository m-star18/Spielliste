import io

from PIL import Image, ImageTk


def get_img_data(site, maxsize=(500, 500), first=False):
    """
    Generate image data using PIL
    """
    image = Image.open(site)
    image.thumbnail(maxsize)
    if first:  # tkinter is inactive the first time
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        del image
        return bio.getvalue()
    return ImageTk.PhotoImage(image)
