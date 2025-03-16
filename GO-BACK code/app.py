from flask import Flask, request, jsonify, send_from_directory
import random

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    message = data['message']
    window_size = data['windowSize']
    
    sender_logs = []
    receiver_logs = []
    
    # Tracking statistics
    total_packets_sent = 0
    total_packets_lost = 0
    total_retransmissions = 0

    base = 0
    next_seq_num = 0
    total_packets = len(message)
    retransmission_needed = False

    def simulate_loss():
        return random.random() < 0.2  # Simulate 20% packet loss

    while base < total_packets:
        # Sending packets within the window size
        while next_seq_num < base + window_size and next_seq_num < total_packets:
            sender_logs.append(f"Sending packet {next_seq_num}: {message[next_seq_num]}")
            total_packets_sent += 1
            next_seq_num += 1

        # Acknowledgment loop for received packets
        for seq in range(base, next_seq_num):
            if simulate_loss():
                sender_logs.append(f"Packet {seq} lost!")
                receiver_logs.append(f"Packet {seq} not received!")
                total_packets_lost += 1
                retransmission_needed = True
                break
            else:
                sender_logs.append(f"Packet {seq} acknowledged.")
                receiver_logs.append(f"Received packet {seq}: {message[seq]}")
                base = seq + 1

        # If packet was lost, prepare for retransmission
        if retransmission_needed:
            total_retransmissions += 1
            sender_logs.append(f"Retransmitting window starting from packet {base}")
            retransmission_needed = False
            next_seq_num = base

    # Add statistics to logs
    sender_logs.append(f"TRANSMISSION STATISTICS:")
    sender_logs.append(f"Total Packets Sent: {total_packets_sent}")
    sender_logs.append(f"Total Packets Lost: {total_packets_lost}")
    sender_logs.append(f"Total Retransmissions: {total_retransmissions}")

    # Add success message for the sender
    sender_logs.append("All packets sent successfully!")

    # Add full received message for the receiver
    receiver_logs.append(f"RECEIVED MESSAGE: {''.join(message)}")
    receiver_logs.append(f"TRANSMISSION STATISTICS:")
    receiver_logs.append(f"Total Packets Received: {total_packets_sent - total_packets_lost}")
    receiver_logs.append(f"Total Packets Lost: {total_packets_lost}")

    return jsonify({'senderLogs': sender_logs, 'receiverLogs': receiver_logs})

if __name__ == '__main__':
    app.run(debug=True)