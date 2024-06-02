import grpc
import greet_pb2
import greet_pb2_grpc
import concurrent.futures

# Define a dictionary to track connected clients and their channels
client_channels = {}

class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def Greet(self, request, context):
        # Get the client's channel from the context
        client_channel = context.peer()
        
        if request.name not in client_channels:
            # If the client has not been registered previously, register their channel
            client_channels[request.name] = context
        else:
            # If the client is already registered, send the message to the destination client
            dest_channel = client_channels[request.name]
            dest_channel.send_initial_metadata()
            dest_channel.send_message(request)
            dest_channel.send_status_from_string('Message delivered')
            dest_channel.end(status_code=grpc.StatusCode.OK, details='')

        return greet_pb2.HelloResponse(message=f"Server: Message received for {request.name}")

def run_server():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    run_server()
