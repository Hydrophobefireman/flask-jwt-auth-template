from PIL import Image, ImageOps
from io import BytesIO
from gc import collect


def optimize(image_bytes: bytes):
    b_io = BytesIO(image_bytes)
    target = BytesIO()

    old_size = len(image_bytes)
    img = Image.open(b_io)
    fmt = img.format
    print(f"detected {fmt=}")
    if fmt != "JPEG":
        img = img.convert("RGB")
    ImageOps.exif_transpose(img, in_place=True)
    img.save(target, optimize=True, quality=70, format="jpeg")
    target.seek(0)
    new_file = target.read()
    new_size = len(new_file)
    print(f"{old_size=} ; {new_size=} {new_size/old_size=}")
    collect()
    return new_file
