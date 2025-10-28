import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps


"""

    Small Script to render the emojis 

"""

def get_emoji_font_path():
    if sys.platform == "darwin":
        # macOS
        return "/System/Library/Fonts/Apple Color Emoji.ttc"
    elif sys.platform == "win32":
        # Windows
        return "C:\\Windows\\Fonts\\seguiemj.ttf"
    else:
        # Linux (may need to install an emoji font)
        # Common options: "NotoColorEmoji.ttf"
        possible_paths = [
            "/home/quentin/Desktop/videoKR25/Apple Color Emoji.ttc",
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
            "/usr/share/fonts/emoji/NotoColorEmoji.ttf"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        raise OSError("No emoji font found on this system.")


if sys.platform == "darwin":
    # macOS
    FONTSIZE = 160
elif sys.platform == "win32":
    # Windows
    FONTSIZE = 160
else:
    # Linux (may need to install an emoji font)
    # Common options: "NotoColorEmoji.ttf"
    FONTSIZE = 109

def render_emoji_to_png(emoji, filename='emoji.png', color : tuple | None = None,output_size=512, font_size=FONTSIZE, output_dir="media/emojis"):
    """
    takes an emoji as UNICODE-string, and renders it to PNG

    Parameters:
    -----------
    emoji
            the emoji as unicode-sring
    filename
            the filename the emoji is saved to
    color
            color the emoji shoud take (If None, it just ouptuts the default emoji)
    output_size
            size of the PNG
    font_size
            size at which the emoji gets rendered
    output_dir
            directory where the emoji is saved

    
    """
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)

    # Load Emoji font
    font_path = get_emoji_font_path()
    font = ImageFont.truetype(font_path, font_size)


    canvas_size = font_size * 2
    image = Image.new("RGBA", (canvas_size , canvas_size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # render the emoji
    bbox = draw.textbbox((0, 0), emoji, font=font, embedded_color=True)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (canvas_size - text_width) // 2 - bbox[0]
    y = (canvas_size - text_height) // 2 - bbox[1]
    draw.text((x, y), emoji, font=font, embedded_color=True)
    (a,b,c,d) = image.getbbox()

    cropped = image.crop((a-10, b-10, c + 10, d + 10))
    # final = cropped.resize((output_size  , output_size ), resample=Image.LANCZOS)
    final = ImageOps.contain(cropped, (output_size  , output_size ))

    # recolor if neccessary
    if not color is None:
        (f1,f2,f3,alpha) = final.split()
        final = final.convert('L')
        final = ImageOps.colorize(final,black = "white", white = color)
        final.putalpha(alpha)

        # set the color of all pixels that should not be visible to BLACK (since manim sometimes deletes the alpha channel)
        pixels = final.load()          
        for y in range(final.height): 
            for x in range(final.width):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    pixels[x, y] = (0, 0, 0, 0)

    final.save(full_path)
    return full_path
