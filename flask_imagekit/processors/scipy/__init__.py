def process_image(img, processors=None, format=None, autoconvert=True, options=None):
    from scipy.misc import fromimage, imsave
    from StringIO import StringIO

    num_img = fromimage(img)

    format = format or img.format or 'JPEG'

    for proc in processors:
        num_img = proc.process(num_img)

    new_file = StringIO()
    imsave(new_file, num_img, format)
    new_file.seek(0)

    return new_file
