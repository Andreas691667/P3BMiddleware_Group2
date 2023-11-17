import numpy as np
import matplotlib.pyplot as plt
import os
from random import shuffle

def read_all_files_from_directory(directory_str):
    directory = os.fsencode(directory_str)
    content = []
    split_indexes = []
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith(".txt"):
            f = open(directory_str + filename, "r")
            lines : str = f.read()
            lines = lines.split("\n")
            lines = lines[:len(lines)-1]
            content += lines
            split_indexes.append(len(content)-1)
    return content, split_indexes


lines, split_indexes = read_all_files_from_directory("log_files/transmission_times/")

def get_feature(line, feature):
    feature_num = 0 if feature == "msg_id" else (1 if feature == "tm_stamp" else 2)
    data_sep = line.split(";")
    feature = float(data_sep[feature_num]) if feature == "tm_stamp" or feature == "ts_time" else int(data_sep[feature_num])
    return feature


def plot_transmission_times_by_color():
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

def trans_time_plot(ts_times, split_indexes,a=0.75):
    ts_times_sorted = sorted(ts_times)
    # get 75% of the data
    ts_times_a = ts_times_sorted[:int(len(ts_times_sorted)*a)]

    # shuffle data again
    shuffle(ts_times_a)

    plt.subplot(2, 2, 2)
    plt.boxplot(ts_times_a, vert=False, meanline=True)
    plt.xlabel("Transmission time in ms")
    plt.ylabel("")

    plt.subplot(2, 2, 4)
    ts_times_shuffle = ts_times
    shuffle(ts_times_shuffle)
    plt.plot(ts_times_shuffle, 'o')
    plt.xlabel("Message number")
    plt.ylabel("Transmission time in ms")
    plt.ylim(min(ts_times_a)-10, max(ts_times_a)+10)
    # draw box around the 75% of the data
    plt.plot([0, len(ts_times_shuffle)], [min(ts_times_a), min(ts_times_a)], color="red", label=f'min: {min(ts_times_a)}')
    plt.plot([0, len(ts_times_shuffle)], [max(ts_times_a), max(ts_times_a)], color="green", label=f'max: {max(ts_times_a)}')
    # place legens bottom right
    plt.legend(loc='lower right')

    plt.subplot(1, 2, 1)
    plt.plot(ts_times_shuffle, 'o')
    plt.xlabel("Message number")
    plt.ylabel("Transmission time in ms")
    # draw box around the 75% of the data
    plt.plot([0, len(ts_times_shuffle)], [min(ts_times_a), min(ts_times_a)], color="red")
    plt.plot([0, len(ts_times_shuffle)], [max(ts_times_a), max(ts_times_a)], color="red")

    # plot split indexes as vertical lines
    # for index in split_indexes:
    #     plt.axvline(x=index, color="green")


    plt.show()

def message_loss(msg_ids, split_indexes):
    index_0 = 0
    losses = []
    for index in split_indexes:
        ids = msg_ids[index_0:index]
        if len(ids) != 0:
            id_0 = ids[0]
            loss = 0
            for id in ids:
                if id_0 != id:
                    loss += 1
                id_0 += 1
            losses.append(loss)
            index_0 = index

    # plot the losses in a bar chart
    plt.bar(range(len(losses)), losses)
    plt.xlabel("Game number")
    plt.ylabel("Message loss")

    # calculate mean weighted by the number of messages

    no_msg = []
    for i, ind in enumerate(split_indexes):
        no_msg.append(ind - (0 if i == 0 else split_indexes[i-1]))

    weighted_loss_sum = 0
    for i, loss in enumerate(losses):
        weighted_loss_sum += loss*no_msg[i]
    weighted_loss_mean = weighted_loss_sum/sum(no_msg)

    # add mean line
    plt.axhline(y=weighted_loss_mean, color="red", label=f'Weighted mean: {weighted_loss_mean}')
    plt.legend(loc='upper right')
    # add non-weighted mean
    plt.axhline(y=sum(losses)/sum(no_msg), color="green", label=f'Mean: {sum(losses)/sum(no_msg)}')
    plt.legend(loc='upper right')


    plt.show()


# plot the transmission times
# trans_time_plot(ts_times, split_indexes)

# plot the message loss
message_loss(msg_ids, split_indexes)
