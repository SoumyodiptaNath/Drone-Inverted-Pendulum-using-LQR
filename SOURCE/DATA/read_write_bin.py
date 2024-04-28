import pickle


def read_bin(file_path):
    with open(file_path, "rb") as f_in:
        stuff = pickle.load(f_in)
    return stuff


def write_bin(stuff, file_path):
    with open(file_path, "wb") as f_out:
        pickle.dump(stuff, f_out)
