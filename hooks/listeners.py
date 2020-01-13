from statistics import median
import locust, os, sys, time
from locust import runners, events


"""
================================================
**** Listeners for LOCUST REQUESTS ****
================================================
"""

def response_time_listener(request_type, name, response_time, response_length, **kw):
    if os.environ.get('MAX_LATENCY') is not None:
        # print("Successfully fetched: %s" % (name))
        max_latency = os.environ.get('MAX_LATENCY', 'MAX_LATENCY variable is not set!')
        if response_time > float(max_latency):
            error_message = "Request Failed! Response time is > than {} ms.".format(max_latency)
            runners.logger.error(error_message)
            # events.locust_error.fire(locust_instance="response_time_listener", exception=error_message, tb=None)
            events.request_failure.fire(request_type="response_listener", name=name, response_time=response_time,
                                        exception=error_message)
            # Exit and stop locust
            # runners.locust_runner.stop()
            # runners.locust_runner.quit()
            # sys.exit(1)
        # print("Stats: \n {}".format(runners.global_stats.__dict__))
        # print("Start Time: \n {}".format(runners.global_stats.start_time))
        # print("Total Request Number: \n {}".format(runners.global_stats.total.num_requests))


def request_number_listener(request_type, name, response_time, response_length, **kw):
    if os.environ.get("MAX_REQUESTS") is not None:
        max_requests = os.environ.get("MAX_REQUESTS")
        total_reqs = locust.runners.global_stats.total.num_requests
        # print("Successfully fetched: %s" % (name))
        if total_reqs > int(max_requests):
            error_message = "Stopping Requests! \n The Requests Number is: {}. \n Stopping!".format(total_reqs)
            runners.logger.info(error_message)
            runners.locust_runner.stop()
            runners.locust_runner.quit()


def on_error_listener(request_type, name, response_time, exception, **kw):
    print("Got Exception: %s" % (exception))
    errors_count = runners.global_stats.num_failures
    events.locust_error.fire(locust_instance="error_listener", exception=exception, tb=None)
    if os.environ.get('MAX_ERRORS') is not None:
        if int(errors_count) == int(os.environ.get('MAX_ERRORS')):
            error_message = "STOPPING TESTS!!! ERROR FOUND: {}".format(exception)
            runners.logger.error(error_message)
            events.locust_error.fire(locust_instance="error_listener", exception=error_message, tb=None)
            runners.logger.error("Shutting down Locust. Actual error number is: {}".format(errors_count))
            runners.locust_runner.stop()
            runners.locust_runner.quit()
            raise Exception(error_message)
            # sys.exit(1)


def timeout_listener(request_type, name, response_time, response_length, **kw):
    if os.environ.get("LOAD_TEST_TIMEOUT") is not None:
        timeout_sces = os.environ.get("LOAD_TEST_TIMEOUT")
        # print("No variable LOAD_TEST_TIMEOUT is set.")
        import time
        start_time = runners.global_stats.total.start_time
        total_time = round(time.time() - start_time)
        time_seconds = total_time % 60
        if time_seconds == int(timeout_sces):
            print("Timeout. Stopping Load Tests!!! LOAD_TEST_TIMEOUT={} secs.".format(timeout_sces))
            runners.locust_runner.stop()
            runners.locust_runner.quit()


# Validates test results on even "quit"
# when tests are quiting
def results_validation_listener():
    if os.environ.get('MAX_LATENCY') is not None:
        max_latency = os.environ.get('MAX_LATENCY', 'MAX_LATENCY variable is not set!')
        error_count = runners.global_stats.num_failures
        percentile_latancey = runners.global_stats.total.get_response_time_percentile(95)

        print("Overall 95% latency: {}".format(runners.global_stats.total.get_response_time_percentile(95)))
        if percentile_latancey is not None:
            if percentile_latancey > float(max_latency) or error_count >= 1:
                error_message = ("BUILD FAILED WITH CONDITIONS:"
                                 "\nExpected max latency: {} ms. Actual: {}ms"
                                 "\nExpected number of errors: 0, Found: {}".format(max_latency, percentile_latancey,
                                                                                    error_count))
                runners.logger.error(error_message)
                events.locust_error.fire(locust_instance="error_listener", exception=error_message, tb=None)
                runners.logger.error("BUILD FAILED.")
                # sys.exit(1)
                runners.locust_runner.stop()
                runners.locust_runner.quit()
                raise Exception(error_message)
            else:
                runners.logger.info("BUILD PASSED.")


"""
================================================
**** Listeners for LOCUST CLUSTER ****
================================================
"""


# Validates test results on event "slave_report"
# when report comes to the master
def on_slave_report_latency_handler(client_id, data, **kw):
    if os.environ.get("MAX_LATENCY") is not None:
        max_latency = os.environ.get('MAX_LATENCY', 'MAX_LATENCY variable is not set!')
        if data.get('stats_total').get('num_requests') > 0:
            error_count = runners.global_stats.num_failures
            percentile_latancey = runners.global_stats.total.get_response_time_percentile(95)

            print("Overall 95% latency: {}".format(runners.global_stats.total.get_response_time_percentile(95)))
            if percentile_latancey is not None:
                if percentile_latancey > float(max_latency) or error_count >= 1:
                    error_message = ("BUILD FAILED WITH CONDITIONS:"
                                     "\nExpected max latency: {} ms. Actual: {}ms"
                                     "\nExpected number of errors: 0, Found: {}".format(max_latency,
                                                                                        percentile_latancey,
                                                                                        error_count))
                    runners.logger.error(error_message)
                    events.locust_error.fire(locust_instance="LoadTest.class", exception=error_message, tb=None)
                    runners.logger.error("BUILD FAILED.")
                    # sys.exit(1)
                    runners.locust_runner.stop()
                    runners.locust_runner.quit()
                    raise Exception(error_message)
                else:
                    runners.logger.info("CONDITION 'MAX_LATENCY' - PASSED.")


##### Every slave will spin up 2 users
####### The users count and desire_rps should be counted according to the slaves number
def on_report_to_master(client_id, data, **kw):
    if os.environ.get('TARGET_RPS') is not None:
        target_rps = os.environ.get('TARGET_RPS', 'TARGET_RPS variable is not set!')
        nodes = os.environ.get('SLAVES_COUNT', 'Add SLAVES_NUMBER variable according to integrate TARGET_RPS.')

        if data.get('stats_total').get('num_requests') > 0:
            # Executes before on_slave_report
            # Validate data statistics on slave
            clients_number = runners.locust_runner.num_clients
            hatch_rate = runners.locust_runner.hatch_rate
            print("Clients number: {}".format(clients_number))
            rps_mid = data['stats_total']['num_reqs_per_sec'].values()
            if len(rps_mid) >= 2:
                rpss = list(rps_mid)
                rpss.sort()
                med_rps = sum(rpss) / len(rpss)  # sum([rpss[-1], rpss[-2]])/2
                print("Max RPS {}".format(max(rpss)))
                print("Med RPS {}".format(med_rps))
                print("Desired RPS: {}".format(int(target_rps) / int(nodes)))
                # print("Mid {}".format(median(rpss)))
                # the calculation is provided by max rps count
                if med_rps < int(target_rps) / int(nodes):
                    clients_number += 1
                    runners.locust_runner.start_hatching(clients_number, hatch_rate)
                    events.hatch_complete.fire(user_count=clients_number)
                if med_rps >= int(target_rps) / int(nodes) + 0.5:
                    clients_number -= 1
                    runners.locust_runner.start_hatching(clients_number, hatch_rate)
                    events.hatch_complete.fire(user_count=clients_number)


def on_slave_report(client_id, data, **kw):
    if os.environ.get('TARGET_RPS') is not None:
        # Executes after on_report_to_master
        # Print data statistics on master
        if data.get('stats_total').get('num_requests') > 0:
            rps_number = runners.global_stats.total.current_rps
            clients_number = runners.locust_runner.num_clients
            # print("Users number: {}".format(data['user_count']))
            print("Total Users: {}".format(data['user_count'] * len(runners.locust_runner.clients)))
            str(len(runners.locust_runner.clients))
            os.environ['SLAVES_COUNT'] = str(len(runners.locust_runner.clients))
            print("RPS number: {}".format(rps_number))
            clients_number += data['user_count']
            # print(data['user_count'])
            # print(len(runners.locust_runner.clients))
            # print(runners.locust_runner.clients[client_id].__dict__)
