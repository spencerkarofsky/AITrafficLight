"""
Traffic Sign Class
"""
import pandas as pd
import random
import time

class TrafficSign:
    # Variables and Constants:

    # LED pins
    # reds = [None,None,None,None]
    # greens = [None, None, None, None]
    # yellows = [None, None,None,None]

    # Constants
    VEHICLE_TIME_CONSTANT = 2  # time, in seconds, per vehicle, of green light time

    '''
    
    '''
    # Constructor
    def __init__(self):
        dataframe_columns = ['Date/Time', 'Side 1', 'Side 2', 'Side 3', 'Side 4']
        self.traffic_dataframe = pd.DataFrame(columns=dataframe_columns)
        green_light_list = []

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
    '''
    get_green_light_time()
    Inputs: street, the string value for street (either 1 or 2)
    Returns: green_light_time, the amount of time, in seconds, for the green light
    Calculates the time for a green light based on the average amount of vehicles between both sides of a street, then multiplies this value by a constant.
    '''
    def get_green_light_time(self,street):
        # Green light time = a constant * the average number of vehicles on a given street
        if street == 'Street 1':
            green_light_time = self.VEHICLE_TIME_CONSTANT * ((self.traffic_dataframe.iloc[-1,1] + self.traffic_dataframe.iloc[-1,3]) / 2)
        elif street == 'Street 2':
            green_light_time = self.VEHICLE_TIME_CONSTANT * ((self.traffic_dataframe.iloc[-1, 3] + self.traffic_dataframe.iloc[-1, 4]) / 2)
        else:
            green_light_time = 0
        return green_light_time

    '''
    set_green_light()
    Inputs: street (the street), t (time, in seconds)
    Returns: none
    Sets street's light to green for t seconds
    '''
    def set_green_light(self,street,t):
        self.green_light_list.append(street)

    '''
    set_yellow_light()
    Inputs: street (the street), t (time, in seconds)
    Returns: none
    Sets street's light to yellow for 3 seconds
    '''
    def set_yellow_light(self,street,t=3):
        pass

    '''
    set_red_light()
    Inputs: street (the street)
    Returns: none
    Sets street's light to red
    '''
    def set_red_light(self,street):
        pass

    '''
    set_flash_red()
    Inputs: street (the street), t (time, in seconds)
    Returns: none
    Sets street's light to flash red
    '''
    def set_flash_red(self,street):
        pass

    '''
    get_last_green()
    Inputs: none
    Returns: last_street_green, the last street to have a green light
    Used to determine which street gets the green light when they have equal traffic
    '''
    def get_last_green(self):
        # The last street with the green light is the last item (street) on the green light list
        last_street_green = self.green_light_list[-1]
        return last_street_green

    '''
    set_traffic_light()
    Inputs: none
    Returns: none
    Controls the traffic light lights based on the following logic:
    
    * Do all streets have less than 2 cars?
        * Yes: Both streets flash red light; intersection will function as a 4-way stop
        * No:
            * Compare traffic ratio between the two streets (ratio < 1: Street 2 has more traffic than Street 1; ratio > 1: Street 1 has more traffic than Street 2)
            * Is ratio < 1?
                * Street 1 (Sides 1 & 3) get green light; Street 2 (Sides 2 & 4) get red light.
            * Is ratio > 1:
                * Street 2 gets green light; Street 1 gets red light
            * Does ratio = 1 (both streets have the same amount of traffic)?
                * Is there an existing data row other than the current one (is this not the first iteration of the while true loop)?
                    * Yes: Randomly select one street to start with the green light and the other will start with red light.
                    * No: The street that previously had a green light will now have a red light, and the other street gets red light
    '''
    def set_traffic_lights(self):
        # Case 1: All sides have less than 2 cars; intersection will act as a 4-way stop.
        if self.traffic_dataframe.iloc[-1, 1] <= 2 and self.traffic_dataframe.iloc[-1, 2] <= 2 and self.traffic_dataframe.iloc[-1, 3] <= 2 and self.traffic_dataframe.iloc[-1, 4] <= 2:
            # turn all greens and yellows off; all reds  blink to signal 4-way stop
            self.set_flash_red('Street 1')
            self.set_flash_red('Street 2')
        # Case 2: some sides have more than 2 cars, so the ratio between the 2 streets will be calculated using the calculate_traffic_ratio function.
        # That ratio will then be used to determine the timing of the lights.
        else:
            ratio = self.calculate_traffic_ratio(self.traffic_dataframe.iloc[-1])
            # Case A: Street 2 has more traffic than Street 1; Street 2 gets green light priority
            if ratio < 1:
                # Green light time = a constant * the average number of vehicles on a given street
                green_light_time = self.get_green_light_time('Side 2')

                # Set street 2 lights (green[1] and green[3]) to green and street 1 lights to red.

            # Case B: Street 1 has more traffic than Street 2; Street 1 gets green light priority.
            elif ratio > 1:
                # Green light time = a constant * the average number of vehicles on a given street
                green_light_time = self.get_green_light_time('Side 2')

                # Set street 1 lights (green[0] and green[2]) to green and street 2 lights to red.

            else:
                # The streets have equal traffic amounts.

                # If traffic_dataframe row is first row, randomly select street to get green light priority
                current_row_index = self.traffic_dataframe.index.get_loc(
                    self.traffic_dataframe.index[0])
                if current_row_index == 0:
                    random_street = random.randint(1, 2)
                    if random_street == 1:
                        # Street 1 gets green light priority
                        green_light_time = self.get_green_light_time('Side 1')
                        # Set green and red lights
                    else:
                        # Street 2 gets green light priority
                        green_light_time = self.get_green_light_time('Side 2')
                        # Set green and red lights
                # Else, give green light priority to the last street to have red light.
                else:
                    if (self.traffic_dataframe.iloc[-2, 1] + self.traffic_dataframe.iloc[-2, 3]) > (
                            self.traffic_dataframe.iloc[-2, 2] + self.traffic_dataframe.iloc[-2, 4]):
                        pass
                    else:
                        street_green = self.get_last_green()
                        self.set_green_light(street_green)
                        if street_green == 'Street 1':
                            self.set_red_light('Street 2')
                        else:
                            self.set_red_light('Street 1')
