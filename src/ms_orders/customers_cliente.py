import os
import grpc
import customers_pb2_grpc
from customers_pb2 import( 
    CustomerRequest
)

class CustomerClient():
    def __init__(self):
        self.host = os.getenv('SERVICE_HOST', 'localhost')
        self.port = os.getenv('SERVICE_PORT', 50051)

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port))

        self.stub = customers_pb2_grpc.CustomerServiceStub(self.channel)

    def IsCustomer(self, customer_id):
        req = CustomerRequest(customer_id=customer_id)
        return self.stub.IsCustomer(req)