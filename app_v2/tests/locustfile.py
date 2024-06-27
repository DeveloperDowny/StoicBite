from locust import HttpUser, task, between

class DailyStoicUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_daily_stoic(self):
        self.client.get("/daily_stoic")

# Run with: locust -f locustfile.py