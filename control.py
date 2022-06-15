# IMPORTS
import socket as so
from constants import *
from main import Server
from utils import logging
from utils.thread import Thread
from utils.crypt import rsa, aes


# CLASSES

# Control server
class Control(Thread):

    # CONSTRUCTOR
    def __init__(self, server: Server):

        # Initialize the thread
        Thread.__init__(self, server, name="Control Thread", daemon=True)

        # Define the logger
        self.logger = logging.Logger(self.server.lock, f"{NAME} - CONTROL", LOG_DEBUG if self.server.debug else LOG_INFO, self.server.log_file)

        # Load the ip
        self.logger.debug("Load ip ...")
        if not "ip" in self.server.control_config.data.keys():
            self.logger.warning("No IP found in configuration file! Get user input ...")
            while True:
                print("")
                print("Please type the IP for the control server:")
                print(f"[<String> (Default: {so.gethostbyname(so.gethostname())})]")
                self.ip = input("> ")
                if self.ip.strip() == "":
                    print("")
                    print("Invalid input! Empty input ...")
                    continue
                print("")
                self.server.control_config.data["ip"] = self.ip
                break
        else:
            self.ip = self.server.control_config.data["ip"]

        # Load the port
        self.logger.debug("Load port ...")
        if not "port" in self.server.control_config.data.keys():
            self.logger.warning("No port found in configuration file! Get user input ...")
            while True:
                print("")
                print("Please type the port for the control server:")
                print("[<Integer> (Default: 44445)]")
                port = input("> ")
                if port.strip() == "":
                    print("")
                    print("Invalid input! Empty input ...")
                    continue
                try:
                    self.port = int(port)
                except ValueError:
                    print("")
                    print("Invalid input! Cannot convert to integer ...")
                    continue
                print("")
                self.server.control_config.data["port"] = self.port
                break
        elif type(self.server.control_config.data["port"]) != int:
            self.logger.warning("Invalid port found in configuration file! Get user input ...")
            while True:
                print("")
                print("Please type the port for the control server:")
                print("[<Integer> (Default: 44445)]")
                port = input("> ")
                if port.strip() == "":
                    print("")
                    print("Invalid input! Empty input ...")
                    continue
                try:
                    self.port = int(port)
                except ValueError:
                    print("")
                    print("Invalid input! Cannot convert to integer ...")
                    continue
                print("")
                self.server.control_config.data["port"] = self.port
                break
        else:
            self.port = self.server.control_config.data["port"]

        # Define the socket
        self.logger.debug("Define socket ...")
        self.socket = so.socket(so.AF_INET, so.SOCK_STREAM)
        self.socket.settimeout(0.5)

        # Define started and exit variable
        self.started = False
        self.exit = False


    # METHODS

    # Main
    def main(self) -> None:

        # Bind the socket
        try:
            self.logger.debug("Bind the socket ...")
            self.socket.bind((self.ip, self.port))
            self.logger.debug("Socket successfully bound.")
        except (so.error, OverflowError):
            self.logger.error(f"The current IP ({self.ip}) or port ({self.port}) is not available or invalid!")
            self.logger.error("Please restart the server and specify another IP or port!")
            self.server.control_config.data.pop("port")
            self.server.control_config.data.pop("ip")
            self.server.exit = True
            self.started = True
            return

        # Log info
        self.logger.info("The control server is running on:")
        self.logger.info(f"IP: {self.ip}")
        self.logger.info(f"Port: {self.port}")

        # Set started to true
        self.started = True

        # Listen
        self.listen()

        # Close the socket
        self.socket.close()
        self.logger.debug("Closed socket.")

    # Listen
    def listen(self):

        # Log info
        self.logger.debug("Start listening for a client ...")
        self.socket.listen(1)

        # Listening loop
        while not self.exit:

            # Try to accept a client
            try:
                client, (ip, port) = self.socket.accept()
            except so.timeout:
                continue

            # Log info
            self.logger.info(f"New control client connection from {ip}:{port}! Initialize ...")

            # Send server information
            try:
                server_info = f"{NAME}-{VERSION}-{CONTROL_VER}" + " " * (128 - len(f"{NAME}-{VERSION}-{CONTROL_VER}"))
                client.send(server_info.encode("utf-8"))
            except so.error:
                self.logger.info(f"Server connection {ip}:{port} failed! Connection closed ...")
                client.close()
                continue

            # Receive client information
            try:
                client_info = client.recv(128).decode("utf-8")
                name, version, control_ver = client_info.strip().split("-")
            except (so.error, UnicodeDecodeError):
                self.logger.info(f"Client connection {ip}:{port} failed! Invalid response ...")
                client.close()
                continue

            # Check client information
            if name != "Shop Link Control":
                self.logger.info(f"Client connection {ip}:{port} failed! Invalid client ...")
                client.close()
                continue
            if control_ver != CONTROL_VER:
                self.logger.info(f"Client connection {ip}:{port} failed! Invalid version ...")
                client.close()
                continue

            # Send the server public rsa key
            try:
                client.send(rsa.export_key_to_bytes(self.server.public_key))
            except so.error:
                self.logger.info(f"Server connection {ip}:{port} failed! Connection closed ...")
                client.close()
                continue

            # Receive the client public rsa key
            try:
                client_key = rsa.import_key_from_bytes(client.recv(2048))
            except so.error:
                self.logger.info(f"Client connection {ip}:{port} failed! Invalid key ...")
                client.close()
                continue

            # Generate a new aes password
            password = aes.generate_password(30)

            # Send the aes password
            try:
                encrypted_password = rsa.encrypt_bytes(client_key, password.encode("utf-8"))
                client.send(str(len(encrypted_password)).zfill(8).encode("utf-8"))
                client.send(encrypted_password)
            except so.error:
                self.logger.info(f"Server connection {ip}:{port} failed! Connection closed ...")
                client.close()
                continue

            # Receive and check the aes password
            try:
                length = int(client.recv(8).decode("utf-8"))
                if rsa.decrypt_bytes(self.server.private_key, client.recv(length)).decode("utf-8") != password:
                    self.logger.info(f"Server connection {ip}:{port} failed! Cannot validate password ...")
                    client.close()
                    continue
            except so.error:
                self.logger.info(f"Server connection {ip}:{port} failed! Invalid password ...")
                client.close()
                continue

            # Start handling
            self.logger.info(f"Successfully connected with client {ip}:{port}! [CLIENT VERSION: {version}]")
            self.handle_client(aes.get_key(password), client, ip, port)

        # Log info
        self.logger.debug("Stopped listening for a client.")

    # Handle client
    def handle_client(self, key: bytes, socket: so.socket, ip: str, port: int):

        # Set the timeout
        socket.settimeout(0.5)

        socket.close()

    # STATIC METHODS

    # Send
    @staticmethod
    def send(key: bytes, socket: so.socket, data: bytes) -> bool:

        try:

            # Encrypt the data
            encrypted_data = aes.encrypt_bytes(key, data)

            # Send the header with the data size
            socket.send(str(len(encrypted_data)).zfill(16).encode("utf-8"))

            # Send the encrypted data
            socket.send(encrypted_data)

            # Return true
            return True

        except so.error:

            # Return false
            return False

    # Send message
    @staticmethod
    def send_msg(key: bytes, socket: so.socket, msg: str) -> bool:

        # Send the encoded message
        return Control.send(key, socket, msg.encode("utf-8"))

    # Receive
    @staticmethod
    def receive(key: bytes, socket: so.socket) -> bytes | None:

        try:

            # Receive the data size
            length = int(socket.recv(16).decode("utf-8"))

            # Receive the encrypted data
            encrypted_data = socket.recv(length)

            # Decrypt and return the data
            return aes.decrypt_bytes(key, encrypted_data)

        except (so.error, so.timeout):

            # Return none
            return None
