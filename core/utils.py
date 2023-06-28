import sys
import requests
import aiohttp
from matplotlib import pyplot as plt
from core.conf import API_KEY
import io


def get_script_param(param_id: int, param_message: str):
    if param_id < len(sys.argv):
        param = sys.argv[param_id]
    else:
        param = input(param_message)
    return param


BASE_URL = "https://api.meraki.com"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": API_KEY
}


def send_request(url: str, params: dict = {}):
    # print(f"Sending: {url} with {params}")
    r = requests.get(url=url, params=params, headers=HEADERS)
    return r.json()


async def send_async_request(url, params: dict = {}):
    # print(f"Sending: {url} with {params}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, params=params) as response:
            data = await response.json()
            return data


def create_column_plot(X, Y, font_size=16, show_gap=3, title='', xlabel='', ylabel=''):
    if len(X) != len(Y):
        raise ValueError("Listy X i Y muszą mieć taką samą długość.")

    indexes = range(len(X))
    plt.figure(figsize=(20, 10))
    plt.bar(indexes, Y)
    plt.xticks(indexes[::show_gap], X[::show_gap], rotation=45, ha='center', fontsize=font_size)
    plt.tight_layout(pad=4)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    image_data = io.BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)
    return image_data


def flatten(l):
    return [item for sublist in l for item in sublist]
