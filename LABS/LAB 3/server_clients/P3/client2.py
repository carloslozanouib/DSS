import grpc
import greet_pb2
import greet_pb2_grpc

def greet_client(name):
    # Create a channel to the gRPC server (localhost:50051)
    channel = grpc.insecure_channel('localhost:50051')
    
    # Create a gRPC stub for the Greeter service
    stub = greet_pb2_grpc.GreeterStub(channel)

    while True:
        # Prompt the user to enter a message to send to Client 1
        message = input("Client 2, enter a message to send to Client 1: ")
        
        # Check if the user wants to exit the chat
        if message == "exit":
            break

        # Create a request with the message for Client 1
        request = greet_pb2.HelloRequest(name="Client 1", message=message)
        
        # Send the request to the server and receive a response
        response = stub.Greet(request)

        # Print the message sent to Client 1
        print(f"Sent to Client 1: {message}")
        
        # Print the response received from the server (Client 2 to Client 1)
        print(f"Response from server (Client 2 to Client 1): {response.message}")

if __name__ == "__main__":
    # Start the Client 2 application
    greet_client("Client 2")
