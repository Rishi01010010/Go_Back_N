# 🌐 Go-Back-N ARQ Simulation: Reliable Data Transfer 🌐

Welcome to the *Go-Back-N ARQ Simulation*, a project developed by students at SAI Vidya Institute of Technology (SVIT), Bengaluru, under the guidance of Dr. Tejashwini N. Submitted as part of the Computer Networks course (2023-24) at the Department of Computer Science and Engineering, this project simulates the Go-Back-N Automatic Repeat Request (ARQ) protocol. It demonstrates reliable data transfer over unreliable networks by handling packet loss, retransmissions, and acknowledgments, with a web-based interface for visualization.

## 🔍 Project Overview

In communication networks, ensuring reliable data transfer over noisy or unreliable channels is a significant challenge. The *Go-Back-N ARQ* protocol addresses this by using a sliding window mechanism to send multiple frames without waiting for individual acknowledgments, retransmitting unacknowledged frames upon detecting errors or packet loss. This project simulates the protocol using Python, introducing random packet loss to mimic real-world conditions, and visualizes the process through a Flask-based web application.

### ✨ Key Features:

- *Protocol Simulation:* Implements Go-Back-N ARQ with sender and receiver logic.
- *Packet Loss Simulation:* Randomly drops packets to test reliability.
- *Retransmission Handling:* Retransmits unacknowledged frames to ensure data integrity.
- *Web Visualization:* Displays transmission statistics (packets sent, retransmissions) using HTML, JavaScript, and D3.js.
- *Educational Tool:* Provides a hands-on approach to understanding ARQ protocols in networking.

## 🚀 Getting Started

### 1. *Prerequisites:*
- **Operating System:** Windows.
- **Python 3.7** installed.
- **Python Libraries:**
  - `flask` (for the web server)
  - `socket` (for network communication)
  - `time` (for delays and timestamps)
  - `random` (for simulating packet loss)
- **Code Editor:** Visual Studio Code (recommended).
- **Hardware:** Dual-core processor (i3 or equivalent), 4 GB RAM (8 GB recommended), 50 MB storage, and a network connection (LAN/Wi-Fi).

### 2. *Setting Up:*

- Clone the repository (if hosted on GitHub):
  ```bash
  git clone https://github.com/your-username/GoBackN_ARQ_Simulation.git
  cd GoBackN_ARQ_Simulation
  ```

- Install Python dependencies:
  ```bash
  pip install flask
  ```

- Ensure Python 3.7 is set as the default Python version.

### 3. *Running the System:*

- Start the Flask server:
  ```bash
  python app.py
  ```

- Open a web browser and navigate to `http://localhost:5000` to access the simulation interface.
- Input a message and window size, then observe the simulation of packet transmission, including packet loss, retransmissions, and acknowledgments.
- View real-time statistics (e.g., packets transmitted, retransmissions) visualized on the webpage.

### 4. *Sample Output:*
- **Transmission Statistics (from Web Interface):**
  ```
  Packets Transmitted: 7
  Retransmissions: 1
  ```
- **Sender Logs:**
  ```
  Packet #1 sent to receiver
  Packet Lost
  Retransmitting window...
  ACK Received
  All Packets Sent
  ```

## 💾 Directory Structure

```
GoBackN_ARQ_Simulation/
│
├── app.py               # Main Flask application for the web server
├── receiver.py          # Receiver-side logic for Go-Back-N ARQ
├── sender.py            # Sender-side logic for Go-Back-N ARQ
│
└── static/              # Frontend assets
    └── index.html       # Web interface for simulation and visualization
```

### 📝 Code Explanation

1. **app.py**:
   - Sets up the Flask server to handle HTTP requests.
   - Coordinates communication between `sender.py` and `receiver.py`.
   - Serves the web interface (`index.html`) and provides JSON data for visualization.

2. **sender.py**:
   - Implements the sender-side logic of Go-Back-N ARQ.
   - Manages the sliding window, transmits packets, simulates packet loss, and handles retransmissions based on acknowledgments.

3. **receiver.py**:
   - Implements the receiver-side logic, waiting for packets and sending acknowledgments.
   - Processes received data and logs packet receipt.

4. **static/index.html**:
   - Provides a web interface for user input (message, window size).
   - Uses JavaScript and D3.js to visualize packet transmission, acknowledgments, and statistics.

## 🌐 System Design

- **Architecture:**
  - **Frontend:** HTML, CSS, JavaScript, and D3.js for visualization.
  - **Backend:** Flask server to simulate ARQ logic and calculate statistics.
  - **Communication:** AJAX (JSON) for data exchange between frontend and backend.
- **Sender Workflow:**
  - Inputs message and window size.
  - Transmits packets in the window.
  - Simulates packet loss and retransmits if necessary.
  - Logs acknowledgments and completes transmission.
- **Receiver Workflow:**
  - Waits for packets from the sender.
  - Processes received packets and sends acknowledgments.

## 🛠️ How It Works

1. *User Input:* Enter a message and window size via the web interface.
2. *Simulation Start:* The Flask server triggers the sender to transmit packets bit by bit.
3. *Packet Loss:* Random packet loss is simulated using Python’s `random` library.
4. *Retransmission:* The sender retransmits unacknowledged packets upon detecting loss.
5. *Visualization:* The frontend displays real-time logs and statistics (e.g., packets sent, retransmissions).

## 🎯 Project Intent

The *Go-Back-N ARQ Simulation* aims to provide an educational tool for understanding the Go-Back-N ARQ protocol. By simulating real-world network issues like packet loss, it demonstrates the importance of error-handling mechanisms in ensuring reliable data transfer, making it a valuable learning resource for computer networks students.

## 🔧 Future Enhancements

- *Error Detection and Correction:* Add mechanisms to detect and correct errors in transmitted data.
- *Quality of Service (QoS) Management:* Implement QoS features to prioritize traffic and manage latency.
- *Advanced Visualization:* Enhance the frontend with more detailed graphs (e.g., packet loss rate over time).
- *Real Network Integration:* Extend the simulation to work over actual network connections.

## 📌 References

- "Energy Efficiency of ARQ Protocols in IoT Networks" (2023)
- "ARQ Schemes for 6G Communication Systems" (2024)
- "Reinforcement Learning for Adaptive ARQ" (2023)
- "Improving Go-Back-N ARQ in Vehicular Networks" (2024)
- "Error Correction and ARQ for Quantum Communication" (2023)
- "Comparison of ARQ Protocols and Buffering Strategies" (2024)
