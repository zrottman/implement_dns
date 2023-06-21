from part_1 import build_query, DNSQuestion, DNSHeader
from dataclasses import dataclass
import struct

@dataclass
class DNSRecord:
    name: bytes     # domain name
    type_: int      # A, AAAA, MX, NS, TXT, etc
    class_: int     # 1
    ttl: int        # time to live
    data: bytes     # content of record, e.g. IP address

def parse_header(reader):
    items = struct.unpack("!HHHHHH", reader.read(12))
    return DNSHeader(*items)

def decode_name_simple(reader):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        parts.append(reader.read(length))
    return b".".join(parts)

def parse_question(reader):
    name = decode_name_simple(reader)
    data = reader.read(4)
    type_, class_ = struct.unpack("!HH", data)
    return DNSQuestion(name, type_, class_)

def parse_record(reader):
    name = decode_name_simple(reader)
    # type, class, TTL, and data = 10 bytes
    data = reader.read(10)
    # HHIH => 2-byte int, 2-byte int, 4-byte int, 2-byte int
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
    data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)
