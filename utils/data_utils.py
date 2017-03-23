import os
import errno


def safely_mkdir(directory_path):
    """
    Safely create the given directory if it doesn't already exist.
    Return whether or not the directory was successfully made (True if already existed).
    """
    success = False
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            success = True
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise Exception("Could not safely create the directory: %s" % directory_path)
    else:
        success = True
    return success


#def createCurrentDateDir(parent_dir):
#    """
#    Create a new directory with the current date (ISO format) under the given parent_dir.
#    Return whether it was successful, the full path for the new directory, and the current date string.
#    If the date directory already exists or is not successful, default to returning the parent_dir as the full path.
#    """
#    current_date_str = date.today().isoformat()
#    dir_path = os.path.join(parent_dir, current_date_str)
#    success = data_utils.safely_mkdir(dir_path)
#    if not success:
#        # TODO: handle this better
#        # Safely default to returning the parent_dir if we cannot create the dir_path
#        print('Could not create a new directory for the current date [{}], defaulting to existing parent dir'.format(current_date_str))
#        dir_path = parent_dir
#    else:
#        print('Created new raw data dir: {}'.format(dir_path))
#    return success, dir_path, current_date_str
#
#
#def updateLatestDataDir(download_path, latest_path, latest_run_date_file, current_date_str, run_date_suffix):
#    """
#    Copies all files from the given download_path into the given latest_path configured in
#    `resources/constants.py`. Appends to the latest_run_date_file with the current_date_str and run_date_suffix.
#    """
#    if not download_path or not current_date_str:
#        print('Could not copy data to the "latest" directory! Current date: [{}],data path:  {}'.format(current_date_str, download_path))
#        return
#    dir_util.copy_tree(download_path, latest_path)
#    with open(latest_run_date_file, 'a') as run_file:
#        run_file.write('{}-{}\n'.format(current_date_str, run_date_suffix))
#    return

