import matplotlib.pyplot as plt

from core.conf import ORGANIZATION_ID
from core.utils import BASE_URL, send_request
import io
from datetime import datetime


def get_devices_url():
    return f"{BASE_URL}/api/v1/organizations/{ORGANIZATION_ID}/devices"


def get_loss_latency_url(serial: str):
    return f"{BASE_URL}/api/v1/devices/{serial}/lossAndLatencyHistory"


def create_loss_plot(X: list, data):
    plt.figure(figsize=(20, 10))
    plt.xlabel("Day timespan")
    plt.ylabel("Package loss (%)")
    plt.title("Packets loss percentage for devices in your organisation")
    for record in data:
        plt.plot(X, record['lossPercent'], label=record['serial'])

    plt.legend()
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    image_data = io.BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)
    return image_data


def create_latency_plot(X: list, data):
    plt.figure(figsize=(20, 10))
    plt.xticks(rotation=30, ha='right')
    plt.xlabel("Day timespan")
    plt.ylabel("Delay/Jitter [ms]")
    plt.title("Delay and jittering of devices in your organisation")

    for record in data:
        plt.plot(X, record['latencyMs'], label=record['serial'] + '-latency')
        plt.plot(X, record['jitters'], label=record['serial'] + '-jitter')

    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    image_data = io.BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)
    return image_data


def get_devices_response():
    devicesResponse = send_request(get_devices_url())
    serials = list(map(lambda x: x['serial'], devicesResponse))
    return serials


def get_loss_latency_response(t0: str, t1: str, destination_ip: str, serials: list, limit: int):
    lossLatencyResponse = [{"serial": serial,
                            "lossLatency": send_request(get_loss_latency_url(serial), {
                                "t0": t0,
                                "t1": t1,
                                "ip": destination_ip})}
                           for serial in serials[:limit]]
    return list(filter(lambda x: x["lossLatency"] != [], lossLatencyResponse))


def create_timestamps(response: list[dict]):
    # Input time format: YYYY:DD:MM'T'HH:MM:SS'Z'
    raw_input_time = list(map(lambda x: x['startTs'].split("T"), response[0]['lossLatency']))
    processed_date_time = list(
        map(lambda x: (str(x[0]).split("-"), str(x[1][:len(x[1]) - 1]).split(":")), raw_input_time))
    timestamps = list(
        map(lambda datatime: datetime(int(datatime[0][0]), int(datatime[0][1]), int(datatime[0][2]),
                                      int(datatime[1][0]), int(datatime[1][1]),
                                      int(datatime[1][2])), processed_date_time))
    return timestamps


def get_loss(t0: str, t1: str, destination_ip: str = "0.0.0.0", devices_limit: int = 3):
    serials = get_devices_response()
    lossLatencyResponse = get_loss_latency_response(t0, t1, destination_ip, serials, devices_limit)

    loss_final = [{
        "serial": device['serial'],
        "lossPercent": list(map(lambda x: x['lossPercent'], device['lossLatency']))
    } for device in lossLatencyResponse]

    return create_loss_plot(create_timestamps(lossLatencyResponse), loss_final)


def get_latency(t0: str, t1: str, destination_ip: str = "0.0.0.0", devices_limit: int = 3):
    serials = get_devices_response()
    lossLatencyResponse = get_loss_latency_response(t0, t1, destination_ip, serials, devices_limit)

    loss_latency_final = [{
        "serial": device['serial'],
        "latencyMs": list(map(lambda x: x['latencyMs'], device['lossLatency'])),
        "jitters": list(map(lambda x: x['jitter'], device['lossLatency'])),
    } for device in lossLatencyResponse]

    return create_latency_plot(create_timestamps(lossLatencyResponse), loss_latency_final)

# destination_ip = get_script_param(1, "Enter destination IP (Format: X.X.X.X):")

# start_date = get_script_param(2, "Enter start date (YYYY-MM-DD) :")
# end_date = get_script_param(3, "Enter end date (YYYY-MM-DD) :")

# datetime_start = f"{start_date}T00:00:00.000Z"
# datetime_end = f"{end_date}T00:00:00.000Z" # 1 day long

# datetime_start = f"{start_date}T15:00:00.000Z"
# datetime_end = f"{end_date}T16:00:00.000Z"  # 1 hour long - Give same day as arg
#
# find_heavy_hitter(network_id, datetime)
# get_loss_latency(datetime_start, datetime_end, destination_ip)
