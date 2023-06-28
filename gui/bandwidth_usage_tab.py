from core.bandwidth_usage import create_bandwidth_usage_chart
from utils import *


def init(parent):
    bandwidth_usage_tab = ttk.Frame(parent)
    parent.add(bandwidth_usage_tab, text="Obciążenie")

    entry_network_id = create_input(bandwidth_usage_tab, "Adres sieci szkoły")
    entry_date = create_input(bandwidth_usage_tab, "Data", 'calendar')

    image_label = ttk.Label(bandwidth_usage_tab)

    button_execute_heavy_hitters = ttk.Button(
        bandwidth_usage_tab,
        text="Pokaż wykres",
        command=lambda: execute_on_click(entry_date, entry_network_id, image_label),
        state="normal"
    )
    button_execute_heavy_hitters.pack()


def execute_on_click(entry_date, entry_network_id, image_label):
    date, network_id = entry_date.get_date(), entry_network_id.get()
    plot_data = create_bandwidth_usage_chart(network_id, date)
    show_image(image_label, plot_data)
