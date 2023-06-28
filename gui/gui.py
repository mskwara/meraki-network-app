from heavy_hitters_tab import init as init_heavy_hitters_tab
from latency_tab import init as init_latency_tab
from loss_tab import init as init_loss_tab
from bandwidth_usage_tab import init as init_bandwidth_usage_tab
from devices_network_usage_tab import init as init_devices_network_usage_tab
from vpn_tab import init as init_vpn_tab

import tkinter as tk
from tkinter import ttk

# Tworzenie głównego okna
root = tk.Tk()
root.title("Monitoring sieci")
root.geometry("1200x800")

# Tworzenie zakładek
tab_control = ttk.Notebook(root)
init_heavy_hitters_tab(tab_control)
init_latency_tab(tab_control)
init_loss_tab(tab_control)
init_bandwidth_usage_tab(tab_control)
init_devices_network_usage_tab(tab_control)
init_vpn_tab(tab_control)

# Dodanie zakładek do głównego okna
tab_control.pack(expand=1, fill="both")

# # Uruchomienie pętli zdarzeń
root.mainloop()
