import file_utils
from datetime import datetime, timedelta


def _convert_string_to_datetime_obj(date_str):
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except:
        return None


def _convert_datetime_obj_to_string(date_obj):
    try:
        return date_obj.strftime("%d-%m-%Y")
    except:
        return None


### DISPLAYS ###


def get_leaderboard():
    # list of names, in order of highest to lowest
    # print(file_utils.read_ladder_list())
    return file_utils.read_ladder_list()


def get_yet_to_play_challenges():
    records = file_utils.read_records_list()
    yet_to_play_challenges = [
        record
        for record in records
        if len(record) == 3
        and (
            _convert_string_to_datetime_obj(record[2])
            >= (datetime.today() - timedelta(days=1))
        )
    ]
    for challenge in yet_to_play_challenges:
        # remove the past ranking from displaying
        challenge[0] = challenge[0].rsplit(" ", 1)[0]
        challenge[1] = challenge[1].rsplit(" ", 1)[0]
    # yet_to_play_challenges = []
    # # CHECK that the challenges have not overrun yet
    # # it's not counted if the challenge has past.
    # for record in yet_to_play_challenges:
    #     record_date = _convert_string_to_datetime_obj(record[2])
    #     print(record_date, datetime.today())
    #     if record_date <= datetime.today():
    #         yet_to_play_challenges.remove(record)
    return yet_to_play_challenges


def get_most_recent_challenges():
    records = file_utils.read_records_list()
    records_with_results = [record for record in records if len(record) == 4]
    for record in records_with_results:
        record[2] = _convert_string_to_datetime_obj(record[2])
    sorted_records = sorted(records_with_results, key=lambda x: x[2], reverse=True)
    for record in sorted_records:
        record[2] = _convert_datetime_obj_to_string(record[2])
    if len(sorted_records) >= 5:
        sorted_records = sorted_records[:5]
    return sorted_records


### CHALLENGE ###


def create_challenge(challenger, opponent, date):
    leaderboard = file_utils.read_ladder_list()
    ranking_diff = leaderboard.index(challenger) - leaderboard.index(opponent)
    # cannot create a challenge if opponent's ranking is more than 3 higher than you
    if not (0 < ranking_diff <= 3):
        return False
    else:
        file_utils.append_to_record_list(
            [
                f"{challenger} {leaderboard.index(challenger) + 1}",
                f"{opponent} {leaderboard.index(opponent) + 1}",
                date,
            ]
        )
        return True


def record_challenge_result(challenger, opponent, date, results):
    # append to csv file (data.txt)
    # update leaderboard and most recent challenges
    records = file_utils.read_records_list()
    for i in range(len(records)):
        if len(records[i]) == 3:
            if (
                challenger in records[i][0]
                and opponent in records[i][1]
                and date in records[i][2]
            ):
                break
    else:
        # no match found for the challenge
        return False

    records[i] = records[i] + [results]
    # after editing records, rewrite the file to data.txt
    file_utils.write_record_list(records)

    ladder = get_leaderboard()
    winner, loser = _get_winner_from_record(records[i])
    winner = winner.rsplit(" ", 1)[0]
    loser = loser.rsplit(" ", 1)[0]
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
    file_utils.write_leaderboard(ladder)
    return True


### REGISTRATION & DEREGISTRATION ###


def register_new_player(name):
    # make sure that the player is not registered yet before registering
    if name not in get_leaderboard():
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
    if name in get_leaderboard():
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
    original_ladder = file_utils.read_ladder_list(original=True)
    records = file_utils.read_records_list()
    ladder = original_ladder.copy()

    for record in records:
        if len(record) == 4:
            if _convert_string_to_datetime_obj(record[2]) <= datetime_obj:
                challenger, c_rank = record[0].rsplit(" ", 1)
                opponent, o_rank = record[1].rsplit(" ", 1)
                c_rank, o_rank = int(c_rank), int(o_rank)
                winner, _ = _get_winner_from_record(record)
                winner = winner.rsplit(" ", 1)[0]

                if challenger == winner:
                    ladder.remove(winner)
                    ladder.insert(o_rank-1, winner)

        elif len(record) == 2:
            if _convert_string_to_datetime_obj(record[1]) <= datetime_obj:
                status = record[0][0]
                name = record[0][1:]
                if status == "-":
                    name, score = name.rsplit(" ", 1)
                    ladder.remove(name)
                elif status == "+":
                    ladder.append(name)

    return ladder


# Query B
def get_challenges_by_names(name1, name2):
    records = file_utils.read_records_list()
    challenges = []
    for record in records:
        # disregard registration data
        if len(record) > 2:
            challenger = record[0].rsplit(" ", 1)[0]
            opponent = record[1].rsplit(" ", 1)[0]
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
        if len(record) != 2:
            record_date = record[2]
            # match dates
            if record_date == input_date:
                record[0] = record[0].rsplit(" ", 1)[0]
                record[1] = record[1].rsplit(" ", 1)[0]
                challenges.append(record)
    return challenges


# Query D
def get_list_of_player_matches(name):
    records = file_utils.read_records_list()
    player_matches = []
    for record in records:
        # disregard registration data
        if len(record) > 2:
            record[0] = record[0].rsplit(" ", 1)[0]
            record[1] = record[1].rsplit(" ", 1)[0]
            challenger = record[0]
            opponent = record[1]
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
        name1 = name1.rsplit(" ", 1)[0]
        name2 = name2.rsplit(" ", 1)[0]

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
    return most_active_list, max_count


# Query F
def get_least_active_players():
    # get list of least active players
    dic = _get_num_matches_dict()
    min_count = min(dic.values())
    least_active_list = [name for name, count in dic.items() if count == min_count]
    return least_active_list, min_count


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
                record[0] = record[0].rsplit(" ", 1)[0]
                record[1] = record[1].rsplit(" ", 1)[0]
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
        winner = winner.rsplit(" ", 1)[0]

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
    return most_wins_list, max_wins


# Query H - extra query
def get_player_with_least_wins():
    num_wins_dict = {}
    records_list = file_utils.read_records_list()
    for record in records_list:
        # we do not want to include matches that are yet to happen
        # we are also not concerned with player registration or withdrawal records
        # a match that happened would have 4 columns
        if len(record) != 4:
            continue

        winner, loser = _get_winner_from_record(record)
        winner = winner.rsplit(" ", 1)[0]

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

    min_wins = min(num_wins_dict.values())
    least_wins_list = [
        name for name, count in num_wins_dict.items() if count == min_wins
    ]
    return least_wins_list, min_wins
