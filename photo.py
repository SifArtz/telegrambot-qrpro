from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO

def round_image(image_url):
    output_size = (150, 150)
    radius = 20

    # Load the original image from URL
    response = requests.get(image_url)
    original_image = Image.open(BytesIO(response.content))
    
    # Crop to a square shape
    width, height = original_image.size
    if width > height:
        left = (width - height) // 2
        top = 0
    else:
        left = 0
        top = (height - width) // 2
    right = left + min(width, height)
    bottom = top + min(width, height)
    
    cropped_image = original_image.crop((left, top, right, bottom))
    resized_image = cropped_image.resize(output_size)

    im = resized_image.convert("RGBA")

    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))

    im.putalpha(alpha)

    rounded_image = Image.new('RGBA', im.size, (255, 255, 255, 0))
    rounded_image.paste(im, (0, 0), im)
    rounded_image.save("output_rounded.png")
    return rounded_image



