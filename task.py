import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Ask the user to choose the plot to generate(0 for charging station occupancy plot, 1 for power demand plot)
user_input = input("Enter 0 to generate the charging station occupancy plot, 1 to generate the power demand plot: ")

#Load the Excel file
file_path = './ChargingStationData.xlsx'
df = pd.read_excel(file_path)

#Time range with 1 minute interval for the whole day
time_range = pd.date_range(start='2022-07-01 00:00', end='2022-07-01 23:59', freq='min')

#Define constant charging power and total number of charging points
charging_power = 11 #in kw
total_charging_points = 6

#Initialize arrays to store the occupancy of the charging points and power demand for each minute
occupancy = np.zeros(len(time_range)) #0 means the charging point is available and 1 means the charging point is occupied
power_demand = np.zeros(len(time_range))

#Iterate over each vehicle and mark occupancy
for index, row in df.iterrows():
    #Get the arrival and departure time of the vehicle
    arrival_time = pd.to_datetime(row['TimeOfArrival'])
    departure_time = pd.to_datetime(row['TimeOfDeparture'])
    
    #Get the initial SOC and battery capacity of the vehicle
    soc = row['VehicleInitialSoC']
    battery_capacity = row['VehicleBatteryCapacity']

    #Calculte the index of the arrival and departure time in the time_range
    arrival_index = time_range.get_loc(arrival_time)
    departure_index = time_range.get_loc(departure_time)


    #Simulate the charging process for each minute until SOC reaches 90% or departure time is reached
    for minute in range(arrival_index, departure_index):
        #If SOC is less than 90%, charge the vehicle
        if soc < 90:
            soc += ((charging_power/60)/battery_capacity)*100
            occupancy[minute] += 1
            power_demand[minute] += charging_power
        else:
            #If SOC reaches 90%, stop charging
            break

# Generate the plot based on user input
if user_input == '0':
    # Plot the occupancy over the day
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.scatter(time_range, occupancy, label="Occupancy", color='blue', s=1)
    ax.set_title('Charging Station Occupancy')
    
    # Set the y-axis limit to the total number of charging points
    ax.set_ylim(0, total_charging_points)

    # Format the x-axis to display hours and minutes
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim([pd.to_datetime('2022-07-01 00:00'), pd.to_datetime('2022-07-01 23:59')])

    # Set the labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Occupancy')
    plt.tight_layout()
    plt.show()

elif user_input == '1':
    # Plot the occupancy over the day
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.scatter(time_range, power_demand, label="Power Demand", color='green', s=1)
    ax.set_title('Charging Station Power Demand in kW')
    
    # Set the y-axis limit to the total number of charging points*charging power
    ax.set_ylim(0, total_charging_points*charging_power)

    # Format the x-axis to display hours and minutes
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim([pd.to_datetime('2022-07-01 00:00'), pd.to_datetime('2022-07-01 23:59')])

    # Set the labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Power Demand in kW')
    plt.tight_layout()
    plt.show()

else:
    #If the user input is invalid, print an error message
    print("Invalid input. Please enter 0 or 1")
