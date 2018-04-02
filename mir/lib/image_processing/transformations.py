from PIL import Image, ImageFilter, ImageEnhance

# ---------------------------------
# Transformation Functions
# ---------------------------------

def thumbnail(size):
    size = [int(i) for i in size.split(',')]
    def create(img):
        img.thumbnail(size)
        return img
    return create


def rotate(deg):
    deg = int(deg)
    def create(img):
        return img.rotate(deg)
    return create


def crop(
    w,
    h,
    vert_position='center',
    horiz_position='center',
    cover=True,
    contain=False
):
    valid_positions= [
        'top',
        'bottom',
        'left',
        'right',
        'center'
    ]
    # TODO: Implement crop function
    def create(img):
        return img
    return create


def blur(radius):
    radius = float(radius)
    def create(img):
        return img.filter(
            ImageFilter.GaussianBlur(radius=radius)
        )
    return create


def contrast(value):
    adj_value = float(value)
    def create(img):
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(adj_value)
        return img
    return create


def saturation(value):
    adj_value = float(value)
    def create(img):
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(adj_value)
        return img
    return create


def brightness(value):
    adj_value = float(value)
    def create(img):
        enhancer= ImageEnhance.Brightness(img)
        img = enhancer.enhance(adj_value)
        return img
    return create


def sharpness(value):
    adj_value = float(value)
    def create(img):
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(adj_value)
        return img
    return create

def flip(direction):
    adj_value = float(value)
    def create(img):
        if direction =='horizontal':
            return img.transpose(Image.FLIP_LEFT_RIGHT)
        if direction =='vertical':
            return img.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            return img
    return create


funcs = {
    'thumbnail': thumbnail,
    'rotate': rotate,
    'blur': blur,
    'contrast': contrast,
    'brightness': brightness,
    'saturation': saturation,
    'sharpness': sharpness,
    'flip': flip
}
