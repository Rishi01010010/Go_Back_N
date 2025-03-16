import time, socket, sys
import random

class GoBackNReceiver:
    def __init__(self):
        self.expected_seq_num = 0
        self.received_bits = []
        self.buffer = {}  # Buffer to store received packets
        
        # Packet statistics tracking
        self.total_packets_received = 0
        self.total_packets_lost = 0
        
    def receive_packet(self, packet_data):
        try:
            seq_num, data = packet_data.split(":", 1)
            seq_num = int(seq_num)
            
            if seq_num == self.expected_seq_num:
                print(f"\nReceived in-order packet {seq_num} with data: {data}")
                self.received_bits.append(data)
                self.total_packets_received += 1
                self.expected_seq_num += 1
                
                # Check buffer for consecutive packets
                while self.expected_seq_num in self.buffer:
                    self.received_bits.append(self.buffer[self.expected_seq_num])
                    del self.buffer[self.expected_seq_num]
                    self.total_packets_received += 1
                    self.expected_seq_num += 1
                    
                return f"ACK {seq_num}"
            else:
                print(f"\nReceived out-of-order packet {seq_num}, expected {self.expected_seq_num}")
                # Store out-of-order packet in buffer
                if seq_num > self.expected_seq_num:
                    self.buffer[seq_num] = data
                return f"ACK {self.expected_seq_num - 1}"
        except (ValueError, IndexError):
            return f"ACK {self.expected_seq_num - 1}"

print("\nWelcome to Chat Room")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(f"{shost} ({ip})\n")
host = input(str("Enter server address: "))
name = input(str("\nEnter your name: "))
port = 1234
print(f"\nTrying to connect to {host} ({port})\n")
time.sleep(1)
s.connect((host, port))
print("Connected...\n")

s.send(name.encode())
s_name = s.recv(1024)
s_name = s_name.decode()
print(f"{s_name} has joined the chat room\nYou will receive messages from {s_name}")

gbn_receiver = GoBackNReceiver()

while True:
    try:
        # Receive original message
        message = s.recv(1024)
        if not message:
            break
        message = message.decode()
        
        if message == "[e]":
            print(f"\n{s_name} left the chat room!")
            break
            
        print(f"\nReceiving message from {s_name}: {message}")
            
        # Receive number of bits
        total_bits = s.recv(1024)
        total_bits = int(total_bits.decode())
        print(f"Expected total bits: {total_bits}")
        
        # Reset receiver statistics
        gbn_receiver.expected_seq_num = 0
        gbn_receiver.received_bits = []
        gbn_receiver.buffer = {}
        gbn_receiver.total_packets_received = 0
        gbn_receiver.total_packets_lost = 0
        
        while len(gbn_receiver.received_bits) < total_bits:
            try:
                packet = s.recv(1024)
                if not packet:
                    break
                packet = packet.decode()
                
                # Simulate random packet loss
                if random.random() < 0.3:  # 30% chance of packet loss
                    print("\nPacket Lost!")
                    gbn_receiver.total_packets_lost += 1
                    s.send("ACK Lost".encode())
                    continue
                    
                ack = gbn_receiver.receive_packet(packet)
                print(f"Sending {ack}")
                s.send(ack.encode())
                
                # Print current received message status
                if gbn_receiver.received_bits:
                    received_bits = ''.join(gbn_receiver.received_bits)
                    if len(received_bits) >= 8:  # Make sure we have at least one complete byte
                        bytes_data = [received_bits[i:i+8] for i in range(0, len(received_bits), 8)]
                        current_message = ''.join(chr(int(byte, 2)) for byte in bytes_data if len(byte) == 8)
                        print(f"\nCurrent received message: {current_message}")
                
            except socket.error as e:
                print(f"Error receiving packet: {e}")
                break
        
        # Final message conversion and display
        if gbn_receiver.received_bits:
            received_bits = ''.join(gbn_receiver.received_bits)
            bytes_data = [received_bits[i:i+8] for i in range(0, len(received_bits), 8)]
            decoded_message = ''.join(chr(int(byte, 2)) for byte in bytes_data if len(byte) == 8)
            print(f"\nFinal Received message: {message}")
            print(f"Final Decoded message: {decoded_message}")
            
            # Print transmission statistics
            print("\nTRANSMISSION STATISTICS:")
            print(f"Total Packets Received: {gbn_receiver.total_packets_received}")
            print(f"Total Packets Lost: {gbn_receiver.total_packets_lost}")
        else:
            print("\nNo complete message received")
        
    except socket.error as e:
        print(f"\nConnection error: {e}")
        print(f"{s_name} has left the chat room!")
        break

s.close()