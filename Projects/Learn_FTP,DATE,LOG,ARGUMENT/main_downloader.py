import argparse
import logging
from datetime import datetime, timedelta
from utils import get_target_info

#setup logging
logging.basicConfig(
    filename="downloader.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="FTP File Downloader")
    p.add_argument("--start", required=True, help="Start date in YYYY-MM-DD format")
    p.add_argument("--end", required=True, help="End date in YYYY-MM-DD format")
    p.add_argument("--station", required=True, help="Station code (e.g., ABC)")
    args = p.parse_args()

    try:
        current_datetime = datetime.strptime(args.start, "%Y%m%d")
        end_datetime = datetime.strptime(args.end, "%Y%m%d")
        logging.info(f"-- Starting download from {args.start} to {args.end} for station {args.station} ---")
        print(f"Downloading files from {args.start} to {args.end} for station {args.station}")

        while current_datetime <= end_datetime:
            # We call the function to get the target path and filename
            target_path, remote_file = get_target_info(current_datetime, args.station)
            logging.info(f"Target Path: {target_path}, Remote File: {remote_file}")
            print(f"Would download: {target_path}/{remote_file}")

            if target_path and remote_file:
                logging.info(f"Prepared to download {remote_file} from {target_path}")
            # Move to the next day
            current_datetime += timedelta(days=1)
        logging.info("--- Download process completed ---")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
    