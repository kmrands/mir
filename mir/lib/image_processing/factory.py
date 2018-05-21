import io

from PIL import Image


# ---------------------------------
# Processing Factory
# ---------------------------------

def process(binary, format='JPEG', quality=95, optimize=True):
    optimize = optimize.lower() == 'true' if isinstance(optimize, str) else optimize
    def transform(funclist):
        transformed = None
        try:
            transformed = Image.open(io.BytesIO(binary))
        except:
            transformed = Image.open(binary)

        for func in funclist:
            transformed = func(transformed)

        output = io.BytesIO()
        transformed.save(
            output,
            format=format,
            quality=int(quality),
            optimize=optimize
        )
        output.seek(0)

        return output
    return transform
