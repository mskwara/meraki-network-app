from core.bandwidth_usage import get_bandwidth_load
from core.devices_network_usage import devices_network_usage
from core.utils import get_script_param


def heavy_hitters_plot(network_id, date):
    datetime = f"{date}T00:00:00.000Z"
    timestamps, bandwidth_load = get_bandwidth_load(network_id, datetime)
    max_load = max(zip(timestamps, bandwidth_load), key=lambda entry: entry[1])
    max_load_datetime = f"{date}T{max_load[0]}:00.000Z"
    return devices_network_usage(network_id, max_load_datetime)


if __name__ == '__main__':
    network_id = get_script_param(1, "Enter network ID:")
    date = get_script_param(2, "Enter date (YYYY-MM-DD) :")
