import socket
import threading
from dnslib import DNSRecord, DNSHeader, DNSQuestion, RR, A, AAAA, CNAME, MX, NS, PTR, SRV, TXT, SOA, DNAME, QTYPE, RCODE
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

def DNSQuery(sock, data, addr, reply):
    """
    외부 DNS 서버로 요청을 전달하고 응답을 반환합니다.
    """
    qs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); qs.settimeout(1)

    for root in rootServers:
        try:
            qs.sendto(data, root)
            root_query = DNSRecord.parse(qs.recvfrom(512)[0])  # 요청 데이터 파싱
            #log.debug(root_query)
            def query(qu):
                if not qu.header.aa:
                    qs.sendto(DNSRecord.question(str(qu.q.qname), qtype=QTYPE[qu.q.qtype]).pack(), (str(qu.auth[0].rdata), 53))
                    res = DNSRecord.parse(qs.recvfrom(512)[0])
                    log.debug(res)
                    return query(res)
                else:
                    if QTYPE[qu.q.qtype] == "TXT": return [eval(str(d.rdata)) for d in qu.rr]
                    else: return [str(d.rdata) for d in qu.rr]
            return query(root_query)
        except Exception as e: log.error(f"{root} | {traceback.format_exc()}")

def DNS(sock):
    try:
        data, addr = sock.recvfrom(512)
        st = time.time()
        dns_query = DNSRecord.parse(data)  # 요청 데이터 파싱
        qname = str(dns_query.q.qname)  # 요청된 도메인 이름
        qtype = QTYPE[dns_query.q.qtype]  # 요청 타입 (A, AAAA 등)
        recordData = db.fetch("SELECT value FROM records WHERE domain = %s AND record = %s", [qname, qtype])
        if not recordData: aa = 0; recordData = DNSQuery(sock, data, addr, reply=None)
        else: aa = 1
        reply = DNSRecord(DNSHeader(id=dns_query.header.id, qr=1, aa=aa, ra=1), q=dns_query.q)

        if qtype == "A" and recordData:
            for r in recordData: reply.add_answer(RR(qname, QTYPE.A, ttl=60, rdata=A(r)))
        elif qtype == "AAAA" and recordData:
            for r in recordData: reply.add_answer(RR(qname, QTYPE.AAAA, ttl=60, rdata=AAAA(r)))
        elif qtype == "CNAME" and recordData:
            for r in recordData: reply.add_answer(RR(qname, QTYPE.CNAME, ttl=60, rdata=CNAME(r)))
        elif qtype == "MX" and recordData:
            for r in recordData: pr, t = r.split(" "); reply.add_answer(RR(qname, QTYPE.MX, ttl=60, rdata=MX(t, int(pr))))
        elif qtype == "NS" and recordData:
            for r in recordData: reply.add_answer(RR(qname, QTYPE.NS, ttl=60, rdata=NS(r)))
        elif qtype == "PTR" and recordData:
            for r in recordData: reply.add_answer(RR(qname, QTYPE.PTR, ttl=60, rdata=PTR(r)))
        elif qtype == "SRV" and recordData:
            for r in recordData: pr, w, p, t = r.split(" "); reply.add_answer(RR(qname, QTYPE.SRV, ttl=60, rdata=SRV(int(pr), int(w), int(p), t)))
        elif qtype == "TXT" and recordData:
            for r in recordData: reply.add_answer(RR(qname, QTYPE.TXT, ttl=60, rdata=TXT(r)))
        elif qtype == "SOA" and recordData:
            for r in recordData: s, u, t = r.split(" ", 2); t = [int(i) for i in t.split(" ")]; reply.add_answer(RR(qname, QTYPE.SOA, ttl=60, rdata=SOA(s, u, t)))
        #elif qtype == "DNAME" and recordData: pass
        elif not recordData: #정보 없을시 NXDOMAIN 설정하고 SOA 레코드 조회후 반환
            #try: sock.sendto(data, ("1.1.1.1", 53))
            #except: sock.sendto(data, ("2606:4700:4700::1111", 53))
            #s, u, t = str(DNSRecord.parse(sock.recvfrom(512)[0]).auth[0].rdata).split(" ", 2); t = [int(i) for i in t.split(" ")]
            reply = DNSRecord(DNSHeader(id=dns_query.header.id, qr=1, aa=aa, ra=1, rcode=RCODE.NXDOMAIN), q=dns_query.q)
            #reply.add_auth(RR(qname.split(".")[-2], QTYPE.SOA, ttl=60, rdata=SOA(s, u, t)))
        else: print(f"지원하지 않는 타입: {qtype}")

        sock.sendto(reply.pack(), addr) #클라이언트로 응답 전송
        log.info(f"{addr} | ({qtype}) {qname} --> {recordData} | {round((time.time() - st) * 1000, 2)}ms")
    except Exception as e: print(f"오류 발생: {traceback.format_exc()}")

if __name__ == "__main__":
    threading.Thread(target=IPv4).start()
    threading.Thread(target=IPv6).start()