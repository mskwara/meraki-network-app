from core.vpn import create_vpn_plot
from utils import *


def init(parent):
    vpn_tab = ttk.Frame(parent)
    parent.add(vpn_tab, text="Statystyki VPN")

    entry_network_id = create_input(vpn_tab, "Adres sieci szkoły")

    image_label = ttk.Label(vpn_tab)

    button_execute_heavy_hitters = ttk.Button(
        vpn_tab,
        text="Pokaż wykres",
        command=lambda: execute_on_click(entry_network_id, image_label),
        state="normal"
    )
    button_execute_heavy_hitters.pack()


def execute_on_click(entry_network_id, image_label):
    network_id = entry_network_id.get()
    plot_data = create_vpn_plot(network_id)
    show_image(image_label, plot_data)
