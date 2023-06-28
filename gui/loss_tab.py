from utils import *
from core.loss_latency import get_loss


def init(parent):
    tab_latency = ttk.Frame(parent)
    parent.add(tab_latency, text="Monitoring zgubionych pakietów")

    entry_ip = create_input(tab_latency, "Adres IP (X.Y.Z.W):")
    entry_start_date = create_input(tab_latency, "Data początku:", 'calendar')
    entry_end_date = create_input(tab_latency, "Data końca:", 'calendar')

    image_label = ttk.Label(tab_latency)

    button_execute_monitoring = ttk.Button(
        tab_latency,
        text="Pokaż wykres",
        command=lambda: execute_on_click(entry_start_date, entry_end_date, entry_ip, image_label),
        state="normal"
    )
    button_execute_monitoring.pack()


def execute_on_click(entry_start_date, entry_end_date, entry_ip, image_label):
    start_date, end_date, ip = entry_start_date.get_date(), entry_end_date.get_date(), entry_ip.get()
    plot_data = get_loss(f"{start_date}T00:00:00.000Z", f"{end_date}T00:00:00.000Z", ip)
    show_image(image_label, plot_data)
