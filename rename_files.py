import os
import pandas as pd

DIRECTORY = "Data"

# files = os.listdir(DIRECTORY)
# for file in files:
#     if not file.endswith('.json'):
#         files.remove(file)
# intv = 82
# for file in files:
#     print(type(file))
#     os.rename(DIRECTORY + "/" +file, DIRECTORY + "/" + str(intv)+".json")
#     intv += 1
files = os.listdir(DIRECTORY)
for file in files:
        if not file.endswith('.json'):
            files.remove(file)
game_id = set()
c = 0
for file in files:
    # print(file)
    df = pd.read_json(DIRECTORY + "/" + file)
    # print(df)
    # print(df['gameId'][0])
    if df['gameId'][0] not in game_id:
        game_id.add(df['gameId'][0])
    else:
        print(file)
        os.remove(DIRECTORY + "/"+file)
    # print(game_id)