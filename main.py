from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY
from collector import CloudwatchLogsCollector
import time
import datetime


def main():
    port = 9106
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
          "Starting exporter on :", port)
    try:
        start_http_server(port)
        REGISTRY.register(CloudwatchLogsCollector())
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print(" Interrupted")
        exit(0)


if __name__ == "__main__":
    main()
