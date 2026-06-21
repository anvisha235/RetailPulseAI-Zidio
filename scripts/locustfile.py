from locust import HttpUser, task, between

class RetailPulseUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_homepage(self):
        self.client.get("/")

    @task
    def load_health_check(self):
        self.client.get("/_stcore/health")

    @task
    def load_metrics(self):
        self.client.get("/_stcore/metrics")
