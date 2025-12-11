import socket
import threading
from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, A, AAAA, CNAME, TXT, SRV, NS, SOA, PTR, DNAME, QTYPE, RCODE
import time
import traceback
from helpers import config
from helpers import logUtils as log
from helpers import dbConnect
#from helpers import drpc

db = dbConnect.db()

rootServers = [
    ("A.ROOT-SERVERS.NET", 53),
    ("B.ROOT-SERVERS.NET", 53),
    ("C.ROOT-SERVERS.NET", 53),
    ("D.ROOT-SERVERS.NET", 53),
    ("E.ROOT-SERVERS.NET", 53),
    ("F.ROOT-SERVERS.NET", 53),
    ("G.ROOT-SERVERS.NET", 53),
    ("H.ROOT-SERVERS.NET", 53),
    ("I.ROOT-SERVERS.NET", 53),
    ("J.ROOT-SERVERS.NET", 53),
    ("K.ROOT-SERVERS.NET", 53),
    ("L.ROOT-SERVERS.NET", 53),
    ("M.ROOT-SERVERS.NET", 53),
]
rootServers = [
    ("A.ROOT-SERVERS.NET", 53)
]

def IPv4(host='0.0.0.0', port=config.APP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); sock.bind((host, port))
    while True: DNS(sock)
def IPv6(host='::', port=config.APP_PORT):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
    sock.bind((host, port))
    while True: DNS(sock)
def DNS(sock):
    data, addr = sock.recvfrom(512)
    log.debug(data)
    log.info(data.decode())


    import struct
    # DNS 패킷을 해석하는 함수
    def parse_dns_packet(packet):
        # DNS 헤더 정보 (12바이트)
        transaction_id = struct.unpack('!H', packet[0:2])[0]
        flags = struct.unpack('!H', packet[2:4])[0]
        qd_count = struct.unpack('!H', packet[4:6])[0]
        an_count = struct.unpack('!H', packet[6:8])[0]
        ns_count = struct.unpack('!H', packet[8:10])[0]
        ar_count = struct.unpack('!H', packet[10:12])[0]

        print(f"Transaction ID: {transaction_id}")
        print(f"Flags: {flags:04x}")
        print(f"Question Count: {qd_count}")
        print(f"Answer Count: {an_count}")
        print(f"Authority Count: {ns_count}")
        print(f"Additional Count: {ar_count}")

        # 패킷의 질의 부분 해석
        offset = 12  # 헤더 길이
        for _ in range(qd_count):
            # QName (도메인 이름)
            qname, offset = parse_qname(packet, offset)
            qtype = struct.unpack('!H', packet[offset:offset+2])[0]
            qclass = struct.unpack('!H', packet[offset+2:offset+4])[0]
            offset += 4  # QType, QClass 크기만큼 이동

            print(f"QName: {qname}")
            print(f"QType: {qtype} (0x{qtype:04x})")
            print(f"QClass: {qclass} (0x{qclass:04x})")

    def parse_qname(packet, offset):
        qname = ''
        length = packet[offset]
        while length > 0:
            qname += packet[offset+1:offset+1+length].decode('utf-8') + '.'
            offset += length + 1
            length = packet[offset]
        return qname[:-1], offset + 1  # 마지막 '.' 제거
    
    parse_dns_packet(data)


if __name__ == "__main__":
    threading.Thread(target=IPv4).start()
    threading.Thread(target=IPv6).start()