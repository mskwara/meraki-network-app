from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import DateEntry


def show_image(image_label, io, size_x=1100, size_y=550):
    image = Image.open(io)
    image = image.resize((size_x, size_y), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)

    image_label.configure(image=img)
    image_label.image = img
    image_label.pack()


def create_input(tab, input_label: str, entry_type: str = 'input'):
    label = ttk.Label(tab, text=input_label)
    label.pack()

    if entry_type == 'input':
        entry = ttk.Entry(tab)
    elif entry_type == 'calendar':
        entry = DateEntry(tab, width=20, background="black", foreground='white', borderwidth=2)

    entry.pack()

    return entry
