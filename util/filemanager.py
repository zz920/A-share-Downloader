import os
import _pickle as pickle
import logging


def append_to_pkl(data, filepath):
    """
    # append data into an existent pickle file
    #
    # parameter:
    #   data : any picklable type | picklable data
    #   filepath : string | pickle file
    #
    # return:
    #   status : Boolean | success status
    """
    if os.path.exists(filepath) and os.path.isfile(filepath):
        if filepath.endswith(".pkl"):
            try:
                with open(filepath, 'ab') as pklfile:
                    pickle.dump(data, pklfile)
            except Exception as e:
                logging.error("IOError: %s" % e)
                return False
        else:
            logging.error("File %s is not pickle type file." % filepath)
            return False
    else:
        logging.error("File %s does not exist." % filepath)
        return False

    return True


def remove_pkl(filepath):

    """
    # remove existent pickle file
    #
    # parameter:
    #   filepath : string | pickle file
    #
    # return:
    #   status : Boolean | success status
    """

    if os.path.exists(filepath) and os.path.isfile(filepath):
        if filepath.endswith(".pkl"):
            try:
                os.remove(filepath)
            except Exception as e:
                logging.error(e)
                return False
        else:
            logging.error("File %s is not pickle type file." % filepath)
            return False
    else:
        logging.warning("File %s does not exist." % filepath)
        return True
    return True


def load_from_pkl(filepath):

    """
    # load data from a pickle file
    #
    # parameter:
    #   filepath : string | pickle file
    #
    # return:
    #   data : list | list of unpickled data
    """

    data = []
    if os.path.exists(filepath) and os.path.isfile(filepath):
        if filepath.endswith(".pkl"):
            try:
                with open(filepath, 'rb') as pklfile:
                    while True:
                        try:
                            data.append(pickle.load(pklfile))
                        except EOFError:
                            break
            except Exception as e:
                logging.error(e)

        else:
            logging.error("File %s is not pickle type file." % filepath)
    else:
        logging.error("File %s does not exist." % filepath)

    return data


def save_to_csv(data, filepath):

    """
    # save data into a csv file
    #
    # parameter:
    #   filepath : string | csv file
    #   data : pandas.DataFrame | data
    #
    # return:
    #   status : Boolean | success status
    """

    if not filepath.endswith('.csv'):
        logging.error("File name invalid. (%s)" % filepath)
        return False

    write_mode = 'w'
    header = True
    if os.path.exists(filepath):
        write_mode = 'a'
        header = False

    try:
        with open(filepath, write_mode) as f:
            f.write(data.to_csv(header=header, index=False))
    except Exception as e:
        logging.error(e)
        return False

    return True
