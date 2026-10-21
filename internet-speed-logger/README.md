# Internet Speed Logger

A small Python project that tests internet speed and saves the results in a CSV file.

It records ping, download speed, upload speed, the speed-test server, and the date and time. Failed tests are logged too.

## Setup

```cmd
py -m pip install -r requirements.txt
```

## Run

One test:

```cmd
py speed_logger.py
```

Five tests, one minute apart:

```cmd
py speed_logger.py --count 5 --interval 60
```

Results are added to `speed_log.csv` in the current directory.

**Note:** Uses the community-maintained `speedtest-cli` package. Results depend on the selected test server and network conditions, and the package may not work with every Speedtest server.
