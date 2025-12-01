# FILE: Projects/Learn_FTP,DATE,LOG,ARGUMENT/utils.py
from datetime import datetime

def get_target_info(date_obj, station_code):
    """
    Calculates the remote path and filename pattern based on the 
    given datetime object and station code.
    """

    #Create the target path: /YYYY/DOY
    target_path = f"/{date_obj.year:04d}/{date_obj.strftime('%j')}"

    remote_file = f"{station_code.upper()}_{date_obj.strftime('%Y%m%d')}.dat"
    return target_path, remote_file