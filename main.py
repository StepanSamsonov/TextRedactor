import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
from tkinter.filedialog import askdirectory
from win32api import GetSystemMetrics


def new_editor(given_letter=None, given_font=None, size_of_cell=None, is_my_symbol=False):
    def coloring(event):
        nonlocal flag_for_action
        flag_for_action = True
        x = (event.x // size_of_cell)*size_of_cell
        y = (event.y // size_of_cell)*size_of_cell
        cnv_for_editor.create_rectangle(x, y, x+size_of_cell, y+size_of_cell, fill=fill_for_coloring)
        letter_draw.rectangle([x, y, x+size_of_cell, y+size_of_cell], fill=fill_for_coloring)

    def change_to_white():
        nonlocal fill_for_coloring
        fill_for_coloring = 'white'

    def change_to_black():
        nonlocal fill_for_coloring
        fill_for_coloring = 'black'

    def apply_change_cell():
        def changing():
            nonlocal flag_for_action
            if flag_for_action:
                attention_window.destroy()
            flag_for_action = False
            cnv_for_editor.delete('all')
            nonlocal size_of_cell
            try:
                if int(change_cell.get()) <= 0:
                    raise BaseException
                size_of_cell = int(change_cell.get())
            except BaseException:
                error_correct_data(editor_window)
            create_cells()

        def closing():
            attention_window.destroy()

        if flag_for_action:
            attention_window = tk.Toplevel(editor_window)
            attention_window.title('')
            attention_window.geometry('200x60')
            attention_window.resizable(0, 0)
            attention_label = tk.Label(attention_window, text='All your progress will be lost.\n Are you sure?')
            attention_label.pack()
            attention_button_yes = tk.Button(attention_window, text='Yes', command=changing)
            attention_button_no = tk.Button(attention_window, text='No', command=closing)
            attention_button_yes.pack()
            attention_button_no.pack()
        else:
            changing()

    def create_cells():
        for i in range(0, width_of_editor_cnv, size_of_cell):
            cnv_for_editor.create_line(i, 0, i, height_of_editor_cnv)
        for i in range(0, height_of_editor_cnv, size_of_cell):
            cnv_for_editor.create_line(0, i, width_of_editor_cnv, i)

    def save_letter():
        name = name_letter.get()
        lines = open('My letters\\List_of_letters.txt').readlines()
        for elem in lines:
            if name == elem.split(' ')[0][0:-4]:
                error_label = tk.Label(editor_window, text='This name exists, choose other!')
                error_label.place(relx=0.1, rely=0.75)
                return None
        letter_image.save('My letters\\' + name + '.jpg')
        icon_letter_image = letter_image.resize((50, 50), Image.ANTIALIAS)
        icon_letter_image.save('My letters\\Icons\\' + name + '.jpg')
        lines.append(name+'.jpg ' + name + '\n')
        lines = ''.join(lines)
        text = open('My letters\\List_of_letters.txt', 'w')
        text.write(lines)
        text.close()

    flag_for_action = False
    width_of_editor_cnv = 300
    height_of_editor_cnv = 300
    if not size_of_cell:
        size_of_cell = int(cell_size)
    else:
        size_of_cell = int(size_of_cell)
    fill_for_coloring = 'black'
    editor_window = tk.Toplevel(window)
    editor_window.title('Symbol Editor')
    editor_window.geometry('600x300')
    editor_window.resizable(0, 0)

    cell_frame = tk.LabelFrame(editor_window, text='Size of cell')
    cell_frame.place(relx=0.55, rely=0.1)
    change_cell = tk.Entry(cell_frame)
    change_cell.insert(0, size_of_cell)
    change_cell.grid(row=1, column=0)
    change_cell_button = tk.Button(cell_frame, text='Apply', command=apply_change_cell)
    change_cell_button.grid(row=1, column=1)

    color_frame = tk.LabelFrame(editor_window, text='Color')
    color_frame.place(relx=0.55, rely=0.4)
    var_rb = tk.StringVar()
    var_rb.set('Black')
    white_rb = tk.Radiobutton(color_frame, variable=var_rb, value='White', command=change_to_white, text='White')
    black_rb = tk.Radiobutton(color_frame, variable=var_rb, value='Black', command=change_to_black, text='Black')
    white_rb.grid(row=1, column=1)
    black_rb.grid(row=1, column=0)

    cnv_for_editor = tk.Canvas(editor_window, width=width_of_editor_cnv, height=height_of_editor_cnv, bg='white')
    cnv_for_editor.bind("<Button-1>", coloring)
    cnv_for_editor.place(relx=0, rely=0)
    create_cells()

    letter_image = Image.new('RGB', (width_of_editor_cnv, height_of_editor_cnv), (255, 255, 255))
    letter_draw = ImageDraw.Draw(letter_image)

    save_frame = tk.LabelFrame(editor_window, text='Enter the name of the symbol')
    save_frame.place(relx=0.55, rely=0.7)
    save_letter_butt = tk.Button(save_frame, text='Save', command=save_letter)
    save_letter_butt.grid(row=1, column=1)
    name_letter = tk.Entry(save_frame)
    name_letter.grid(row=1, column=0)

    class FakeEvent:
        x = 0
        y = 0

        def __init__(self, x, y):
            self.x = x
            self.y = y

    coords = []
    if is_my_symbol:
        given_letter = given_letter[1:-1]
        coords = insert_my_letter(given_letter, flag=False)

    elif given_font and given_letter and size_of_cell:
        coords, size_of_letter = generate_letter(letter=given_letter, font=given_font, size=295, mode='solid', dop_mode='')
    for elem in coords:
        fake = FakeEvent(elem[0], elem[1])
        coloring(fake)


def transform(n):
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    diag = (w**2 + h**2)**(1/2)
    d_to_mm = n*25.4
    pix_per_mm = diag/d_to_mm
    mm_per_pix = d_to_mm/diag
    return pix_per_mm, mm_per_pix


def pix_to_mm(n):
    return round(n*mm_per_pix, 2)


def mm_to_pixel(n):
    return round(n*pix_per_mm)


def mm_to_inches(n):
    return n*0.0393701


def pix_to_inches(n):
    return mm_to_inches(pix_to_mm(n))


def open_editor():
    def open_editor_command():
        letter = letter_name_entry.get()
        is_my_letter = False
        if len(letter) > 1:
            if letter[0] == '*' and letter[-1] == '*':
                is_my_letter = True
                lines = open('My letters\\List_of_letters.txt').readlines()
                found = False
                for elem in lines:
                    psy = elem.split(' ')[1].rstrip()
                    if letter[1:-1] == psy:
                        found = True
                        break
                if not found:
                    def n_f_closing():
                        not_found_window.destroy()

                    not_found_window = tk.Toplevel(open_window)
                    not_found_label = tk.Label(not_found_window, text='Symbol is not found')
                    not_found_label.pack()
                    not_found_butt = tk.Button(not_found_window, text='Ok', command=n_f_closing)
                    not_found_butt.pack()
                    return None
            else:
                def closing():
                    error_window.destroy()

                error_window = tk.Toplevel(open_window)
                error_window.resizable(0, 0)
                error_label = tk.Label(error_window, text='Only one symbol is supported')
                error_label.pack()
                error_butt = tk.Button(error_window, text='Ok', command=closing)
                error_butt.pack()
                return None
        global cell_size
        try:
            if int(cell_size_entry.get()) <= 0:
                raise BaseException
        except BaseException:
            error_correct_data(open_window)
            return None
        cell_size = int(cell_size_entry.get())
        open_window.destroy()
        new_editor(given_letter=letter, given_font=current_font, is_my_symbol=is_my_letter)

    open_window = tk.Toplevel(window)
    open_window.title('Open')
    open_window.geometry('250x100')
    open_window.resizable(0, 0)
    open_frame = tk.LabelFrame(open_window)
    open_frame.place(relx=0.1, rely=0.1)
    letter_name_label = tk.Label(open_frame, text='Write a letter:')
    cell_size_label = tk.Label(open_frame, text='Write cell size:')
    letter_name_entry = tk.Entry(open_frame)
    cell_size_entry = tk. Entry(open_frame)
    cell_size_entry.insert(tk.END, 10)
    enter_open_button = tk.Button(open_window, text='Enter', command=open_editor_command)
    letter_name_label.grid(row=0, column=0)
    letter_name_entry.grid(row=0, column=1)
    cell_size_label.grid(row=1, column=0)
    cell_size_entry.grid(row=1, column=1)
    enter_open_button.place(relx=0.2, rely=0.6)


def open_list_of_my_letters():
    def change_names():
        lines = open('My letters\\List_of_letters.txt').readlines()
        text = open('My letters\\List_of_letters.txt', 'w')
        for i, elem in enumerate(list_of_labels):
            if elem.get() != '':
                file_name, ps = lines[i].split(' ')
                ps = elem.get()
                lines[i] = file_name + ' ' + ps + '\n'
            else:
                error_correct_data(oloml_window)
                text.write(''.join(lines))
                text.close()
                return None
        text.write(''.join(lines))
        text.close()

    def del_letters():
        def del_chosen():
            lines = open('My letters\\List_of_letters.txt').readlines()
            text = open('My letters\\List_of_letters.txt', 'w')
            i = 0
            while i < len(lines):
                elem = list_of_check_var[i]
                if elem.get():
                    name = (lines[i].split(' '))[0]
                    del lines[i]
                    del list_of_check_var[i]
                    os.remove('My letters\\' + name)
                    os.remove('My letters\\Icons\\' + name)
                    i -= 1
                i += 1
            text.write(''.join(lines))
            text.close()
            oloml_window.destroy()
            open_list_of_my_letters()

        new_appl_butt = tk.Button(show_frame, text='Apply', command=del_chosen)
        new_appl_butt.grid(row=0, column=0)
        butt_del.grid_forget()
        butt_appl.grid_forget()
        for elem in list_of_labels:
            elem.grid_forget()
        for i, elem in enumerate(list_of_check):
            elem.grid(row=i+1, column=1)

    def on_configure(event):
        loc_cnv.configure(scrollregion=loc_cnv.bbox('all'))

    oloml_window = tk.Toplevel(window)
    oloml_window.title('List')
    oloml_window.geometry('200x250')
    oloml_window.resizable(0, 0)
    loc_cnv = tk.Canvas(oloml_window, width=200, height=250)
    loc_cnv.place(relx=0, rely=0)
    scroll = tk.Scrollbar(oloml_window, command=loc_cnv.yview)
    scroll.place(relx=0.91, rely=0, relheight=1)
    loc_cnv.configure(yscrollcommand=scroll.set)
    show_frame = tk.Frame(loc_cnv, width=200, height=250)
    loc_cnv.create_window((0, 0), window=show_frame, anchor='nw')

    list_of_letters = open('My letters\\List_of_letters.txt').readlines()
    list_of_labels = []
    list_of_check = []
    list_of_check_var = []
    for i, elem in enumerate(list_of_letters):
        name, pseudonym = elem.split(' ')
        img = ImageTk.PhotoImage(file='My letters\\Icons\\' + name)
        panel = tk.Label(show_frame, image=img)
        panel.image = img
        panel.grid(row=i+1, column=0)
        label = tk.Entry(show_frame, width=10)
        label.grid(row=i+1, column=1)
        label.insert(tk.END, pseudonym.rstrip())
        check_var = tk.IntVar()
        check_but = tk.Checkbutton(show_frame, variable=check_var, onvalue=1, offvalue=0)
        list_of_check.append(check_but)
        list_of_check_var.append(check_var)
        list_of_labels.append(label)
    butt_appl = tk.Button(show_frame, text='Apply', command=change_names)
    butt_appl.grid(row=0, column=0)
    butt_del = tk.Button(show_frame, text='Delete', command=del_letters)
    butt_del.grid(row=0, column=1)
    loc_cnv.bind('<Configure>', on_configure)


def generate_dot_letter(pix, width, height):
    global dot_cell_size, dot_space_for_cell
    dot_cell_size = 3
    dot_space_for_cell = 1
    coords = []
    for i in range(dot_cell_size, width, dot_cell_size):
        for j in range(dot_cell_size, height, dot_cell_size):
            check = False
            most_colored = (255, 255, 255)
            for k in range(i-dot_cell_size, i):
                for l in range(j-dot_cell_size, j):
                    if pix[k, l] != (255, 255, 255):
                        check = True
                        if (pix[k, l][0] < most_colored[0] or pix[k, l][1] < most_colored[1]
                            or pix[k, l][2] < most_colored[2]):
                            most_colored = pix[k, l]
            if check:
                for k in range(i-dot_cell_size+dot_space_for_cell, i-dot_space_for_cell):
                    for l in range(j-dot_cell_size+dot_space_for_cell, j-dot_space_for_cell):
                        coords.append((k, l, most_colored))
    return coords


def generate_line_letter(pix, width, height):
    global line_line_width, line_space_for_cell
    line_line_width = 3
    line_space_for_cell = 1
    coords = []
    for i in range(line_line_width, height, line_line_width):
        for j in range(width):
            for k in range(line_space_for_cell):
                try:
                    pix[j, i+k] = (255, 255, 255)
                except:
                    pass
    for i in range(width):
        for j in range(height):
            if pix[i, j] != (255, 255, 255):
                coords.append((i, j, pix[i, j]))
    return coords


def generate_letter(letter, font, size, mode, dop_mode):
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
    loc_draw.text((0, 0), letter, (0, 0, 0), font)
    data = open('Symbol_add_data.txt').readlines()
    k = 1
    diff = 0
    left_pix, top_pix, right_pix, bottom_pix = 0, 0, 0, 0
    for elem in data:
        elem = elem.rstrip().split(' ')
        if letter == elem[0]:
            diff = int(elem[1])
            k = float(elem[2])
            left_pix = int(elem[3])
            top_pix = int(elem[4])
            right_pix = int(elem[5])
            bottom_pix = int(elem[6])
    loc_img = loc_img.crop((left_pix, top_pix, right_pix + 1, bottom_pix + 1))

    before = loc_img.size[1]
    loc_img = loc_img.resize((round(loc_img.size[0]*(size/loc_img.size[1])*k), round(size*k)), Image.ANTIALIAS)
    coords = []
    pix = loc_img.load()
    width = loc_img.size[0]
    height = loc_img.size[1]

    if mode == 'dot':
        coords = generate_dot_letter(pix, width, height)
        return coords, round(size*k - diff*size*k/before)
    if mode == 'line':
        coords = generate_line_letter(pix, width, height)
        return coords, round(size*k - diff*size*k/before)
    for i in range(width):
        for j in range(height):
            if pix[i, j] != (255, 255, 255):
                coords.append([i, j, pix[i, j]])
    if letter == '%':
        diff = 0
    return coords, round(size*k - diff*size*k/before)


def write_letter(letter_coords, begin_x, begin_y, bold, size_of_leteer, space, local_font_size, add_space):
    new_x = 0
    for i, elem in enumerate(letter_coords):
        r, g, b = elem[2]
        if bold >= 0:
            r = int(r * (1 - (bold / 100)))
            g = int(g * (1 - (bold / 100)))
            b = int(b * (1 - (bold / 100)))
        else:
            r = int(r - (255 - r)*bold/100)
            g = int(g - (255 - g)*bold/100)
            b = int(b - (255 - b)*bold/100)
        letter_coords[i] = list(letter_coords[i])
        letter_coords[i][2] = (r, g, b)
    for elem in letter_coords:
        if elem[0]+begin_x+right_space_cnv > width_of_cnv:
            begin_x = left_space_cnv
            begin_y = begin_y + (local_font_size+add_space)*1.325 + space_betwen_lines
        if elem[1]+begin_y+bottom_space_cnv > height_of_cnv:
            return begin_x, begin_y, 'space'
    for elem in letter_coords:
        r, g, b = elem[2]
        img_from_tk_cnv_draw.point((elem[0]+begin_x, elem[1]+begin_y+local_font_size+add_space-size_of_leteer), "#%02x%02x%02x" % (r, g, b))
        if elem[0] > new_x:
            new_x = elem[0]
    return new_x + space + begin_x, begin_y, 'ok'


def insert_my_letter(name, flag=True):
    def closing():
        error_window.destroy()

    lines = open('My letters\\List_of_letters.txt').readlines()
    file_name = None
    for elem in lines:
        elem = elem.split(' ')
        if name == elem[1].rstrip():
            file_name = elem[0]
            break
    if not file_name and flag:
        error_window = tk.Toplevel(window)
        error_window.resizable(0, 0)
        error_label = tk.Label(error_window, text='Symbol "' + name + '" is not found')
        error_label.pack()
        error_butt = tk.Button(error_window, text='Ok', command=closing)
        error_butt.pack()
        return 'error'
    loc_img = Image.open('My letters\\' + file_name)
    if flag:
        loc_img = loc_img.resize((size_of_font, size_of_font), Image.ANTIALIAS)
    pix = loc_img.load()
    coords = []
    width = loc_img.size[0]
    height = loc_img.size[1]
    if flag:
        if letter_mode == 'dot':
            coords = generate_dot_letter(pix, width, height)
            return coords
        if letter_mode == 'line':
            coords = generate_line_letter(pix, width, height)
            return coords

    for i in range(width):
        for j in range(height):
            if pix[i, j] != (255, 255, 255):
                coords.append([i, j, pix[i, j]])
    return coords


class Symbol:
    is_my_letter = None
    name = None
    bolding = None
    mode = None
    dop_mode = None
    size = None
    font = None
    space = None
    line_space = None
    add_space_for_size = None

    def __init__(self, is_my_letter, name, bolding, mode, dop_mode, size, font, space, line_space):
        self.is_my_letter = is_my_letter
        self.name = name
        self.bolding = bolding
        self.mode = mode
        self.dop_mode = dop_mode
        self.size = size
        self.font = font
        self.space = space
        self.line_space = line_space
        self.add_space_for_size = 0

    def __eq__(self, other):
        return self.name == other.name


array_of_symbols = []


def get_text():
    def find_name(given_text, ind):
        ind += 1
        start = ind
        if ind == len(given_text):
            return '', ind
        else:
            while given_text[ind] != '*':
                ind += 1
                if ind == len(given_text):
                    return '', start
        return given_text[start:ind], ind

    def parse(text):
        i = 0
        new_array_of_symbol = []
        while i < len(text):
            if text[i] == '*':
                name, i = find_name(text, i)
                if name == '':
                    new_array_of_symbol.append(Symbol(False, '*', bold, letter_mode, dop_mode, size_of_font, current_font, space_betwen_letters, space_betwen_lines))
                    if i < len(text):
                        while text[i] == '*':
                            new_array_of_symbol.append(Symbol(False, '*', bold, letter_mode, dop_mode, size_of_font, current_font, space_betwen_letters, space_betwen_lines))
                            i += 1
                            if i == len(text):
                                break
                        i -= 1
                else:
                    new_array_of_symbol.append(Symbol(True, name, bold, letter_mode, dop_mode, size_of_font, current_font, space_betwen_letters, space_betwen_lines))
            else:
                new_array_of_symbol.append(Symbol(False, text[i], bold, letter_mode, dop_mode, size_of_font, current_font, space_betwen_letters, space_betwen_lines))
            i += 1
        return new_array_of_symbol

    def inserted(a, b):
        bias = 0
        if len(b) == 0:
            return True
        if len(a) < len(b):
            return False
        for _, _ in enumerate(a):
            try:
                start = a[bias:].index(b[0])
            except ValueError:
                return False
            for i, elem in enumerate(b):
                if a[start + i] != elem:
                    bias = start + 1
                    break
                if i == len(b) - 1:
                    return True
            if bias >= len(a):
                return False

    global array_of_symbols
    global panel_for_cnv, img_from_tk_cnv
    global photoimg_from_tk_cnv, img_from_tk_cnv_draw, img_from_tk_cnv
    text = text_for_cnv.get('1.0', tk.END).rstrip()
    old_text = ''
    for elem in array_of_symbols:
        if not elem.is_my_letter:
            old_text += elem.name
        else:
            old_text += '*' + elem.name + '*'
    old_text_arr = array_of_symbols
    text_arr = parse(text)
    if text_arr == old_text_arr:
        return None
    elif text_arr == [] and old_text_arr != []:
        array_of_symbols = []
        img_from_tk_cnv = Image.new('RGB', (width_of_cnv, height_of_cnv), 'white')
        photoimg_from_tk_cnv = ImageTk.PhotoImage(img_from_tk_cnv)
        img_from_tk_cnv_draw = ImageDraw.Draw(img_from_tk_cnv)
        main_cnv.create_image((0, 0),
                                   image=photoimg_from_tk_cnv, state='normal', anchor='nw')
        main_cnv.image = photoimg_from_tk_cnv

    elif inserted(text_arr, old_text_arr) and old_text_arr != [] and text != []:
        if len(text.split(old_text)) == 2:
            left_text, right_text = text.split(old_text)
        else:
            arr = text.split(old_text)
            left_text = arr[0]
            right_text = text[len(left_text) + len(old_text):]

        new_array_of_symbol = parse(left_text)

        for elem in reversed(new_array_of_symbol):
            array_of_symbols.insert(0, elem)

        new_array_of_symbol = parse(right_text)

        for elem in new_array_of_symbol:
            array_of_symbols.append(elem)

    elif inserted(old_text_arr, text_arr) and old_text_arr != [] and text_arr != []:
        if len(old_text.split(text)) == 2:
            left_text, right_text = old_text.split(text)
        else:
            arr = old_text.split(text)
            left_text = arr[0]
            right_text = old_text[len(left_text) + len(text):]
        new_array_of_symbol = parse(left_text)
        for elem in reversed(new_array_of_symbol):
            del array_of_symbols[0]

        new_array_of_symbol = parse(right_text)
        for elem in reversed(new_array_of_symbol):
            del array_of_symbols[-1]

    else:
        array_of_symbols = parse(text)
    star_begin = False
    global begin_x, begin_y
    begin_x = left_space_cnv
    begin_y = top_space_cnv
    img_from_tk_cnv = Image.new('RGB', (width_of_cnv, height_of_cnv), 'white')
    photoimg_from_tk_cnv = ImageTk.PhotoImage(img_from_tk_cnv)
    img_from_tk_cnv_draw = ImageDraw.Draw(img_from_tk_cnv)
    space_over = False

    max_space = 0
    start_line = 0
    for i, symbol in enumerate(array_of_symbols):
        if max_space < symbol.size:
            max_space = symbol.size
        if symbol.name == '\n':
            for j, elem in enumerate(array_of_symbols[start_line:i]):
                array_of_symbols[start_line+j].add_space_for_size = max_space - elem.size
            start_line = i + 1
            max_space = 0
            continue
        if i == len(array_of_symbols) - 1:
            for j, elem in enumerate(array_of_symbols[start_line:]):
                array_of_symbols[start_line + j].add_space_for_size = max_space - elem.size
            start_line = i + 1
            max_space = 0
            continue

    for i, symbol in enumerate(array_of_symbols):
        if symbol.name == '*' and not star_begin:
            star_begin = True
            continue
        if star_begin and symbol.name != '*':
            star_begin = False
        if symbol.name == '*' and star_begin:
            letter_coords, size_of_letter = generate_letter('*', symbol.font, symbol.size, symbol.mode, symbol.dop_mode)
            begin_x, begin_y, ans = write_letter(letter_coords, begin_x, begin_y, symbol.bolding, size_of_letter, symbol.space, symbol.size, symbol.add_space_for_size)
            if ans == 'space':
                space_over = True
            photoimg_from_tk_cnv = ImageTk.PhotoImage(img_from_tk_cnv)
            main_cnv.create_image((0, 0),
                                       image=photoimg_from_tk_cnv, state='normal', anchor='nw')
            main_cnv.image = photoimg_from_tk_cnv
            continue
        if symbol.is_my_letter:
            letter_coords = insert_my_letter(symbol.name)
            if letter_coords == 'error':
                return None
            begin_x, begin_y, ans = write_letter(letter_coords, begin_x, begin_y, symbol.bolding, symbol.size, symbol.space, symbol.size, symbol.add_space_for_size)
            if ans == 'space':
                space_over = True
            photoimg_from_tk_cnv = ImageTk.PhotoImage(img_from_tk_cnv)
            main_cnv.create_image((0, 0),
                                   image=photoimg_from_tk_cnv, state='normal', anchor='nw')
            main_cnv.image = photoimg_from_tk_cnv
        else:
            if symbol.name == ' ':
                begin_x += symbol.size//2
            elif symbol.name == '\n':
                begin_x = left_space_cnv
                space_line_arr = []
                for symb in reversed(array_of_symbols[:i]):
                    if symb.name == '\n':
                        break
                    space_line_arr.append(symb.line_space)
                if len(space_line_arr) == 0:
                    space_line_arr.append(space_betwen_lines)
                down = 0
                for elem in reversed(array_of_symbols[:i]):
                    if elem.name == '\n':
                        break
                    if down < elem.size + elem.add_space_for_size:
                        down = elem.size + elem.add_space_for_size

                begin_y = begin_y + down*1.325 + symbol.line_space
            else:
                letter_coords, size_of_letter = generate_letter(symbol.name, symbol.font, symbol.size, symbol.mode, symbol.dop_mode)
                begin_x, begin_y, ans = write_letter(letter_coords, begin_x, begin_y, symbol.bolding, size_of_letter, symbol.space, symbol.size, symbol.add_space_for_size)
                if ans == 'space':
                    space_over = True
                photoimg_from_tk_cnv = ImageTk.PhotoImage(img_from_tk_cnv)
                main_cnv.create_image((0, 0),
                                           image=photoimg_from_tk_cnv, state='normal', anchor='nw')
                main_cnv.image = photoimg_from_tk_cnv
    if space_over:
        def closing():
            space_end_window.destroy()

        space_end_window = tk.Toplevel(window)
        tk.Label(space_end_window, text='Space is over').pack()
        tk.Button(space_end_window, text='Ok', command=closing).pack()


def open_default_settings():
    def apply_default():
        may_be = open('Settings\\Common settings.txt').readlines()
        text = open('Settings\\Common settings.txt', 'w')
        list_of_param = []
        for i, elem in enumerate(list_of_settings):
            if i == 0:
                if elem.get() == 'solid' or elem.get() == 'dot' or elem.get() == 'line':
                    list_of_param.append(elem.get())
                else:
                    error_correct_data(settings_window)
                    text.write(''.join(may_be))
                    text.close()
                    return None
            elif 0 < i < 10:
                try:
                    if float(elem.get()) >= 0:
                        list_of_param.append(str(mm_to_pixel(float(elem.get()))))
                    else:
                        raise BaseException
                except BaseException:
                    error_correct_data(settings_window)
                    text.write(''.join(may_be))
                    text.close()
                    return None
            elif i == 11 or i == 10:
                try:
                    if int(elem.get()) > 0:
                        list_of_param.append(str(int(elem.get())))
                    else:
                        raise BaseException
                except BaseException:
                    error_correct_data(settings_window)
                    text.write(''.join(may_be))
                    text.close()
                    return None
            elif i == 12:
                try:
                    if float(elem.get()) > 0:
                        list_of_param.append(str(float(elem.get())))
                    else:
                        raise BaseException
                except BaseException:
                    error_correct_data(settings_window)
                    text.write(''.join(may_be))
                    text.close()
                    return None
            else:
                list_of_param.append(str(elem.get()))
        list_of_param.append('250')
        list_of_param.append('450')
        text.write('\n'.join(list_of_param))
        text.close()
        init()
        height_cnv_entry.delete(0, tk.END)
        height_cnv_entry.insert(tk.END, str(pix_to_mm(height_of_cnv)))
        width_cnv_entry.delete(0, tk.END)
        width_cnv_entry.insert(tk.END, str(pix_to_mm(width_of_cnv)))
        size_of_font_entry.delete(0, tk.END)
        size_of_font_entry.insert(tk.END, str(pix_to_mm(size_of_font)))
        space_betwen_letters_entry.delete(0, tk.END)
        space_betwen_letters_entry.insert(tk.END, str(pix_to_mm(space_betwen_letters)))
        space_betwen_lines_entry.delete(0, tk.END)
        space_betwen_lines_entry.insert(tk.END, str(pix_to_mm(space_betwen_lines)))

    def ok():
        apply_default()
        settings_window.destroy()

    def factory():
        def yes():
            sure_window.destroy()
            text = open('Settings\\Common settings.txt', 'w')
            lines = open('Settings\\Factory common settings.txt').readlines()
            text.write(''.join(lines))
            text.close()
            settings_window.destroy()
            init()
            open_default_settings()

        def no():
            sure_window.destroy()

        sure_window = tk.Toplevel(settings_window)
        sure_window.title('')
        sure_window.geometry('200x60')
        sure_window.resizable(0, 0)
        tk.Label(sure_window, text='Are you sure?').place(relx=0.3, rely=0.1)
        yes_butt = tk.Button(sure_window, text='Yes', command=yes)
        yes_butt.place(relx=0.25, rely=0.5)
        no_butt = tk.Button(sure_window, text='No', command=no)
        no_butt.place(relx=0.6, rely=0.5)

    settings_window = tk.Toplevel(window)
    settings_window.title('Common')
    settings_window.geometry('260x420')
    settings_window.resizable(0, 0)
    settings_frame = tk.LabelFrame(settings_window, height=300, width=300)
    settings_frame.place(relx=0.15, rely=0.05)
    tk.Label(settings_frame, text='Mode:').grid(row=0, column=0)
    tk.Label(settings_frame, text='Size of symbols:').grid(row=1, column=0)
    tk.Label(settings_frame, text='Space between symbols:').grid(row=2, column=0)
    tk.Label(settings_frame, text='Space between lines:').grid(row=3, column=0)
    tk.Label(settings_frame, text='Width of canvas:').grid(row=4, column=0)
    tk.Label(settings_frame, text='Height of canvas:').grid(row=5, column=0)
    tk.Label(settings_frame, text='Right indentation:').grid(row=6, column=0)
    tk.Label(settings_frame, text='Left indentation:').grid(row=7, column=0)
    tk.Label(settings_frame, text='Top indentation:').grid(row=8, column=0)
    tk.Label(settings_frame, text='Bottom indentation:').grid(row=9, column=0)
    tk.Label(settings_frame, text='Cell size in the editor:').grid(row=10, column=0)
    tk.Label(settings_frame, text='Screen diagonal:').grid(row=11, column=0)
    lines = open('Settings\\Common settings.txt').readlines()
    list_of_settings = []
    for i, elem in enumerate(lines):
        if i < 12:
            entry = tk.Entry(settings_frame, width=6)
            if 0 < i < 10:
                entry.insert(tk.END, pix_to_mm(int(elem.rstrip())))
            else:
                entry.insert(tk.END, elem.rstrip())
            entry.grid(row=i, column=1)
            list_of_settings.append(entry)
    list_of_settings[0].configure(state=tk.DISABLED)
    apply_butt = tk.Button(settings_window, text='Apply', command=apply_default)
    apply_butt.place(relx=0.16, rely=0.9)
    ok_butt = tk.Button(settings_window, text='Ok', command=ok)
    ok_butt.place(relx=0.72, rely=0.9)
    factory_frame = tk.LabelFrame(settings_window)
    factory_frame.place(relx=0.165, rely=0.725)
    tk.Label(factory_frame, text='If you want to reset to the\n factory settings, press "Enter":').pack()
    factory_butt = tk.Button(factory_frame, text='Reset', command=factory)
    factory_butt.pack()


def open_mode_settings():
    def apply_mode():
        try:
            if int(dot_cell_size_entry.get()) <= 0:
                raise BaseException
            if int(dot_space_for_cell_entry.get()) <= 0:
                raise BaseException
            if int(line_line_width_entry.get()) <= 0:
                raise BaseException
            if int(line_space_for_line.get()) <= 0:
                raise BaseException
        except BaseException:
            error_correct_data(mode_settings_window)
            return None
        list_of_param = []
        list_of_param.append(str(dot_cell_size_entry.get()))
        list_of_param.append(str(dot_space_for_cell_entry.get()))
        list_of_param.append(str(line_line_width_entry.get()))
        list_of_param.append(str(line_space_for_line.get()))
        list_of_param.append('250')
        list_of_param.append('450')
        text = open('Settings\\Mode settings.txt', 'w')
        text.write('\n'.join(list_of_param))
        text.close()
        init()

    def ok():
        apply_mode()
        mode_settings_window.destroy()

    def factory():
        def yes():
            sure_window.destroy()
            text = open('Settings\\Mode settings.txt', 'w')
            lines = open('Settings\\Factory mode settings.txt').readlines()
            text.write(''.join(lines))
            text.close()
            mode_settings_window.destroy()
            init()
            open_mode_settings()

        def no():
            sure_window.destroy()

        sure_window = tk.Toplevel(mode_settings_window)
        sure_window.title('')
        sure_window.geometry('200x60')
        sure_window.resizable(0, 0)
        tk.Label(sure_window, text='Are you sure?').place(relx=0.3, rely=0.1)
        yes_butt = tk.Button(sure_window, text='Yes', command=yes)
        yes_butt.place(relx=0.25, rely=0.5)
        no_butt = tk.Button(sure_window, text='No', command=no)
        no_butt.place(relx=0.6, rely=0.5)

    mode_settings_window = tk.Toplevel(window)
    mode_settings_window.title('Mode')
    mode_settings_window.geometry('220x300')
    mode_settings_window.resizable(0, 0)
    settings = open('Settings\\Mode settings.txt').readlines()

    dot_frame = tk.LabelFrame(mode_settings_window, text='Dot')
    dot_frame.place(relx=0.15, rely=0.05)
    tk.Label(dot_frame, text='Size of cell:').grid(row=0, column=0)
    tk.Label(dot_frame, text='Space between cells:').grid(row=1, column=0)
    dot_cell_size_entry = tk.Entry(dot_frame, width=5)
    dot_cell_size_entry.insert(tk.END, int(settings[0].rstrip()))
    dot_cell_size_entry.grid(row=0, column=1)
    dot_space_for_cell_entry = tk.Entry(dot_frame, width=5)
    dot_space_for_cell_entry.insert(tk.END, int(settings[1].rstrip()))
    dot_space_for_cell_entry.grid(row=1, column=1)

    line_frame = tk.LabelFrame(mode_settings_window, text='Line')
    line_frame.place(relx=0.15, rely=0.3)
    tk.Label(line_frame, text='Width of line:').grid(row=0, column=0)
    tk.Label(line_frame, text='Space between lines').grid(row=1, column=0)
    line_line_width_entry = tk.Entry(line_frame, width=5)
    line_line_width_entry.insert(tk.END, int(settings[2].rstrip()))
    line_line_width_entry.grid(row=0, column=1)
    line_space_for_line = tk.Entry(line_frame, width=5)
    line_space_for_line.insert(tk.END, int(settings[3].rstrip()))
    line_space_for_line.grid(row=1, column=1)

    mode_frame_for_reset = tk.LabelFrame(mode_settings_window)
    mode_frame_for_reset.place(relx=0.1, rely=0.55)
    tk.Label(mode_frame_for_reset, text='If you want to reset to the\n factory settings, press "Enter":').pack()
    factory_butt = tk.Button(mode_frame_for_reset, text='Reset', command=factory)
    factory_butt.pack()

    apply_mode_butt = tk.Button(mode_settings_window, text='Apply', command=apply_mode)
    apply_mode_butt.place(relx=0.1, rely=0.8)
    ok_mode_butt = tk.Button(mode_settings_window, text='Ok', command=ok)
    ok_mode_butt.place(relx=0.75, rely=0.8)


def open_doc():
    doc_window = tk.Toplevel(window)
    doc_window.title('Documentation')
    doc_window.geometry('500x480')
    doc_window.resizable(0, 0)
    doc_text = tk.Text(doc_window, height=30, width=60, wrap=tk.WORD)
    doc_text.place(x=0, y=0)
    doc_scroll = tk.Scrollbar(doc_window, command=doc_text.yview)
    doc_text.config(yscrollcommand=doc_scroll.set)
    doc_scroll.place(relx=0.965, rely=0, relheight=1)
    doc = open('Documentation.txt').readlines()
    doc = ''.join(doc)
    doc_text.insert(tk.END, doc)
    doc_text.config(state=tk.DISABLED)


def create_image():
    dir_name = askdirectory()
    frame_im = Image.new('RGB', (width_of_cnv+4, height_of_cnv+4), 'white')
    frame_draw = ImageDraw.Draw(frame_im)
    frame_draw.rectangle((0, 0, 2, height_of_cnv+4), fill='grey')
    frame_draw.rectangle((0, 0, width_of_cnv+4, 2), fill='grey')
    frame_draw.rectangle((0, height_of_cnv+2, width_of_cnv+4, height_of_cnv + 4), fill='grey')
    frame_draw.rectangle((width_of_cnv+2, 0, width_of_cnv+4, height_of_cnv + 4), fill='grey')
    frame_im.paste(img_from_tk_cnv, (2, 2))
    frame_im.save(dir_name + '\\Image.png')


def init():
    # Initialization
    global letter_mode, current_font, size_of_font, space_betwen_letters, space_betwen_lines, width_of_cnv
    global height_of_cnv, default_width_of_cnv, default_height_of_cnv, cell_size, monitor_size
    global left_space_cnv, right_space_cnv, top_space_cnv, bottom_space_cnv
    current_font = 'arial'
    settings = open('Settings\\Common settings.txt').readlines()
    letter_mode = settings[0].rstrip()
    size_of_font = int(settings[1].rstrip())
    space_betwen_letters = int(settings[2].rstrip())
    space_betwen_lines = int(settings[3].rstrip())
    width_of_cnv = int(settings[4].rstrip())
    height_of_cnv = int(settings[5].rstrip())
    right_space_cnv = int(settings[6].rstrip())
    left_space_cnv = int(settings[7].rstrip())
    top_space_cnv = int(settings[8].rstrip())
    bottom_space_cnv = int(settings[9].rstrip())
    cell_size = int(settings[10].rstrip())
    monitor_size = float(settings[11].rstrip())
    default_width_of_cnv = int(settings[12].rstrip())
    default_height_of_cnv = int(settings[13].rstrip())

    global dot_cell_size, dot_space_for_cell
    global line_line_width, line_space_for_cell
    settings = open('Settings\\Mode settings.txt').readlines()
    dot_cell_size = int(settings[0].rstrip())
    dot_space_for_cell = int(settings[1].rstrip())
    line_line_width = int(settings[2].rstrip())
    line_space_for_cell = int(settings[3].rstrip())

    global bold
    bold = 0
    global dop_mode
    dop_mode = ''


def clear_text():
    text_for_cnv.delete('1.0', tk.END)
    get_text()


bold = 0
init()
current_text = ''
begin_x = right_space_cnv
begin_y = top_space_cnv
pix_per_mm, mm_per_pix = transform(monitor_size)


window = tk.Tk()
window.title('Program')
window.geometry('900x480')
window.resizable(0, 0)

menu = tk.Menu(window)
window.config(menu=menu)

# Menu part
fm = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Settings', menu=fm)
fm.add_command(label='Common', command=open_default_settings)
fm.add_command(label='Mode', command=open_mode_settings)
sm = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Symbol editor', menu=sm)
sm.add_command(label='New', command=new_editor)
sm.add_command(label='Open', command=open_editor)
sm.add_command(label='List', command=open_list_of_my_letters)
hm = tk.Menu(menu, tearoff=False)
menu.add_cascade(label='Help', menu=hm)
hm.add_command(label='Doc', command=open_doc)

# Text part
text_frame = tk.LabelFrame(window, width=202, height=150)
text_frame.place(x=600, y=20)
text_for_cnv = tk.Text(text_frame, width=22, height=6, wrap=tk.NONE)
text_for_cnv.place(relx=0, rely=0)

vscroll_for_text = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
text_for_cnv.config(yscrollcommand=vscroll_for_text.set)
vscroll_for_text.config(command=text_for_cnv.yview)
vscroll_for_text.place(relx=0.92, rely=0, relheight=0.65)
hscroll_for_text = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
text_for_cnv.config(xscrollcommand=hscroll_for_text.set)
hscroll_for_text.config(command=text_for_cnv.xview)
hscroll_for_text.place(relx=0, rely=0.65, relwidth=1)

button_for_text = tk.Button(text_frame, text='Get', command=get_text)
button_for_text.place(relx=0.1, rely=0.8)

button_for_image = tk.Button(text_frame, text='Save', command=create_image)
button_for_image.place(relx=0.39, rely=0.8)

button_for_clear = tk.Button(text_frame, text='Clear', command=clear_text)
button_for_clear.place(relx=0.7, rely=0.8)

# Canvas part
main_cnv = tk.Canvas(window, width=width_of_cnv, height=height_of_cnv, bg='white')
img_from_tk_cnv = Image.new('RGB', (width_of_cnv, height_of_cnv), 'white')
photoimg_from_tk_cnv = ImageTk.PhotoImage(img_from_tk_cnv)
img_from_tk_cnv_draw = ImageDraw.Draw(img_from_tk_cnv)
main_cnv.place(x=16, y=10)
main_cnv.create_image((0, 0), image=photoimg_from_tk_cnv, state='normal', anchor='nw')
main_cnv.image = photoimg_from_tk_cnv

vscroll_for_cnv = tk.Scrollbar(window, orient=tk.VERTICAL)
main_cnv.config(yscrollcommand=vscroll_for_cnv.set)
vscroll_for_cnv.config(command=main_cnv.yview)
hscroll_for_cnv = tk.Scrollbar(window, orient=tk.HORIZONTAL)
main_cnv.config(xscrollcommand=hscroll_for_cnv.set)
hscroll_for_cnv.config(command=main_cnv.xview)
vscroll_for_cnv.place(x=568, y=12, relheight=0.91)
hscroll_for_cnv.place(x=15, y=449, relwidth=0.635)


# Letter part
font_frame = tk.LabelFrame(window, text='Font')
font_frame.place(x=600, y=190)
size_of_font_entry = tk.Entry(font_frame, width=5)
size_of_font_entry.insert(tk.END, pix_to_mm(size_of_font))
size_of_font_entry.grid(row=0, column=1)
font_size_label = tk.Label(font_frame, text='Size of symbol:')
font_size_label.grid(row=0, column=0)
space_betwen_letters_label = tk.Label(font_frame, text='Space between symbols:')
space_betwen_letters_label.grid(row=2, column=0)
space_betwen_letters_entry = tk.Entry(font_frame, width=5)
space_betwen_letters_entry.insert(tk.END, str(pix_to_mm(space_betwen_letters)))
space_betwen_letters_entry.grid(row=2, column=1)
space_betwen_lines_label = tk.Label(font_frame, text='Space between lines:')
space_betwen_lines_label.grid(row=3, column=0)
space_betwen_lines_entry = tk.Entry(font_frame, width=5)
space_betwen_lines_entry.insert(tk.END, str(pix_to_mm(space_betwen_lines)))
space_betwen_lines_entry.grid(row=3, column=1)


# Mode part
def solid_mode():
    global letter_mode
    letter_mode = 'solid'


def dot_mode():
    global letter_mode
    letter_mode = 'dot'


def line_mode():
    global letter_mode
    letter_mode = 'line'


def n_mode():
    global dop_mode
    dop_mode = ''


def i_mode():
    global dop_mode
    dop_mode = 'i'


def b_mode():
    global dop_mode
    dop_mode = 'b'


mode_frame = tk.LabelFrame(window, text='Mode')
mode_frame.place(x=720, y=310)
var_mode = tk.IntVar()
var_mode.set(letter_mode)
rb_letter_mode_solid = tk.Radiobutton(mode_frame, text='Solid', variable=var_mode, value='solid', command=solid_mode)
rb_letter_mode_dot = tk.Radiobutton(mode_frame, text='Dot', variable=var_mode, value='dot', command=dot_mode)
rb_letter_mode_line = tk.Radiobutton(mode_frame, text='Line', variable=var_mode, value='line', command=line_mode)
rb_letter_mode_solid.grid(row=0, column=0)
rb_letter_mode_dot.grid(row=1, column=0)
rb_letter_mode_line.grid(row=2, column=0)

var_dop_mode = tk.IntVar()
var_dop_mode.set(4)
rb_letter_mode_normal = tk.Radiobutton(mode_frame, text='Normal', variable=var_dop_mode, value=4, command=n_mode)
rb_letter_mode_italic = tk.Radiobutton(mode_frame, text='Italic', variable=var_dop_mode, value=5, command=i_mode)
rb_letter_mode_bold = tk.Radiobutton(mode_frame, text='Bold', variable=var_dop_mode, value=6, command=b_mode)
rb_letter_mode_normal.grid(row=0, column=1)
rb_letter_mode_italic.grid(row=1, column=1)
rb_letter_mode_bold.grid(row=2, column=1)

# Size part
frame_cnv_size = tk.LabelFrame(window, text='Size of canvas')
frame_cnv_size.place(x=600, y=310)
width_cnv_label = tk.Label(frame_cnv_size, text='Width:')
height_cnv_label = tk.Label(frame_cnv_size, text='Height:')
width_cnv_entry = tk.Entry(frame_cnv_size, width=7)
width_cnv_entry.insert(tk.END, str(pix_to_mm(width_of_cnv)))
height_cnv_entry = tk.Entry(frame_cnv_size, width=7)
height_cnv_entry.insert(tk.END, str(pix_to_mm(height_of_cnv)))
width_cnv_label.grid(row=0, column=0)
height_cnv_label.grid(row=1, column=0)
width_cnv_entry.grid(row=0, column=1)
height_cnv_entry.grid(row=1, column=1)

#Bold part
scale_frame = tk.LabelFrame(window, text='Bolding')
scale_frame.place(x=600, y=385)
bold_scale = tk.Scale(scale_frame, from_=100, to=-100, orient=tk.HORIZONTAL)
bold_scale.set(bold)
bold_scale.pack()


def error_correct_data(dad_window):
    def closing():
        error_window.destroy()

    error_window = tk.Toplevel(dad_window)
    error_window.resizable(0, 0)
    error_label = tk.Label(error_window, text='Insert data correctly')
    error_label.pack()
    error_butt = tk.Button(error_window, text='Ok', command=closing)
    error_butt.pack()


def apply():
    global current_font, size_of_font, space_betwen_lines, space_betwen_letters
    try:
        if (float(size_of_font_entry.get()) >= 0 and float(space_betwen_lines_entry.get()) >= 0
          and float(space_betwen_letters_entry.get()) >= 0):
            size_of_font = mm_to_pixel(float(size_of_font_entry.get()))
            space_betwen_lines = mm_to_pixel(float(space_betwen_lines_entry.get()))
            space_betwen_letters = mm_to_pixel(float(space_betwen_letters_entry.get()))
        else:
            raise BaseException

        global width_of_cnv, height_of_cnv
        new_width = mm_to_pixel(float(width_cnv_entry.get()))
        new_height = mm_to_pixel(float(height_cnv_entry.get()))
        if new_width >= 0 and new_height >= 0:
            pass
        else:
            raise BaseException
        if width_of_cnv != new_width or height_of_cnv != new_height:
            width_of_cnv = new_width
            height_of_cnv = new_height

            global img_from_tk_cnv, photoimg_from_tk_cnv, img_from_tk_cnv_draw, main_cnv
            img_from_tk_cnv = Image.new('RGB', (width_of_cnv, height_of_cnv), 'white')
            photoimg_from_tk_cnv = ImageTk.PhotoImage(img_from_tk_cnv)
            img_from_tk_cnv_draw = ImageDraw.Draw(img_from_tk_cnv)
            main_cnv.create_image((0, 0), image=photoimg_from_tk_cnv, state='normal', anchor='nw')
            main_cnv.image = photoimg_from_tk_cnv

            if width_of_cnv > default_width_of_cnv or height_of_cnv > default_height_of_cnv:
                main_cnv.config(scrollregion=(0, 0, width_of_cnv, height_of_cnv))
                if width_of_cnv > default_width_of_cnv:
                    main_cnv.config(width=default_width_of_cnv)
                else:
                    main_cnv.config(width=width_of_cnv)
                if height_of_cnv > default_height_of_cnv:
                    main_cnv.config(height=default_height_of_cnv)
                else:
                    main_cnv.config(height=height_of_cnv)
            else:
                main_cnv.configure(width=width_of_cnv, height=height_of_cnv)
                main_cnv.config(scrollregion=(0, 0, width_of_cnv, height_of_cnv))

        global bold
        bold = int(bold_scale.get())
    except BaseException:
        error_correct_data(window)


change_font_butt = tk.Button(window, text='Apply', command=apply)
change_font_butt.place(x=750, y=420)
window.mainloop()
