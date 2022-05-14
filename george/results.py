import pandas as pd
import datetime
import pickle
import json
from sklearn.preprocessing import MinMaxScaler

MODELS = {'HA': '../data/HA_xgb.sav',
         'NK': '../data/NK_xgb.sav',
         'AA': '../data/AA_xgb.sav',
         'UA': '../data/UA_xgb.sav',
         'AS': '../data/AS_xgb.sav',
         'DL': '../data/DL_xgb.sav',
         'G4': '../data/G4_xgb.sav',
         'WN': '../data/WN_xgb.sav',
         'VX': '../data/VX_xgb.sav',
         'B6': '../data/B6_xgb.sav',
         'F9': '../data/F9_xgb.sav'}

MODELS = {'HA': '../data/HA_linreg.sav',
          'NK': '../data/NK_linreg.sav',
          'AA': '../data/AA_linreg.sav',
          'UA': '../data/UA_linreg.sav',
          'AS': '../data/AS_linreg.sav',
          'DL': '../data/DL_linreg.sav',
          'G4': '../data/G4_linreg.sav',
          'WN': '../data/WN_linreg.sav',
          'VX': '../data/VX_linreg.sav',
          'B6': '../data/B6_linreg.sav',
          'F9': '../data/F9_linreg.sav',
          }


def prepare(time, airline, airtime, origin, distance):
    airport = 1
    origin_name = 'origin_' + str(origin)
    cols = ['departing_in_sec', origin_name, 'distance', 'crs_elapsed_time']
    df = pd.DataFrame(columns=cols)
    df.loc[0] = time, airport, distance, airtime
    print(df)
    return {airline: df}


def pre_populate(data_predict, airline):
    """Assuming Init Model seen all the columns"""
    with open('../data/data_records.json') as f:
        records = json.load(f)
    dict_df = {}
    x_cur = data_predict[airline]
    init_col = records[airline]
    curr_cols = x_cur.columns.to_list()
    missing_cols = set(init_col) - set(curr_cols)
    i = 0
    for col in missing_cols:
        i += 1
        print(i)
        x_cur[col] = 0
    x = x_cur.reindex(columns=init_col)
        # SCALER SCALES TO 0 BECAUSE ITS JUST ONE ROW
        # scaler_ = MinMaxScaler()
        # x_scaled = scaler_.fit_transform(x)
        # print(x_scaled)
        # X = pd.DataFrame(x_scaled, columns=x.columns)
        # –––––––––––––––––––––––––––––––––––––––––––––
    dict_df[airline] = x
    print(x)
    return dict_df


def predict(time, airline, airtime, origin, distance):
    df_1 = prepare(time, airline, airtime, origin, distance)
    df = pre_populate(df_1, airline)
    # loaded_model
    loaded_model = pickle.load(open(MODELS[airline], 'rb'))
    prediction = loaded_model.predict(df[airline])
    print(f'Approximate arrival delay is {prediction[0]}')
    return prediction[0]


df = predict(15300, 'AA', 123, 'ATL', 500)
# 76320 AA 123 origin_ATL 500
# 15300 AA 120 origin_ATL 500