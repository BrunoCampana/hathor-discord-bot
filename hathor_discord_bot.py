# This example requires the 'message_content' intent.

import discord
import re
import requests
from urllib import parse
import json

address_pattern = r'HTR\[(\w+)\]'
htr_reward = 1

wallet_id = '<your_test_wallet_id>'
wallet_seed_key = '<your_test_wallet_seed_key>'

wallet_base_url = 'http://localhost:8000'
full_node_base_url = 'https://node2.mainnet.hathor.network'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def response_to_json(response):
    return json.loads(json.dumps(response.json()))

# Inicia uma wallet na aplicação Hathor headless wallet
def start_wallet():
    url = parse.urljoin(wallet_base_url, '/start')
    response = requests.post(url, data={"seedKey": "<your_test_wallet_seed_key>", "wallet-id": "<your_test_wallet_id>"})
    print('Connecting to Wallet Headless:')
    print(response.json())

# Checa se o Discord bot já está com uma wallet pronta para emprego
def is_wallet_ready():
    print('Checking if wallet is ready')
    url = parse.urljoin(wallet_base_url, '/wallet/status')
    header = json.loads('{ "X-Wallet-Id" :"' + wallet_id + '"}')
    response = requests.get(url, headers=header)
    jsonResponse = response_to_json(response)
    print(jsonResponse)

    if 'network' in jsonResponse:
        print('Connected to wallet')
        return True
    else:
        print('Not Connected to wallet')
        return False

# Checa se o endereço provido nas mensagens no server do Discord é um address válido na Hathor Network
def is_valid_address(address):
    print('Checking if the address '+ str(address) + ' is valid')
    url = parse.urljoin(full_node_base_url, '/v1a/validate_address/' + str(address))
    response = requests.get(url)
    jsonResponse = response_to_json(response)
    print(jsonResponse)
    return jsonResponse['valid']

# Bot no Discord lê mensagens no server, e ao perceber que alguém no server está pedindo tokens HTR, tenta enviar alguns tokens para a pessoa
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('I need HTR'):

        if re.search(address_pattern, message.content):

            address = re.search(address_pattern, message.content).group()[4:-1]
            if is_valid_address(address):

                while not is_wallet_ready():
                    start_wallet()

                url = parse.urljoin(wallet_base_url, '/wallet/simple-send-tx')
                header = json.loads('{ "X-Wallet-Id" :"' + wallet_id + '"}')
                data = {
                    'address': address,
                    'value': htr_reward
                }
                response = requests.post(url, json=data, headers=header)
                jsonResponse = response_to_json(response)
                print(jsonResponse)
                if jsonResponse['success'] == True:
                    await message.channel.send(f'Hi, {message.author} I sent 0.01 HTR to you!')
                else:
                    await message.channel.send(f'Hi, {message.author} I cannot help you this time, sorry.')
                #Submit the payment request here!
            else:
                await message.channel.send(f'Hi, {message.author} the address you provided is not a valid HTR address.')

        else:
            await message.channel.send(f'Hi, {message.author} please give me a valid address and I will send HTR to you.')

client.run('<discord_bot_token>')
