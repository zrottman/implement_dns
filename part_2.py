from part_1 import build_query, DNSQuestion, DNSHeader
from dataclasses import dataclass
import struct
import socket
from  io import BytesIO
from typing import List


@dataclass
class DNSRecord:
    name: bytes     # domain name
    type_: int      # A, AAAA, MX, NS, TXT, etc
    class_: int     # 1
    ttl: int        # time to live
    data: bytes     # content of record, e.g. IP address

@dataclass
class DNSPacket:
    header: DNSHeader
    questions: List[DNSQuestion]
    answers: List[DNSRecord]
    authorities: List[DNSRecord]
    additionals: List[DNSRecord]

def parse_header(reader):
    items = struct.unpack("!HHHHHH", reader.read(12))
    return DNSHeader(*items)

def decode_name_simple(reader):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        parts.append(reader.read(length))
    return b".".join(parts)

def decode_name(reader):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        if length & 0b1100_0000:
            parts.append(decode_compressed_name(length, reader))
            break
        else:
            parts.append(reader.read(length))
    return b".".join(parts)

def decode_compressed_name(length, reader):
    pointer_bytes = bytes([length & 0b0011_1111]) + reader.read(1)
    pointer = struct.unpack("!H", pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result

def parse_question(reader):
    name = decode_name_simple(reader)
    data = reader.read(4)
    type_, class_ = struct.unpack("!HH", data)
    return DNSQuestion(name, type_, class_)

def parse_record(reader):
    name = decode_name(reader)
    # type, class, TTL, and data = 10 bytes
    data = reader.read(10)
    # HHIH => 2-byte int, 2-byte int, 4-byte int, 2-byte int
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
    data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)

def parse_dns_packet(data):
    reader = BytesIO(data) # data is our response
    header = parse_header(reader)
    questions = [parse_question(reader) for _ in range(header.num_questions)]
    answer = [parse_record(reader) for _ in range(header.num_answers)]
    authorities = [parse_record(reader) for _ in range(header.num_authorities)]
    additionals = [parse_record(reader) for _ in range(header.num_additionals)]

    return DNSPacket(header, questions, answer, authorities, additionals)

def ip_to_string(ip):
    return ".".join([str(x) for x in ip])

TYPE_A = 1

def lookup_domain(domain_name):
    query = build_query(domain_name, TYPE_A)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(query, ("8.8.8.8", 53))

    data, _ = sock.recvfrom(1024)
    response = parse_dns_packet(data)
    #return ip_to_string(response.answers[0].data)
    return response

if __name__ == '__main__':

    print(lookup_domain("example.com"))
    print(lookup_domain("recurse.com"))
    print(lookup_domain("metafilter.com"))
    print(lookup_domain("www.facebook.com"))
    print(lookup_domain("www.metafilter.com"))

