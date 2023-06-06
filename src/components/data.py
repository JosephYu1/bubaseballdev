import pandas as pd
import numpy as np

# have 3 different sets of data:
# 1. all players, private and public matches
# 2. only private
# 3. only public

base_path = r"./data_combined/"
date_str = r"20230228" # NOTE: change this here for the correct date of file (should be whatever that is latest)

BASEBALL_ALL = pd.read_csv(base_path + date_str + r"-combined-all-fixed-names.csv") # NOTE: assume directory start at /capstone. rstring for literal input
PLAYERS_ALL = np.sort(BASEBALL_ALL['Pitcher'].unique()) # returns a sorted list. Using np.sort() because it returns the result, whereas arr_test.sort() is in-place

BASEBALL_PRIVATE = pd.read_csv(base_path + date_str + r"-combined-private.csv")
PLAYERS_PRIVATE = np.sort(BASEBALL_PRIVATE['Pitcher'].unique())

BASEBALL_PUBLIC = pd.read_csv(base_path + date_str + r"-combined-public.csv")
PLAYERS_PUBLIC = np.sort(BASEBALL_PUBLIC['Pitcher'].unique())

# all attributes
ATTRIBUTES = BASEBALL_ALL.columns.values # this assumes that all files, between private and public, have the same columns

# base on the coachablility list given by Coach Furlong & Dr. Speegle
COACHABLE = ['RelSpeed', 'VertRelAngle', 'HorzRelAngle', 'SpinRate', 'SpinAxis',
             'Tilt', 'RelHeight', 'RelSide', 'Extension', 'HorzBreak', 
             'PlateLocHeight', 'PlateLocSide', 'ZoneSpeed', 'VertApprAngle',
             'HorzApprAngle', 'ZoneTime', 'EffectiveVelo', 'SpeedDrop'
            ]
