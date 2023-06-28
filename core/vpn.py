import matplotlib.pyplot as plt

from core.conf import ORGANIZATION_ID
from core.utils import BASE_URL, send_request, create_column_plot
import io


def get_vpn_stats_url():
    return f"{BASE_URL}/api/v1/organizations/{ORGANIZATION_ID}/appliance/vpn/stats"


def get_summary_for_peer(peer: dict):
    return {
        "receivedInKilobytes": int(peer["usageSummary"]["receivedInKilobytes"]),
        "sendInKilobytes": int(peer["usageSummary"]["sentInKilobytes"])
    }


def sum_meraki_peers_send_receive(meraki_peers: list[dict]):
    received_total = []
    send_total = []
    for peer in meraki_peers:
        data_summary = get_summary_for_peer(peer)
        received_total += [data_summary["receivedInKilobytes"]]
        send_total += [data_summary["sendInKilobytes"]]

    return {
        "receivedInKilobytes": sum(received_total),
        "sendInKilobytes": sum(send_total)
    }


def get_vpn_response_all_networks():
    vpnResponse = send_request(get_vpn_stats_url())
    network_sums = [{
        "networkId": network["networkId"],
        "networkName": network["networkName"],
        "stats": sum_meraki_peers_send_receive(network["merakiVpnPeers"])
    } for network in vpnResponse]
    print(network_sums)


def get_vpn_response_singular_network(network: str = "L_595038100766333456"):
    vpnResponse = send_request(get_vpn_stats_url(), params={"networkIds[]": [network]})
    peers_sum = [{
        "peerId": network["networkId"],
        "peerName": network["networkName"],
        "stats": get_summary_for_peer(network)
    } for network in vpnResponse[0]['merakiVpnPeers']]
    return peers_sum


def create_vpn_plot(network_id):
    peers_stats = get_vpn_response_singular_network(network_id)
    stats = [(f"{stats['peerName']}\n{stats['peerId']}", stats['stats']['receivedInKilobytes'] + stats['stats']['sendInKilobytes']) for stats in peers_stats]
    sorted_usage = sorted(stats, key=lambda x: x[1], reverse=True)[:10]
    X, Y = zip(*sorted_usage)
    return create_column_plot(X, Y, show_gap=1)

