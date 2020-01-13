import os, sys
from locust import HttpLocust, TaskSet, task, events, runners, constant

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, '../..')))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, '../../..')))

from hooks.listeners import *


class JsonServerScenario(TaskSet):
    user_id = ' '

    def setup(self):
        print("Setup Data!")
        self.user_id = self.client.get("/users/1").json()['id']
        print("Got user with id: {}".format(self.user_id))

    def teardown(self):
        print("TearDown!!")

    @task
    def get_user(self):
        self.client.get("/users")

    @task
    def get_user(self):
        self.client.get("/users/{}".format(self.user_id))

    @task
    def get_user(self):
        self.client.get("/posts")

    @task
    def get_user(self):
        self.client.get("/posts/1")


###### Pass Fail Creteria listeners
events.request_success += response_time_listener
events.request_failure += on_error_listener
events.request_success += request_number_listener
events.request_success += timeout_listener
events.quitting += results_validation_listener

"""
Master and Slave listeners
"""
events.slave_report += on_slave_report_latency_handler
"""
Add this listeners to connect LoadTests with RPS listener
RPS listeners WORKING ONLY WITH ONE NODE and MASTER mode
"""
events.report_to_master += on_report_to_master
events.slave_report += on_slave_report


class LocustRunner(HttpLocust):
    host = "http://localhost:3000"
    task_set = JsonServerScenario
    wait_time = constant(1.0)

    """
    Generate stable 100 RPS count using wait_function
    """
    # wait_function = lambda self: self.fixed_rps_wait_function(100)
    # wait_function = lambda t: 900 if runners.global_stats.total.current_rps < 100 else 1100

    def __init__(self):
        super(LocustRunner, self).__init__()
        self.my_wait = 1000

    def fixed_rps_wait_function(self, desired_rps):
        # Will increase and decrease tasks wait time in range of 99.8 - 100.7 rps
        current_rps = runners.global_stats.total.current_rps
        if current_rps < desired_rps - 0.2:
            # the minimum wait is 10 ms
            if self.my_wait > 10:
                self.my_wait -= 4
        elif current_rps > desired_rps + 0.7:
            self.my_wait += 4
        # print("Current RPS: {}".format(current_rps))
        # print("Default wait is: {}".format(self.my_wait))
        return self.my_wait
