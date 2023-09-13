"""
Traffic Sign Class
"""
import pandas as pd
import queue

class TrafficSign:
    # Variables and Constants:

    # LED pins
    # reds = [None,None,None,None]
    # greens = [None, None, None, None]
    # yellows = [None, None,None,None]

    # Constants
    LIGHT_CONSTANT = 2  # time, in seconds, per vehicle, of green light time

    # Constructor
    def __int__(self):
        dataframe_columns = ['Date/Time', 'Side 1', 'Side 2', 'Side 3', 'Side 4']
        self.traffic_dataframe = pd.DataFrame(columns=dataframe_columns)

    # Methods

    '''
    append_data_row()
    Inputs: data_row
    Returns: none
    This method adds a data row containing the date/time, and amount of vehicles for each street.
    '''
    def append_data_row(self,data_row):
        # Add the new data as a row to the DataFrame
        self.traffic_dataframe.loc[len(self.traffic_dataframe)] = data_row

    '''
    calculate_traffic_ratio()
    This function calculates the 2 average traffic amounts for the 2 street pairs and then returns a ratio of Sides 1 & 3 to Sides 2 & 4.
    Inputs: data_row, a list where elements 1-4 are the 4 amounts of detected vehicles for each corresponding street.
    Returns: ratio, the ratio of Street 1 to Street 2
    Compares the amount of vehicles on the roads. Sides 1 & 3 are opposite sides of the same street; same with Sides 2 & 4.
    '''
    def calculate_traffic_ratio(self,data_row):
        # Calculate the average traffic amount for both streets
        street_1_average = (data_row[1] + data_row[3]) / 2
        street_2_average = (data_row[2] + data_row[4]) / 2
        ratio = street_1_average / street_2_average
        return ratio

    '''
    calculate_total_vehicles()
    Inputs: None
    Returns: vehicles, the total number of vehicles detected on the road.
    Calculates the total amount of vehicles on the road.
    '''
    def calculate_total_vehicles(self,data_row):
        # Calculate the average traffic amount for both streets
        vehicles = data_row[1] + data_row[2] + data_row[3] + data_row[4]
        return vehicles


