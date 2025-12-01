import argparse
from datetime import datetime, timedelta
import logging

# 1. Setup Logging
# This tells Python: "Save all log messages of level DEBUG 
# and higher to a file named 'simulate_downloader.log'"
logging.basicConfig(
    filename="downloader.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_target_info(dtstr, station_code):
    """
    Calculates the remote path and filename for the given datetime string and station code.
    """
    # try:
    #     # 1. Parse the input string (e.g, "20241206")
    #     dt = datetime.strptime(dtstr, "%Y%m%d")
    # except ValueError:
    #     print(f"Error: Invalid date format '{dtstr}'. Expected 'YYYYMMDD'.")
    #     return None, None
    
    # 2. Create the target path: /YYYY/DOY
    # %j = Day of year (001 to 366)
    target_path = f"/{dtstr.year:04d}/{dtstr.strftime('%j')}"

    # 3. Create a remote filename pattern (e.g., KGB1_20241206.dat)
    target_filename = f"{station_code.upper()}_{dtstr.strftime('%Y%m%d')}.dat"

    return target_path, target_filename

if __name__ == "__main__":

    #1. Use Argparse to get the date and station code from command line
    p = argparse.ArgumentParser(description="Simulate downloader target path and filename generation.")
    p.add_argument("--date", required=False, help="Date in YYYYMMDD format")
    p.add_argument("--start", required=True, help="Start Date in YYYYMMDD format for date range")
    p.add_argument("--end", required=True, help="End Date in YYYYMMDD format for date range")
    p.add_argument("--station", required=True, help=" 4-char Station code(e.eg., KGB1)")
    p.add_argument("--simulate", action="store_true", help="Simulate the download process")
    args = p.parse_args()

    # 2. Use Date logic to calculate the target path and filename
    # print(f"Simulating download for date: {args.date}, station: {args.station}")
    # path, filename = get_target_info(args.date, args.station)

    """ # 3. Simulate the download process by printing the target path and filename
    if path and filename:
        print(f"Date logic: {args.date } is Day of year {datetime.strptime(args.date, '%Y%m%d').strftime('%j')}")
        print(f"Remote Path: {path}")
        print(f"Remote Filename: {filename}")

        # This is where the actual download logic would go
        print("\n [Simulation] Connecting to sftp.server.com...\n")
        print(f" [Simulation] Downloading file '{filename}' from path '{path}' ...")
        print(" [Simulation] Download complete!")
        print(f"[Simulate] Attemting to save to local path: {path}/{filename}")
        print(" [Simulation] File saved successfully.")
    print("Simulation finished.") """

    # 3. Simulate Date loop Logic

    try:
        # Convert text-based start/end dates into real datetime objects
        current_date = datetime.strptime(args.start, "%Y%m%d")
        end_date = datetime.strptime(args.end, "%Y%m%d") # e.g., "20241210"
        
        # define a "oneday" time difference
        one_day =timedelta(days=1)

        logging.info(f"STARTING BACKFILL for station {args.station} from {args.start} to {args.end}")
        print(f"---Starting backfill for {args.station} from {args.start} to {args.end} ---")

        # loop from start to end, inclusive
        while current_date <= end_date:
            #1. Get the current date string in YYYYMMDD format
            dtstr = current_date.strftime("%Y%m%d")
            print(f"Processing date: {dtstr}")

            #2. Use Date Logic to calculate the target path and filename
            # Pass the datetime object directly to get_target_info
            path, filename = get_target_info(current_date, args.station)
            if path and filename:
                logging.info(f"Processing date {dtstr}: Path={path}, Filename={filename}")
                print(f"Date Logic: {dtstr} is Day of Year {current_date.strftime('%j')}")
                print(f"[SIMULATE] Attempting to download: {filename}")
                print(f"[SIMULATE] Attempting to save to local path: {path}/{filename}")
            # increment the date by one day
            current_date += one_day
        logging.info(f"COMPLETED BACKFILL for station {args.station} from {args.start} to {args.end}")
        print(f"---Backfill simulation complete---")
    except Exception as e:
        logging.error(f"Error during backfill simulation: {e}")
        print(f"Error during backfill simulation: {e}")
