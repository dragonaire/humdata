import os
import errno


def safely_mkdir(directory_path):
    success = False
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            success = True
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise Exception("Could not safely create the directory: %s" % directory_path)
    return success
