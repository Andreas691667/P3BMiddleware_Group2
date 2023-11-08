import os

def read_all_files_from_directory(directory_str):
    directory = os.fsencode(directory_str)
    content = [0]
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith(".txt"):
            f = open(directory_str + filename, "r")
            lines : str = f.read()
            lines = lines.split("\n")
            lines = lines[:len(lines)-1]
            content += lines
    return content

lines = read_all_files_from_directory("../log_files/")
