import csv

LADDER_FILEPATH = "data/ladder.txt"
DATA_FILEPATH = "data/data.txt"
ORIGINAL_LADDER_FILEPATH = "data/original_ladder.txt"


def read_ladder_list(original=False):
    fp = LADDER_FILEPATH if not original else ORIGINAL_LADDER_FILEPATH 
    # read ladder.txt into a list
    with open(fp, "r") as f:
        player_list = f.readlines()

    # remove newlines and whitespaces
    player_list = [line.strip() for line in player_list]

    # return list of registered players in a list form
    return player_list


def read_records_list():
    # read data.txt into a 2D array
    with open(DATA_FILEPATH, "r") as f:
        reader = csv.reader(f, delimiter="/")

        # remove newlines and whitespaces
        history_list = [[el.strip() for el in line if el] for line in reader if line]

    # return a history of challenges and player registration/withdrawal in a 2D array form
    return history_list


def write_record_list(records_2d_array):
    with open(DATA_FILEPATH, "w") as f:
        writer = csv.writer(f, delimiter="/")
        for record in records_2d_array:
            writer.writerow(record)


def append_to_record_list(record_list):
    csv_line = "/".join(record_list)
    with open(DATA_FILEPATH, "a") as f:
        f.write(f"{csv_line}\n")


def write_leaderboard(ladder_list):
    with open(LADDER_FILEPATH, "w") as f:
        f.write("\n".join(ladder_list))


def append_to_player_list(name):
    with open(LADDER_FILEPATH, "a") as f:
        f.write(f"{name}\n")


def delete_from_player_list(name):
    with open(LADDER_FILEPATH, "r+") as f:
        player_list = f.readlines()
        f.seek(0)  # go back to the start of the file
        # rewrite lines, not including the name to be deleted
        for line in player_list:
            if not line.strip() == name:
                f.write(line)
        f.truncate()  # truncate the remaining of the file
