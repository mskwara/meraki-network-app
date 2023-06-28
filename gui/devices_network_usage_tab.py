from core.devices_network_usage import devices_network_usage
from utils import *


def init(parent):
    tab = ttk.Frame(parent)
    parent.add(tab, text="Ruch sieciowy urządzeń")

    entry_network_id = create_input(tab, "Adres sieci szkoły")
    entry_date = create_input(tab, "Data", 'calendar')
    entry_time = create_input(tab, "Godzina (HH:mm)")

    image_label = ttk.Label(tab)

    button_execute_heavy_hitters = ttk.Button(
        tab,
        text="Pokaż wykres",
        command=lambda: execute_on_click(entry_network_id, entry_date, entry_time, image_label),
        state="normal"
    )
    button_execute_heavy_hitters.pack()


def execute_on_click(entry_network_id, entry_date, entry_time, image_label):
    network_id, date, time = entry_network_id.get(), entry_date.get_date(), entry_time.get()
    datetime = f"{date}T{time}:00Z"
    plot_data = devices_network_usage(network_id, datetime)
    show_image(image_label, plot_data)
