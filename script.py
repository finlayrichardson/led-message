import asyncio
from bleak import BleakClient
from datetime import datetime
from time import sleep

MAC_ADDRESS = "84:C2:E4:AF:CC:D5"
WRITE_CHARACTERISTIC = "0000fee1-0000-1000-8000-00805f9b34fb"
PACKET_START = "77616E670000"

CHARS = {
    '0': "007CC6CEDEF6E6C6C67C00",
    '1': "0018387818181818187E00",
    '2': "007CC6060C183060C6FE00",
    '3': "007CC606063C0606C67C00",
    '4': "000C1C3C6CCCFE0C0C1E00",
    '5': "00FEC0C0FC060606C67C00",
    '6': "007CC6C0C0FCC6C6C67C00",
    '7': "00FEC6060C183030303000",
    '8': "007CC6C6C67CC6C6C67C00",
    '9': "007CC6C6C67E0606C67C00",
    '#': "006C6CFE6C6CFE6C6C0000",
    '&': "00386C6C3876DCCCCC7600",
    '_': "00000000000000000000FF",
    '-': "0000000000FE0000000000",
    '?': "007CC6C60C181800181800",
    '@': "00003C429DA5ADB6403C00",
    '(': "000C183030303030180C00",
    ')': "0030180C0C0C0C0C183000",
    '=': "0000007E00007E00000000",
    '+': "00000018187E1818000000",
    '!': "00183C3C3C181800181800",
    '\'': "1818081000000000000000",
    ':': "0000001818000018180000",
    '%': "006092966C106CD2920C00",
    '/': "000002060C183060C08000",
    '"': "6666222200000000000000",
    ' ': "0000000000000000000000",
    '*': "000000663CFF3C66000000",
    ',': "0000000000000030301020",
    '.': "0000000000000000303000",
    '$': "107CD6D6701CD6D67C1010",
    '~': "0076DC0000000000000000",
    '[': "003C303030303030303C00",
    ']': "003C0C0C0C0C0C0C0C3C00",
    '{': "000E181818701818180E00",
    '}': "00701818180E1818187000",
    '<': "00060C18306030180C0600",
    '>': "006030180C060C18306000",
    '^': "386CC60000000000000000",
    '`': "1818100800000000000000",
    ';': "0000001818000018180810",
    '\\': "0080C06030180C06020000",
    '|': "0018181818001818181800",
    'a': "00000000780C7CCCCC7600",
    'b': "00E060607C666666667C00",
    'c': "000000007CC6C0C0C67C00",
    'd': "001C0C0C7CCCCCCCCC7600",
    'e': "000000007CC6FEC0C67C00",
    'f': "001C363078303030307800",
    'g': "00000076CCCCCC7C0CCC78",
    'h': "00E060606C76666666E600",
    'i': "0018180038181818183C00",
    'j': "0C0C001C0C0C0C0CCCCC78",
    'k': "00E06060666C78786CE600",
    'l': "0038181818181818183C00",
    'm': "00000000ECFED6D6D6C600",
    'n': "00000000DC666666666600",
    'o': "000000007CC6C6C6C67C00",
    'p': "000000DC6666667C6060F0",
    'q': "0000007CCCCCCC7C0C0C1E",
    'r': "00000000DE76606060F000",
    's': "000000007CC6701CC67C00",
    't': "00103030FC303030341800",
    'u': "00000000CCCCCCCCCC7600",
    'v': "00000000C6C6C66C381000",
    'w': "00000000C6D6D6D6FE6C00",
    'x': "00000000C66C38386CC600",
    'y': "000000C6C6C6C67E060CF8",
    'z': "00000000FE8C183062FE00",
    'A': "00386CC6C6FEC6C6C6C600",
    'B': "00FC6666667C666666FC00",
    'C': "007CC6C6C0C0C0C6C67C00",
    'D': "00FC66666666666666FC00",
    'E': "00FE66626878686266FE00",
    'F': "00FE66626878686060F000",
    'G': "007CC6C6C0C0CEC6C67E00",
    'H': "00C6C6C6C6FEC6C6C6C600",
    'I': "003C181818181818183C00",
    'J': "001E0C0C0C0C0CCCCC7800",
    'K': "00E6666C6C786C6C66E600",
    'L': "00F060606060606266FE00",
    'M': "0082C6EEFED6C6C6C6C600",
    'N': "0086C6E6F6DECEC6C6C600",
    'O': "007CC6C6C6C6C6C6C67C00",
    'P': "00FC6666667C606060F000",
    'Q': "007CC6C6C6C6C6D6DE7C06",
    'R': "00FC6666667C6C6666E600",
    'S': "007CC6C660380CC6C67C00",
    'T': "007E7E5A18181818183C00",
    'U': "00C6C6C6C6C6C6C6C67C00",
    'V': "00C6C6C6C6C6C66C381000",
    'W': "00C6C6C6C6D6FEEEC68200",
    'X': "00C6C66C7C387C6CC6C600",
    'Y': "00666666663C1818183C00",
    'Z': "00FEC6860C183062C6FE00"
}


async def send_messages(messages):
    # Send header
    await client.write_gatt_char(WRITE_CHARACTERISTIC, bytes.fromhex(PACKET_START.ljust(32, '0')))
    # Send lengths
    lengths = ""
    for message in messages:
        lengths = lengths + str(hex(len(message))).lstrip('0x').rjust(4, '0')
    await client.write_gatt_char(WRITE_CHARACTERISTIC, bytes.fromhex(lengths.ljust(32, '0')))
    # Send timestamp
    time = datetime.now()
    timestamp = str(hex(time.year)).lstrip('0x').rjust(2, '0')[-2:] + str(hex(time.month)).lstrip('0x').rjust(2, '0')[-2:] + str(hex(time.day)).lstrip('0x').rjust(2, '0')[-2:] + str(
        hex(time.hour)).lstrip('0x').rjust(2, '0')[-2:] + str(hex(time.minute)).lstrip('0x').rjust(2, '0')[-2:] + str(hex(time.second)).lstrip('0x').rjust(2, '0')[-2:]  # maybe make better with map
    await client.write_gatt_char(WRITE_CHARACTERISTIC, bytes.fromhex("0" * 12 + timestamp + "0" * 8))
    # Send 0s
    await client.write_gatt_char(WRITE_CHARACTERISTIC, bytes.fromhex("0" * 32))
    # Send messages
    text = ""
    for message in messages:
        for letter in message:
            text = text + CHARS[letter]
    extra = len(text) % 32
    if extra > 0:
        text = text + ('0' * (32 - extra))
    text_packets = [text[i:i+32] for i in range(0, len(text), 32)]
    for text_packet in text_packets:
        await client.write_gatt_char(WRITE_CHARACTERISTIC, bytes.fromhex(text_packet))


async def main():
    global client
    client = BleakClient(MAC_ADDRESS)
    while True:
        try:
            if not client.is_connected():
                await client.connect()
            messages = [line.rstrip() for line in open(
                '/home/finners/led-message/messages.txt')]
            await send_messages(messages)
            sleep(5)
        except:
            sleep(5)

asyncio.run(main())
