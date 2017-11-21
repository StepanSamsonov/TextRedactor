from PIL import Image, ImageDraw, ImageFont, ImageTk


def generate_letter(letter, font='arial', dop_mode=''):
    def get_coords(pix, x, y):
        def obhod(x, i):
            stack.append((x, i))
            while len(stack) != 0:
                a, b = stack.pop()
                visited.add((a, b))
                for k in range(-1, 2, 2):
                    for q in range(-1, 2, 2):
                        try:
                            if pix[a + k, b + q] != (255, 255, 255) and (a + k, b + q) not in visited:
                                stack.append((a + k, b + q))
                        except BaseException:
                            pass

        r, l, t, b = 0, 1000000, 1000000, 0
        width, height = size_imgs, size_imgs
        stack = []
        visited = set()
        while x <= width:
            i = height
            while i > 0:
                if pix[x, i] != (255, 255, 255):
                    obhod(x, i)
                    for elem in visited:
                        if elem[0] > r:
                            r = elem[0]
                        if elem[0] < l:
                            l = elem[0]
                        if elem[1] < t:
                            t = elem[1]
                        if elem[1] > b:
                            b = elem[1]
                    return r, l, t, b
                i -= 1
            x += 1
        return r, l, t, b

    size_imgs = 400
    loc_img = Image.new('RGB', (size_imgs, size_imgs), (255, 255, 255))
    loc_draw = ImageDraw.Draw(loc_img)
    font += dop_mode
    kek = 200
    if dop_mode == 'b':
        try:
            font = ImageFont.truetype(font + '.ttf', kek)
        except BaseException:
            font = ImageFont.truetype(font + 'd' + '.ttf', kek)
    else:
        font = ImageFont.truetype(font + '.ttf', kek)
    L_loc_img = Image.new('RGB', (size_imgs, size_imgs), (255, 255, 255))
    L_loc_draw = ImageDraw.Draw(L_loc_img)
    L_loc_draw.text((0, 0), 'L', (0, 0, 0), font)
    L_pixels = L_loc_img.load()
    L_width = L_loc_img.size[0]
    L_height = L_loc_img.size[1]
    L_left_pix = 10000
    L_right_pix = 0
    L_top_pix = 10000
    L_bottom_pix = 0
    for i in range(L_width):
        for j in range(L_height):
            if L_pixels[i, j] != (255, 255, 255):
                if i < L_left_pix:
                    L_left_pix = i
                if i > L_right_pix:
                    L_right_pix = i
                if j < L_top_pix:
                    L_top_pix = j
                if j > L_bottom_pix:
                    L_bottom_pix = j
    L_height_lettet = L_bottom_pix - L_top_pix
    Ls_loc_img = Image.new('RGB', (size_imgs * 2, size_imgs * 2), (255, 255, 255))
    Ls_loc_draw = ImageDraw.Draw(Ls_loc_img)
    Ls_loc_draw.text((0, 0), 'L ' + letter, (0, 0, 0), font)
    Ls_pixels = Ls_loc_img.load()
    x, y = 0, size_imgs
    right, left, top, bottom = get_coords(Ls_pixels, x, y)
    a, b, c, bottom_for_letter = get_coords(Ls_pixels, right + 20, top)
    diff = (bottom_for_letter - bottom)
    loc_draw.text((20, 0), letter, (0, 0, 0), font)
    pixels = loc_img.load()
    width = loc_img.size[0]
    height = loc_img.size[1]
    left_pix = 10000
    right_pix = 0
    top_pix = 10000
    bottom_pix = 0
    for i in range(width):
        for j in range(height):
            if pixels[i, j] != (255, 255, 255):
                if i < left_pix:
                    left_pix = i
                if i > right_pix:
                    right_pix = i
                if j < top_pix:
                    top_pix = j
                if j > bottom_pix:
                    bottom_pix = j
    loc_img = loc_img.crop((left_pix, top_pix, right_pix + 1, bottom_pix + 1))
    k = loc_img.size[1] / L_height_lettet
    return str(diff), str(k), str(left_pix), str(top_pix), str(right_pix + 1), str(bottom_pix + 1)

    loc_img = Image.new('RGB', (300, 300), (255, 255, 255))
    loc_draw = ImageDraw.Draw(loc_img)
    font += dop_mode
    kek = 200
    if dop_mode == 'b':
        try:
            font = ImageFont.truetype(font + '.ttf', kek)
        except BaseException:
            font = ImageFont.truetype(font + 'd' + '.ttf', kek)
    else:
        font = ImageFont.truetype(font + '.ttf', kek)
    L_loc_img = Image.new('RGB', (300, 300), (255, 255, 255))
    L_loc_draw = ImageDraw.Draw(L_loc_img)
    L_loc_draw.text((0, 0), 'L', (0, 0, 0), font)
    L_pixels = L_loc_img.load()
    L_width = L_loc_img.size[0]
    L_height = L_loc_img.size[1]
    L_left_pix = 10000
    L_right_pix = 0
    L_top_pix = 10000
    L_bottom_pix = 0
    for i in range(L_width):
        for j in range(L_height):
            if L_pixels[i, j] != (255, 255, 255):
                if i < L_left_pix:
                    L_left_pix = i
                if i > L_right_pix:
                    L_right_pix = i
                if j < L_top_pix:
                    L_top_pix = j
                if j > L_bottom_pix:
                    L_bottom_pix = j
    L_height_lettet = L_bottom_pix - L_top_pix
    Ls_loc_img = Image.new('RGB', (700, 700), (255, 255, 255))
    Ls_loc_draw = ImageDraw.Draw(Ls_loc_img)
    Ls_loc_draw.text((0, 0), 'L ' + letter, (0, 0, 0), font)
    Ls_pixels = Ls_loc_img.load()
    x, y = 0, 300
    right, left, top, bottom = get_coords(Ls_pixels, x, y)
    a, b, c, bottom_for_letter = get_coords(Ls_pixels, right+20, top)
    diff = (bottom_for_letter - bottom)
    loc_draw.text((20, 0), letter, (0, 0, 0), font)
    pixels = loc_img.load()
    width = loc_img.size[0]
    height = loc_img.size[1]
    left_pix = 10000
    right_pix = 0
    top_pix = 10000
    bottom_pix = 0
    for i in range(width):
        for j in range(height):
            if pixels[i, j] != (255, 255, 255):
                if i < left_pix:
                    left_pix = i
                if i > right_pix:
                    right_pix = i
                if j < top_pix:
                    top_pix = j
                if j > bottom_pix:
                    bottom_pix = j
    loc_img = loc_img.crop((left_pix, top_pix, right_pix+1, bottom_pix+1))
    k = loc_img.size[1]/L_height_lettet
    return str(diff), str(k), str(left_pix), str(top_pix), str(right_pix+1), str(bottom_pix+1)


data = open('Keyboard symbols.txt').readline()
data = set(list(data.rstrip()))
answer = []
for dop_mode in ['', 'b', 'i']:
    for i, elem in enumerate(data):
        print(i, len(data), elem, dop_mode)
        answer.append(elem + ' ' + dop_mode + ' ' + ' '.join(generate_letter(elem, dop_mode=dop_mode)))
text = open('Symbol_add_data.txt', 'w')
text.write('\n'.join(answer))
