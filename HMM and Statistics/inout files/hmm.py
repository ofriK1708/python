import random
from math import log


# 1 - C - cloudy
# 2 - P - Plain
# 3 - H - HOT


def getGame(currWeather):
    if currWeather == 'C':
        return getGameCloudy()
    elif currWeather == 'P':
        return getGamePlain()
    elif currWeather == 'H':
        return getGameHot()


def getGameCloudy():
    game = random.randint(1, 10)
    if game <= 7:
        return 'B'
    elif game <= 9:
        return 'S'
    else:
        return 'C'


def getGamePlain():
    game = random.randint(1, 10)
    if game <= 6:
        return 'B'
    elif game <= 9:
        return 'S'
    else:
        return 'C'


def getGameHot():
    game = random.randint(1, 10)
    if game <= 1:
        return 'B'
    elif game <= 2:
        return 'S'
    else:
        return 'C'


def getWeather(weather):
    if weather == 'C':
        return getWeatherCloudy()
    elif weather == 'P':
        return getWeatherPlain()
    elif weather == 'H':
        return getWeatherHot()


def getWeatherCloudy():
    next_weather = random.randint(1, 10)
    if next_weather <= 5:
        return 'C'
    elif next_weather <= 8:
        return 'P'
    else:
        return 'H'


def getWeatherPlain():
    next_weather = random.randint(1, 10)
    if next_weather <= 2:
        return 'C'
    elif next_weather <= 7:
        return 'P'
    else:
        return 'H'


def getWeatherHot():
    next_weather = random.randint(1, 10)
    if next_weather <= 4:
        return 'C'
    elif next_weather <= 6:
        return 'P'
    else:
        return 'H'


def HMM():
    hmm_out = open("HMM_OUT", "w")
    game_out = open("GAME_OUT", "r")
    p_mat = [[], [], []]  # 0 - C, 1 - P, 2 - H
    last_states = []  # 0 - C, 1 - P, 2 - H
    next_weathers = [[0.5, 0.3, 0.2], [0.2, 0.5, 0.3], [0.4, 0.2, 0.4]]  # odds of weather change
    games_by_weather = [[0.2, 0.7, 0.1], [0.6, 0.3, 0.1], [0.1, 0.1, 0.8]]  # odds of game by weather
    first_game = game_out.read(1)
    if first_game == 'B':
        last_states.append(log(0.3) + log(games_by_weather[0][0]))
        last_states.append(log(0.3) + log(games_by_weather[0][1]))
        last_states.append(log(0.3) + log(games_by_weather[0][2]))
    elif first_game == 'S':
        last_states.append(log(0.3) + log(games_by_weather[1][0]))
        last_states.append(log(0.3) + log(games_by_weather[1][1]))
        last_states.append(log(0.3) + log(games_by_weather[1][2]))
    else:  # first_game == 'C'
        last_states.append(log(0.3) + log(games_by_weather[2][0]))
        last_states.append(log(0.3) + log(games_by_weather[2][1]))
        last_states.append(log(0.3) + log(games_by_weather[2][2]))

    for f in range(gameLoop - 1):
        temp = [0, 0, 0]

        temp_prev_values = [(last_states[0]) + log(next_weathers[0][0]),
                            (last_states[1]) + log(next_weathers[1][0]),
                            (last_states[2]) + log(next_weathers[2][0])]
        temp[0] = max(temp_prev_values)
        max_index = temp_prev_values.index(max(temp_prev_values))
        p_mat[0].append(max_index)

        temp_prev_values = [(last_states[0]) + log(next_weathers[0][1]),
                            (last_states[1]) + log(next_weathers[1][1]),
                            (last_states[2]) + log(next_weathers[2][1])]
        temp[1] = max(temp_prev_values)
        max_index = temp_prev_values.index(max(temp_prev_values))
        p_mat[1].append(max_index)

        temp_prev_values = [(last_states[0]) + log(next_weathers[0][2]),
                            (last_states[1]) + log(next_weathers[1][2]),
                            (last_states[2]) + log(next_weathers[2][2])]
        temp[2] = max(temp_prev_values)
        max_index = temp_prev_values.index(max(temp_prev_values))
        p_mat[2].append(max_index)

        current_game = game_out.read(1)
        if current_game == 'B':
            temp[0] += log(games_by_weather[0][0])
            temp[1] += log(games_by_weather[0][1])
            temp[2] += log(games_by_weather[0][2])

        elif current_game == 'S':
            temp[0] += log(games_by_weather[1][0])
            temp[1] += log(games_by_weather[1][1])
            temp[2] += log(games_by_weather[1][2])
        else:  # current_game == 'C'
            temp[0] += log(games_by_weather[2][0])
            temp[1] += log(games_by_weather[2][1])
            temp[2] += log(games_by_weather[2][2])

        last_states = temp

    game_out.close()
    rev_best_route = []
    max_index = last_states.index(max(last_states))
    rev_best_route.append(max_index)
    for j in range(gameLoop - 2, -1, -1):
        max_index = p_mat[max_index][j]
        rev_best_route.append(max_index)

    for k in range(len(rev_best_route) - 1, -1, -1):
        match rev_best_route[k]:
            case 0:
                hmm_out.write("C")
            case 1:
                hmm_out.write("P")
            case 2:
                hmm_out.write("H")
    hmm_out.close()


def getAccuracy():
    weather_out = open("WEATHER_OUT", "r")
    hmm_out = open("HMM_OUT", "r")
    weather_check = 'P'
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for r in range(gameLoop):
        true_weather = weather_out.read(1)
        hmm_weather = hmm_out.read(1)
        if true_weather == weather_check:
            if hmm_weather == weather_check:
                true_positive += 1
            else:
                false_negative += 1
        else:  # true_weather == 'C' or true_weather == 'P'
            if hmm_weather == weather_check:
                false_positive += 1
            else:
                true_negative += 1

    print("True Positive: %", (true_positive * 100) / gameLoop)
    print("True Negative: %", (true_negative * 100) / gameLoop)
    print("False Positive: %", (false_positive * 100) / gameLoop)
    print("False Negative: %", (false_negative * 100) / gameLoop)
    weather_out.close()


# ----------------------------- Main ----------------------------------------

# random.seed(1) # for testing purposes
gameOut = open("GAME_OUT", "w")
weatherOut = open("WEATHER_OUT", "w")
gameLoop = 200
firstWeather = random.randint(1, 3)
match firstWeather:
    case 1:  # cloudy
        weatherOut.write("C")
        currentWeather = 'C'
    case 2:  # plain
        weatherOut.write("P")
        currentWeather = 'P'
    case _:  # hot
        weatherOut.write("H")
        currentWeather = 'H'
gameOut.write(getGame(currentWeather))
for i in range(gameLoop - 1):
    currentWeather = getWeather(currentWeather)
    weatherOut.write(currentWeather)
    gameOut.write(getGame(currentWeather))
weatherOut.close()
gameOut.close()
HMM()
getAccuracy()
