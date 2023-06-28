# szukamy po bandiwth okresu kiedy bylo duze obciazenie -> https://developer.cisco.com/meraki/api-latest/#!get-network-clients-bandwidth-usage-history
# wyciągamy rekord gdzie jest najwiekszy total i stąd mamy 20 minut z duzym obciążeniem
# robimy request organization devices z networkId danej szkoły -> https://developer.cisco.com/meraki/api-latest/#!get-organization-devices
# patrzymy po wszystkich urzadzeniach ktory ma najwiecej wyslanych pakietow -> https://developer.cisco.com/meraki/api-latest/#!get-device-clients
from core.utils import BASE_URL, send_request, get_script_param, create_column_plot


def get_bandwidth_url(network_id: str):
    return f"{BASE_URL}/api/v1/networks/{network_id}/clients/bandwidthUsageHistory"


def get_bandwidth_load(network_id: str, datetime: str):
    bandwidth_response = send_request(get_bandwidth_url(network_id), {"t0": datetime})
    timestamps = list(map(lambda x: x['ts'].split('T')[1][:5], bandwidth_response))
    bandwidth_usage = list(map(lambda x: x['total'], bandwidth_response))
    return timestamps, bandwidth_usage


def create_bandwidth_usage_chart(network_id, date):
    datetime = f"{date}T00:00:00.000Z"
    timestamps, bandwidth_usage = get_bandwidth_load(network_id, datetime)
    return create_column_plot(timestamps, bandwidth_usage, xlabel="Godzina", ylabel="Obciążenie [%]")


if __name__ == '__main__':
    network_id = get_script_param(1, "Enter network ID:")
    date = get_script_param(2, "Enter date (YYYY-MM-DD) :")
    create_bandwidth_usage_chart(network_id, date)
