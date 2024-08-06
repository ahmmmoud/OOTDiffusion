import socket
import os

from run import model_runner

is_garment_received = False
processed = False

def start_server(host='localhost', port=19999):
    global is_garment_received
    global processed
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        model_path = "received_images/model.jpg"
        garment_path = "received_images/garment.jpg"
        try:
            # Receive image data from the client
            image_data = b""
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                image_data += chunk

            if is_garment_received:
                image_filename = garment_path
            else:
                image_filename = model_path

            with open(image_filename, "wb") as image_file:
                image_file.write(image_data)

            print(f"Received image and saved as {image_filename}")

            # selected_garment = 'examples/garment/ahmads/00055_00.jpg'
            if(is_garment_received):
                model_runner.run(model_path, garment_path)
                processed = True
                is_garment_received = False
            else:
                is_garment_received = True
        finally:
            # Close the client socket
            client_socket.close()
            if processed:
                send_image()
                processed = False


def send_image():
    file1 = "./captured_images/output.png"

    import socket

    # Read an image file as binary data
    image_filename = file1
    with open(image_filename, "rb") as image_file:
        image_data = image_file.read()

    # Setup client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 18888))  # Connect to server

    # Send the image data to the server
    client_socket.sendall(image_data)  # Use sendall to ensure all data is sent

    # Close the client socket
    client_socket.close()
    return True

if __name__ == "__main__":
    start_server()
