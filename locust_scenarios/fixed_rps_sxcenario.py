from locust_fixed_interval import FixedIntervalTaskSet
from locust import HttpLocust, Locust, TaskSet, task, between, constant, constant_pacing


class JsonServerScenario(TaskSet):

    @task
    def get_user(self):
        self.client.get("/users")

    @task
    def get_user(self):
        self.client.get("/users/1")

    @task
    def get_user(self):
        self.client.get("/posts")

    @task
    def get_user(self):
        self.client.get("/posts/1")


class LocustRunner(HttpLocust):
    host = "http://localhost:3000"
    task_set = JsonServerScenario
    # wait_time = constant(1.0)
    wait_time = constant_pacing(1.0)