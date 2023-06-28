from utils import *
from core.heavy_hitters import heavy_hitters_plot


def init(parent):
    heavy_hitters_tab = ttk.Frame(parent)
    parent.add(heavy_hitters_tab, text="Heavy Hitters")

    entry_heavy_hitters_network_id = create_input(heavy_hitters_tab, "Adres sieci szkoły")
    entry_heavy_hitters_date = create_input(heavy_hitters_tab, "Data", 'calendar')

    image_label = ttk.Label(heavy_hitters_tab)

    button_execute_heavy_hitters = ttk.Button(
        heavy_hitters_tab,
        text="Pokaż wykres",
        command=lambda: execute_heavy_hitters(entry_heavy_hitters_date, entry_heavy_hitters_network_id, image_label),
        state="normal"
    )
    button_execute_heavy_hitters.pack()


def execute_heavy_hitters(entry_date, entry_network_id, image_label):
    date, network_id = entry_date.get_date(), entry_network_id.get()
    plot_data = heavy_hitters_plot(network_id, date)
    show_image(image_label, plot_data)
