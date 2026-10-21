

import argparse
import csv
import time
from datetime import datetime
from pathlib import Path

import speedtest

HEADERS = ["timestamp", "ping_ms", "download_mbps", "upload_mbps", "server", "status"]


def measure():
    test = speedtest.Speedtest(secure=True)
    server = test.get_best_server()
    download = test.download() / 1_000_000
    upload = test.upload() / 1_000_000
    return {
        "ping_ms": round(test.results.ping, 2),
        "download_mbps": round(download, 2),
        "upload_mbps": round(upload, 2),
        "server": f"{server.get('sponsor', 'Unknown')} - {server.get('name', 'Unknown')}",
        "status": "OK",
    }


def save_row(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        if needs_header:
            writer.writeheader()
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Log internet speed tests to CSV.")
    parser.add_argument("--count", type=int, default=1, help="Number of tests (default: 1)")
    parser.add_argument("--interval", type=int, default=60, help="Seconds between tests (default: 60)")
    parser.add_argument("--output", type=Path, default=Path("speed_log.csv"), help="CSV output file")
    args = parser.parse_args()

    if args.count < 1 or args.interval < 1:
        parser.error("--count and --interval must be positive integers")

    try:
        for number in range(args.count):
            print(f"Running speed test {number + 1}/{args.count}...")
            row = {"timestamp": datetime.now().astimezone().isoformat(timespec="seconds")}
            try:
                row.update(measure())
                print(f"Ping: {row['ping_ms']} ms | Download: {row['download_mbps']} Mbps | Upload: {row['upload_mbps']} Mbps")
            except (speedtest.SpeedtestException, OSError, ValueError) as exc:
                row.update({"ping_ms": "", "download_mbps": "", "upload_mbps": "", "server": "", "status": f"ERROR: {str(exc)[:150]}"})
                print(f"Test failed: {exc}")
            save_row(args.output, row)
            print(f"Saved to {args.output}\n")
            if number < args.count - 1:
                time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    main()
