import time, socket, sys
from typing import List
import threading

def create_packet(seq_num: int, data: str) -> dict:
    return {
        'seq_num': seq_num,
        'data': data,
        'timestamp': time.time()
    }

class GoBackNSender:
    def __init__(self):
        self.window_size = 0
        self.base = 0
        self.next_seq_num = 0
        self.packets = []
        self.timer = None
        self.timeout = 1.0  # 1 second timeout
        self.lock = threading.Lock()
        
        # Packet statistics tracking
        self.total_packets_sent = 0
        self.total_packets_lost = 0
        self.total_retransmissions = 0
        
    def start_timer(self):
        with self.lock:
            if self.timer is not None:
                self.timer.cancel()
            self.timer = threading.Timer(self.timeout, self.timeout_handler)
            self.timer.start()
            
    def stop_timer(self):
        with self.lock:
            if self.timer is not None:
                self.timer.cancel()
                self.timer = None
                
    def timeout_handler(self):
        print("\nTimeout occurred - Resending window")
        with self.lock:
            self.next_seq_num = self.base
            self.total_retransmissions += 1
            self.send_window()
            
    def send_window(self):
        while self.next_seq_num < min(self.base + self.window_size, len(self.packets)):
            packet = self.packets[self.next_seq_num]
            print(f"Sending packet {self.next_seq_num}: {packet['data']}")
            conn.send(f"{self.next_seq_num}:{packet['data']}".encode())
            self.total_packets_sent += 1
            if self.base == self.next_seq_num:
                self.start_timer()
            self.next_seq_num += 1
            time.sleep(0.1)

print("\nWelcome to Chat Room")
print("Initialising....\n")

s = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 1234
s.bind((host, port))
print(f"{host} ({ip})\n")
name = input("Enter your name: ")

s.listen(1)
print("\nWaiting for incoming connections...\n")
conn, addr = s.accept()
print(f"Received connection from {addr[0]} ({addr[1]})\n")

s_name = conn.recv(1024)
s_name = s_name.decode()
print(f"{s_name} has connected to the chat room\nEnter [e] to exit chat room\n")
conn.send(name.encode())

gbn = GoBackNSender()

while True:
    message = input(str("Me : "))
    if message == "[e]":
        conn.send(message.encode())
        print("\nLeaving chat room!")
        break
        
    # Reset statistics for new transmission
    gbn.total_packets_sent = 0
    gbn.total_packets_lost = 0
    gbn.total_retransmissions = 0
    
    # Convert message to packets
    message_bits = ''.join(format(ord(c), '08b') for c in message)
    conn.send(message.encode())  # Send original message
    conn.send(str(len(message_bits)).encode())  # Send total bits
    
    # Create packets
    gbn.packets = [create_packet(i, bit) for i, bit in enumerate(message_bits)]
    gbn.base = 0
    gbn.next_seq_num = 0
    gbn.window_size = int(input("Enter window size: "))
    
    # Start sending packets
    gbn.send_window()
    
    # Handle ACKs
    while gbn.base < len(gbn.packets):
        try:
            ack = conn.recv(1024).decode()
            if ack.startswith("ACK"):
                try:
                    ack_num = int(ack.split(" ")[1])
                    with gbn.lock:
                        gbn.base = ack_num + 1
                        if gbn.base == gbn.next_seq_num:
                            gbn.stop_timer()
                        else:
                            gbn.start_timer()
                        print(f"Window moved to {gbn.base}-{min(gbn.base + gbn.window_size, len(gbn.packets))}")
                        gbn.send_window()
                except (ValueError, IndexError):
                    print("Invalid ACK format")
            elif ack == "ACK Lost":
                print("ACK lost - waiting for timeout")
                gbn.total_packets_lost += 1
                # Timer will handle retransmission
        except socket.error:
            print("Error receiving ACK")
            break

    gbn.stop_timer()

    # Print transmission statistics
    print("\nTRANSMISSION STATISTICS:")
    print(f"Total Packets Sent: {gbn.total_packets_sent}")
    print(f"Total Packets Lost: {gbn.total_packets_lost}")
    print(f"Total Retransmissions: {gbn.total_retransmissions}")

conn.close()
s.close()