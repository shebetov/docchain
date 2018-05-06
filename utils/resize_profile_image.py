from PIL import Image


def resize_image(file_name, size=500, background_color=(255, 255, 255)):
    image = Image.open(file_name)
    if image.size[0] > image.size[1]:
        ratio = (size / float(image.size[0]))
        new_size = (size, int(image.size[1] * ratio))
    elif image.size[0] < image.size[1]:
        ratio = (size / float(image.size[1]))
        new_size = (int(image.size[0] * ratio), size)
    else:
        new_size = (size, size)
    image = image.resize(new_size, Image.ANTIALIAS)
    new_image = Image.new("RGB", (size, size), background_color)
    new_image.paste(image, ((size-image.size[0])//2, (size-image.size[1])//2))
    new_image.save(file_name, quality=95)