import os
import logging


#///////////////////////
# PROJECT BASE DIRECTORY
#///////////////////////

BASE_DIR = os.getcwd()


#//////////////////
# DATABASE SETTINGS
#//////////////////

# FORMART 'dbtype://username:password@ip:port/dbname'
DB_CONNECTION = 'postgresql://zhibowen:zhibowen@localhost:5432/stockdb'


#/////////////
# LOG SETTINGS
#/////////////

# LOG LEVEL INCREASES FROM UP TO DOWN  
#LOGLEVEL = 0    # logging.NOTSET level
LOGLEVEL = 10    # logging.DEBUG level
#LOGLEVEL = 20   # logging.INFO level
#LOGLEVEL = 30   # logging.WARNING level
#LOGLEVEL = 40   # logging.ERROR level
#LOGLEVEL = 50   # logging.CRITICAL level

# LOG FILE NAME
LOGFILENAME = os.path.join(BASE_DIR, 'stock.log')

# LOGGING CONFIG
logging.basicConfig(
            level=LOGLEVEL,
            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=LOGFILENAME,
            filemode='w'
        )

#//////////////////
# DATA FILE SETTING
#//////////////////

# DEFAULT PICKLE FILE PATH
DATAFILENAME = os.path.join(BASE_DIR, 'stock.pkl')
