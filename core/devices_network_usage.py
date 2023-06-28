from core.utils import BASE_URL, get_script_param, send_request, create_column_plot, send_async_request, flatten
from core.conf import ORGANIZATION_ID
import asyncio

get_network_devices_url = f"{BASE_URL}/api/v1/organizations/{ORGANIZATION_ID}/devices"


def get_device_clients_url(serial: str):
    return f"{BASE_URL}/api/v1/devices/{serial}/clients"


async def get_clients_network_usage(serial: str, datetime: str):
    clients_response = await send_async_request(get_device_clients_url(serial), params={'t0': datetime})

    # lista (id, description, total usage)
    return list(map(
        lambda client:
        (client["ip"],
         client["description"],
         client["usage"]["sent"] + client["usage"]["recv"]
         ), clients_response))


def get_network_devices(network_id: str):
    network_devices_response = send_request(get_network_devices_url, params={'networkIds[]': network_id})
    return list(map(lambda entry: entry['serial'], network_devices_response))


def plot_clients_usage(clients_usage, datetime):
    X = list(map(lambda client: f"{client[0]} - {client[1] if client[1] else 'brak nazwy'}", clients_usage))
    Y = list(map(lambda client: client[2], clients_usage))
    return create_column_plot(X, Y, font_size=12, show_gap=1, title=datetime, xlabel="Użytkownicy",
                              ylabel="Ilość przesłanych pakietów")


async def get_all_clients_network_usages(devices_ids, datetime):
    tasks = [get_clients_network_usage(serial, datetime) for serial in devices_ids]

    # Oczekiwanie na zakończenie wszystkich zadań
    return await asyncio.gather(*tasks)


def devices_network_usage(network_id, datetime):
    devices_ids = get_network_devices(network_id)

    loop = asyncio.get_event_loop()
    clients_usage = flatten(loop.run_until_complete(get_all_clients_network_usages(devices_ids, datetime)))

    clients_usage = sorted(clients_usage, key=lambda x: x[2], reverse=True)[:10]
    return plot_clients_usage(clients_usage, datetime)


if __name__ == '__main__':
    network_id = get_script_param(1, "Enter network ID:")
    datetime = get_script_param(2, "Enter datetime (YYYY-MM-DDTHH:MM):")
    devices_network_usage(network_id, datetime)
