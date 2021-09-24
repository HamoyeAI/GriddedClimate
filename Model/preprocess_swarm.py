import pandas as pd
import numpy as np
import datetime


class ConvertoDatetime():

    def __init__ (self, dataframe = None):
        self.dataframe = dataframe

    def convert(self):
        swarm_data = pd.read_excel(self.dataframe)
        swarm_data['STARTDATE'] = pd.to_datetime(swarm_data['STARTDATE']).apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        swarm_data['FINISHDATE'] = pd.to_datetime(swarm_data['FINISHDATE']).apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        swarm_data['STARTDATE'] = pd.to_datetime(swarm_data['STARTDATE'])
        swarm_data['FINISHDATE'] = pd.to_datetime(swarm_data['FINISHDATE'])

        swarm_data['TmSTARTDAT'] = pd.to_datetime(swarm_data['TmSTARTDAT']).apply(lambda x: x.strftime('%H:%M:%S'))
        swarm_data['TmFINISHDA'] = pd.to_datetime(swarm_data['TmFINISHDA']).apply(lambda x: x.strftime('%H:%M:%S'))

        swarm_data['CTLSTDATE'] = pd.to_datetime(swarm_data['CTLSTDATE']).apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        swarm_data['CTLFNDATE'] = pd.to_datetime(swarm_data['CTLFNDATE']).apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        swarm_data['CTLSTDATE'] = pd.to_datetime(swarm_data['CTLSTDATE'])
        swarm_data['CTLFNDATE'] = pd.to_datetime(swarm_data['CTLFNDATE'])
        return swarm_data


class SelectGridSquares():

    def __init__ (self, new_dataframe=None, countrycode=None):
        self.new_dataframe = new_dataframe
        self.countrycode = countrycode

    def selectdf(self):
        dataset = self.new_dataframe[['X', 'Y', 'STARTDATE', 'COUNTRYID', 'LOCPRESENT', 'Rainfall_Value']]
        dataset_df = dataset[dataset['COUNTRYID']== self.countrycode]
        locust_present = dataset_df[dataset_df['LOCPRESENT'] == 1]
        new_locust_data = locust_present.groupby(['STARTDATE', 'COUNTRYID']).LOCPRESENT.count().reset_index()
        return new_locust_data



# if __name__ == "__main__":
#     new_dataframe = SelectGridSquares(dataframe = swarms_df, countrycode = 'ET')
#     new_dataf = new_dataframe.selectdf()

# new_dataf