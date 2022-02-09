from constant import FONT_HEIGHT

def get_font_size(font_height):
    if font_height < 19:
        return 12
    else:
        i = 0
        while font_height > FONT_HEIGHT[i]:
            i += 1
        return i + 12