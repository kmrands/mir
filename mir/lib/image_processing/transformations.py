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


def crop(size_and_pos):
    def is_number(inputString):
        return all(char.isdigit() for char in inputString)

    def create(img):
        w, h, horiz_position, vert_position = size_and_pos.split(',')
        x1 = None
        x2 = None
        y1 = None
        y2 = None

        total_width, total_height = img.size

        if is_number(horiz_position):
            mv = float(horiz_position)/100

            x1 = int(total_width * mv)
            x2 = int(total_width * mv) + int(w)

        if horiz_position == 'left':
            x1 = 0
            x2 = int(w) if int(w) < total_width else total_width

        if horiz_position == 'right':
            x1 = total_width - int(w) if int(w) <= total_width else 0
            x2 = total_width

        if horiz_position == 'center':
            x1 = int(total_width/2) - int(int(w)/2) if int(w) <= total_width else 0
            x2 = int(total_width/2) + int(int(w)/2) if int(w) <= total_width else total_width

        if is_number(vert_position):
            mv = float(vert_position)/100

            y1 = int(total_height * mv)
            y2 = int(total_height * mv) + int(h)

        if vert_position == 'top':
            y1 = 0
            y2 = int(h) if int(h) < total_height else total_height

        if vert_position == 'bottom':
            y1 = total_height - int(h) if int(h) <= total_height else 0
            y2 = total_height

        if vert_position == 'center':
            y1 = int(total_height/2) - int(int(h)/2) if int(h) <= total_height else 0
            y2 = int(total_height/2) + int(int(h)/2) if int(h) <= total_height else total_height

        if x1 != None and y1 != None and x2 != None and y2 != None:
            return img.crop((x1,y1,x2,y2))

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
    'flip': flip,
    'crop': crop
}
