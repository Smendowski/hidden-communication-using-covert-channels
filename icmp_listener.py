#!/usr/bin/python
import socket
import struct

ICMP_PACKET = {
    "IP_HEADER_SIZE": 20,
    "ICMP_HEADER_SIZE": 8,
    "MAX_ICMP_PAYLOAD_SIZE": 1472
}


def get_dotted_decimal_ip_address(unicode_ip_address: bytes) -> str:
    return '.'.join(str(octet) for octet in struct.unpack('4B', unicode_ip_address))


def listen_on_icmp_socket(icmp_socket: socket.socket):
    while True:
        data = icmp_socket.recv(sum(ICMP_PACKET.values()))

        ip_header = data[:ICMP_PACKET["IP_HEADER_SIZE"]]
        source_ip = get_dotted_decimal_ip_address(unicode_ip_address=ip_header[-8:-4])
        destination_ip = get_dotted_decimal_ip_address(unicode_ip_address=ip_header[-4:])

        payload = data[ICMP_PACKET["IP_HEADER_SIZE"] + ICMP_PACKET["ICMP_HEADER_SIZE"]:]
        print(payload)


def get_data_from_icmp_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as icmp_socket:
        icmp_socket.bind(('', 1))
        try:
            listen_on_icmp_socket(icmp_socket=icmp_socket)
        except KeyboardInterrupt:
            raise SystemExit


if __name__ == '__main__':
    get_data_from_icmp_socket()
