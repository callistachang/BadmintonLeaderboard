import file_utils
from datetime import datetime


def _convert_string_to_datetime_obj(date_str):
    return datetime.strptime(date_str, "%d-%m-%Y")


def _convert_datetime_obj_to_string(date_obj):
    return date_obj.strftime("%d-%m-%Y")


### DISPLAYS ###


def get_leaderboard():
    # list of names, in order of highest to lowest
    print(file_utils.read_ladder_list())
    return file_utils.read_ladder_list()


def get_yet_to_play_challenges():
    records = file_utils.read_records_list()
    yet_to_play_challenges = [record for record in records if len(record) == 3]
    # CHECK that the challenges have not overrun yet
    # it's not counted if the challenge has past.
    for record in yet_to_play_challenges:
        record_date = _convert_string_to_datetime_obj(record[2])
        if record_date <= datetime.today():
            yet_to_play_challenges.remove(record)
    return yet_to_play_challenges


def get_most_recent_challenges():
    records = file_utils.read_records_list()
    records_with_results = [record for record in records if len(record) == 4]
    # get the 5 most recent results if there are at least 5, if not return the amount
    if len(records_with_results) >= 5:
        records_with_results = records_with_results[-5:]
    return records_with_results


### CHALLENGE ###


def create_challenge(challenger, opponent, date):
    leaderboard = file_utils.read_ladder_list()
    ranking_diff = leaderboard.index(opponent) - leaderboard.index(challenger)
    # cannot create a challenge if opponent's ranking is more than 3 higher than you
    if ranking_diff > 3:
        return False
    else:
        file_utils.append_to_record_list([challenger, opponent, date])
        return True


def record_challenge_result(name1, name2, results):
    # append to csv file (data.txt)
    # update leaderboard and most recent challenges
    records = file_utils.read_records_list()
    for i in range(len(records)):
        if len(records[i]) == 3:
            challenger, opponent, _ = records[i]
            if (name1 == challenger and name2 == opponent) or (
                name1 == opponent and name2 == challenger
            ):
                break
    else:
        # no match found for the challenge
        return False

    records[i] = records[i] + [results]
    # after editing records, rewrite the file to data.txt
    file_utils.write_record_list(records)
    return True


### REGISTRATION & DEREGISTRATION ###


def register_new_player(name):
    # make sure that the player is not registered yet before registering
    if name not in get_player_names():
        # append to ladder.txt
        file_utils.append_to_player_list(name)
        # enter record of registration to data.txt
        file_utils.append_to_record_list(
            [f"+{name}", _convert_datetime_obj_to_string(datetime.today())]
        )
        return True
    else:
        return False


def withdraw_player(name):
    # make sure that the player is registered before withdrawing
    if name in get_player_names():
        # append to ladder.txt
        file_utils.delete_from_player_list(name)
        # enter record of registration to data.txt
        file_utils.append_to_record_list(
            [f"-{name}", _convert_datetime_obj_to_string(datetime.today())]
        )
        return True
    else:
        return False


### QUERIES ###


def _get_winner_from_record(record):
    if len(record) != 4:
        return None
    challenger, opponent, date, scores = record
    # 22-20 19-21 20-22
    # to [(22, 20), (19, 21), (20, 22)]
    scores = [score.split("-") for score in scores.split()]
    challenger_score = 0
    opponent_score = 0
    for score in scores:
        if int(score[0]) > int(score[1]):
            challenger_score += 1
        elif int(score[0]) < int(score[1]):
            opponent_score += 1

    if challenger_score > opponent_score:
        winner = challenger
        loser = opponent
    else:
        winner = opponent
        loser = challenger
    return winner, loser


# Query A
def get_leaderboard_on_date(date):
    datetime_obj = _convert_string_to_datetime_obj(date)
    records = file_utils.read_records_list()
    # og_leaderboard = file_utils.read_ladder_list(original=True)
    # find the point in the records that has surpassed the input date
    ladder = []
    for record in records:
        # register/deregister records
        if len(record) == 2:
            record_date = _convert_string_to_datetime_obj(record[1])
            # only consider datetime before a certain date
            if record_date <= datetime_obj:
                register_status = record[0][0]
                name = record[0][1:]
                if register_status == "+":
                    # append their name to the end of the ladder after registering
                    ladder = ladder + [name]
                elif register_status == "-":
                    ladder.remove(name)

                # print(record)
                # print(ladder)
                # print()
        # played games records
        elif len(record) == 4:
            record_date = _convert_string_to_datetime_obj(record[2])
            # only consider datetime before a certain date
            if record_date <= datetime_obj:
                winner, loser = _get_winner_from_record(record)
                # both are not in the ladder yet...
                # add both to end of ladder
                if (winner not in ladder) and (loser not in ladder):
                    ladder.append(winner)
                    ladder.append(loser)
                # loser not in the ladder yet...
                # add loser to end of ladder
                elif (winner in ladder) and (loser not in ladder):
                    ladder.append(loser)
                # winner not in ladder yet but loser in the ladder
                # let it win the loser
                elif (winner not in ladder) and (loser in ladder):
                    loser_pos = ladder.index(loser)
                    ladder.insert(loser_pos, winner)
                # winner in ladder and loser in ladder
                # winner takes over loser's position
                # winner in the ladder - will take over the loser's position
                else:
                    winner_pos = ladder.index(winner)
                    loser_pos = ladder.index(loser)
                    # if the winner is of a higher rank
                    # ladder doesn't change
                    if winner_pos < loser_pos:
                        pass
                    # if the loser is of a higer rank than the winner
                    else:
                        ladder.remove(winner)
                        ladder.insert(loser_pos, winner)

                # print(record)
                # print(ladder)
                # print()

    # print(ladder)
    return ladder


# Query B
def get_challenges_by_names(name1, name2):
    records = file_utils.read_records_list()
    challenges = []
    for record in records:
        # disregard registration data
        if len(records[i]) > 2:
            challenger = records[0]
            opponent = records[1]
            # match names
            if (name1 == challenger and name2 == opponent) or (
                name1 == opponent and name2 == challenger
            ):
                challenges.append(record)
    return challenges


# Query C
def get_challenges_by_date(input_date):
    records = file_utils.read_records_list()
    challenges = []
    for record in records:
        # disregard registration data
        if len(records[i]) != 2:
            record_date = records[2]
            # match dates
            if record_date == input_date:
                challenges.append(record)
    return challenges


# Query D
def get_list_of_player_matches(name):
    records = file_utils.read_records_list()
    player_matches = []
    for record in records:
        # disregard registration data
        if len(records[i]) > 2:
            challenger = records[0]
            opponent = records[1]
            if name == challenger or name == opponent:
                player_matches.append(record)
    return player_matches


def _get_num_matches_dict():
    dic = {}
    records_list = file_utils.read_records_list()
    for record in records_list:
        # we do not want to include matches that are yet to happen
        # we are also not concerned with player registration or withdrawal records
        # a match that happened would have 4 columns
        if len(record) != 4:
            continue

        name1, name2, _, _ = record

        # add the number of matches per person into a dictionary
        # { name: number_of_matches }
        if name1 in dic:
            dic[name1] += 1
        else:
            dic[name1] = 1

        if name2 in dic:
            dic[name2] += 1
        else:
            dic[name2] = 1

    # include players who have not played a single match
    # { name: 0 }
    players = file_utils.read_ladder_list()
    players_who_havent_played = list(set(players) - set(dic.keys()))
    for player in players_who_havent_played:
        dic[player] = 0

    return dic


# Query E
def get_most_active_players():
    # get list of most active players
    dic = _get_num_matches_dict()
    max_count = max(dic.values())
    most_active_list = [name for name, count in dic.items() if count == max_count]
    return most_active_list


# Query F
def get_least_active_players():
    # get list of least active players
    dic = _get_num_matches_dict()
    min_count = min(dic.values())
    least_active_list = [name for name, count in dic.items() if count == min_count]
    return least_active_list


# Query G
def get_matches_list_within_date_range(date_start, date_end):
    date_obj_start = _convert_string_to_datetime_obj(date_start)
    date_obj_end = _convert_string_to_datetime_obj(date_end)
    records = file_utils.read_records_list()
    index_start = index_end = None

    date_range_records = []

    for record in records:
        if len(record) > 2:
            record_date_obj = _convert_string_to_datetime_obj(record[2])
            if date_obj_start <= record_date_obj <= date_obj_end:
                date_range_records.append(record)

    return date_range_records


# Query H - extra query
def get_player_with_most_wins():
    num_wins_dict = {}
    records_list = file_utils.read_records_list()
    for record in records_list:
        # we do not want to include matches that are yet to happen
        # we are also not concerned with player registration or withdrawal records
        # a match that happened would have 4 columns
        if len(record) != 4:
            continue

        winner, loser = _get_winner_from_record(record)

        # { name: number_of_wins }
        if winner in num_wins_dict:
            num_wins_dict[winner] += 1
        else:
            num_wins_dict[winner] = 1

    # include players who have not won
    players = file_utils.read_ladder_list()
    players_who_havent_won = list(set(players) - set(num_wins_dict.keys()))
    for player in players_who_havent_won:
        num_wins_dict[player] = 0

    max_wins = max(num_wins_dict.values())
    most_wins_list = [
        name for name, count in num_wins_dict.items() if count == max_wins
    ]
    return most_wins_list
