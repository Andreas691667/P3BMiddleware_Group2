import numpy as np
import matplotlib.pyplot as plt
import os
from random import shuffle

def read_all_files_from_directory(directory_str):
    directory = os.fsencode(directory_str)
    content = []
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith(".txt"):
            f = open(directory_str + filename, "r")
            lines : str = f.read()
            lines = lines.split("\n")
            lines = lines[:len(lines)-1]
            content += lines
    return content


lines = read_all_files_from_directory("log_files/transmission_times/")

def get_feature(line, feature):
    feature_num = 0 if feature == "msg_id" else (1 if feature == "tm_stamp" else 2)
    data_sep = line.split(";")
    feature = float(data_sep[feature_num]) if feature == "tm_stamp" or feature == "ts_time" else int(data_sep[feature_num])
    return feature


def plot_transmission_times_by_color ():
    msg_ids_1 = [get_feature(line, "msg_id") for line in lines][: split_indexes[0]]
    tm_stamps_1 = [get_feature(line, "tm_stamp") for line in lines][: split_indexes[0]]
    ts_times_1 = [get_feature(line, "ts_time") for line in lines][: split_indexes[0]]

    msg_ids_2 = [get_feature(line, "msg_id") for line in lines][split_indexes[0]: split_indexes[1]]
    tm_stamps_2 = [get_feature(line, "tm_stamp") for line in lines][split_indexes[0]: split_indexes[1]]
    ts_times_2 = [get_feature(line, "ts_time") for line in lines][split_indexes[0]: split_indexes[1]]

    msg_ids_3 = [get_feature(line, "msg_id") for line in lines][split_indexes[1]: split_indexes[2]]
    tm_stamps_3 = [get_feature(line, "tm_stamp") for line in lines][split_indexes[1]: split_indexes[2]]
    ts_times_3 = [get_feature(line, "ts_time") for line in lines][split_indexes[1]: split_indexes[2]]

    msg_ids_4 = [get_feature(line, "msg_id") for line in lines][split_indexes[2]: split_indexes[3]]
    tm_stamps_4 = [get_feature(line, "tm_stamp") for line in lines][split_indexes[2]: split_indexes[3]]
    ts_times_4 = [get_feature(line, "ts_time") for line in lines][split_indexes[2]: split_indexes[3]]


    plt.plot(ts_times_1, 'o', color="red")
    plt.plot(ts_times_2, 'o', color="blue")
    plt.plot(ts_times_3, 'o', color="green")
    plt.plot(ts_times_4, 'o', color="purple")

    plt.show()


msg_ids = [get_feature(line, "msg_id") for line in lines]
tm_stamps = [get_feature(line, "tm_stamp") for line in lines]
ts_times = [get_feature(line, "ts_time") for line in lines]

# Shift timestamps
tm_stamps_shiftet = [(tm_stamp-min(tm_stamps))/10**9 for tm_stamp in tm_stamps]

# shuffle the data
# shuffle(ts_times)
mean = np.mean(ts_times)
var = np.var(ts_times)
plt.plot(ts_times, 'o')
plt.show()

