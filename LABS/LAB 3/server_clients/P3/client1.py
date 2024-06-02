import grpc
import greet_pb2
import greet_pb2_grpc

def greet_client(name):
    # Create a channel to the gRPC server (localhost:50051)
    channel = grpc.insecure_channel('localhost:50051')
    
    # Create a gRPC stub for the Greeter service
    stub = greet_pb2_grpc.GreeterStub(channel)

    while True:
        # Prompt the user to enter a message to send to Client 2
        message = input("Client 1, enter a message to send to Client 2: ")
        
        # Check if the user wants to exit the chat
        if message == "exit":
            break

        # Create a request with the message for Client 2
        request = greet_pb2.HelloRequest(name="Client 2", message=message)
        
        # Send the request to the server and receive a response
        response = stub.Greet(request)

        # Print the message sent to Client 2
        print(f"Sent to Client 2: {message}")
        
        # Print the response received from the server (Client 1 to Client 2)
        print(f"Response from server (Client 1 to Client 2): {response.message}")

if __name__ == "__main__":
    # Start the Client 1 application
    greet_client("Client 1")
