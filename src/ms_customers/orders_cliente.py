import os
import grpc
import orders_pb2_grpc
from orders_pb2 import( 
    CustomerRequest
)

class OrdersClient():
    def __init__(self):
        self.host = os.getenv('SERVICE_HOST', 'localhost')
        self.port = os.getenv('SERVICE_PORT', 50050)

        self.channel = grpc.insecure_channel(
                        '{}:{}'.format(self.host, self.port))

        self.stub = orders_pb2_grpc.OrderServiceStub(self.channel)

    def getUserOrders(self, customer_id):
        req = CustomerRequest(customer_id=customer_id)
        return self.stub.GetCustomerInfo(req)