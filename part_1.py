from dataclasses import dataclass
import dataclasses
import struct
import random
import socket

random.seed(1)

TYPE_A = 1
CLASS_IN = 1

@dataclass
class DNSHeader:
    id: int
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int

def header_to_bytes(header):
    fields = dataclasses.astuple(header)
    return struct.pack("!HHHHHH", *fields)

def question_to_bytes(question):
    return question.name + struct.pack("!HH", question.type_, question.class_)

def encode_dns_name(domain_name):
    encoded = b""
    for part in domain_name.encode("ascii").split(b'.'):
        encoded += bytes([len(part)]) + part
    return encoded + b"\x00"

def build_query(domain_name, record_type):
    name = encode_dns_name(domain_name)
    id = random.randint(0, 65535)
    RECURSION_DESIRED = 1 << 8 # => 0b100000000
    header = DNSHeader(id=id, num_questions=1, flags=RECURSION_DESIRED)
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)
    return header_to_bytes(header) + question_to_bytes(question)

if __name__ == '__main__':

    query = build_query("www.example.com", 1)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(query, ("8.8.8.8", 53))

    response, _ = sock.recvfrom(1024)
