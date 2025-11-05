# virtual_net.py, the virtual network thingy #
from queue import Queue
from typing import Dict, Tuple

class VirtualNIC:
    """Simulates a network interface using in-memory queues."""
    def __init__(self, name: str):
        self.name = name
        self.incoming = Queue()
        self.outgoing = Queue()

    def send(self, data: bytes):
        self.outgoing.put(data)

    def recv(self) -> bytes:
        if self.incoming.empty():
            return b""
        return self.incoming.get()

class IPStack:
    """Simple IPv4 layer with virtual routing."""
    def __init__(self, nic: VirtualNIC, ip_addr: str):
        self.nic = nic
        self.ip_addr = ip_addr
        self.routes: Dict[str, VirtualNIC] = {}

    def add_route(self, dest_ip: str, nic: VirtualNIC):
        self.routes[dest_ip] = nic

    def send_packet(self, dest_ip: str, payload: bytes):
        if dest_ip not in self.routes:
            print(f"No route to {dest_ip}")
            return
        frame = f"{self.ip_addr}->{dest_ip}:".encode() + payload
        self.routes[dest_ip].incoming.put(frame)

    def recv_packet(self) -> Tuple[str, bytes]:
        frame = self.nic.recv()
        if not frame:
            return "", b""
        header, payload = frame.split(b":", 1)
        src, dest = header.decode().split("->")
        return src, payload

class UDP:
    """Ultra-simple UDP layer on top of IPStack."""
    def __init__(self, ipstack: IPStack):
        self.ipstack = ipstack
        self.sockets: Dict[int, Queue] = {}

    def bind(self, port: int):
        self.sockets[port] = Queue()

    def sendto(self, dest_ip: str, port: int, data: bytes):
        # attach destination port in packet
        packet = f"{port}:".encode() + data
        self.ipstack.send_packet(dest_ip, packet)

    def recvfrom(self, port: int) -> Tuple[str, int, bytes]:
        """Return (src_ip, src_port, data) for given port."""
        if port not in self.sockets or self.sockets[port].empty():
            return "", 0, b""

        frame = self.sockets[port].get()
        # decode port from packet
        port_bytes, data = frame.split(b":", 1)
        return self.ipstack.ip_addr, int(port_bytes), data

# Example usage
if __name__ == "__main__":
    # create two virtual NICs
    nic1 = VirtualNIC("vnic0")
    nic2 = VirtualNIC("vnic1")

    # connect NICs (bi-directional)
    nic1.outgoing = nic2.incoming
    nic2.outgoing = nic1.incoming

    # IP stacks
    ip1 = IPStack(nic1, "192.168.0.1")
    ip2 = IPStack(nic2, "192.168.0.2")

    # routing
    ip1.add_route("192.168.0.2", nic2)
    ip2.add_route("192.168.0.1", nic1)

    # UDP layers
    udp1 = UDP(ip1)
    udp2 = UDP(ip2)

    udp1.bind(1234)
    udp2.bind(5678)

    # send a message
    udp1.sendto("192.168.0.2", 5678, b"Hello from Deuteric!")

    # simulate delivery to UDP socket
    # grab raw IP packet from NIC and push to correct UDP socket
    frame = ip2.recv_packet()[1]  # payload
    udp2.sockets[5678].put(frame)

    # receive properly from UDP layer
    src_ip, src_port, data = udp2.recvfrom(5678)
    print(f"Packet from {src_ip}:{src_port} -> {data}")
