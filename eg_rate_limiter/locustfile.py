# locustfile.py
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def home(self):
        self.client.get("/")

    @task(1)
    def limited_endpoint(self):
        self.client.get("/limited")