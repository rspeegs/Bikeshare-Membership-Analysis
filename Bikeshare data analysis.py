import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

#___________________________________________
#                       DATA

df_2025_07 = pd.read_csv("202507-divvy-tripdata.csv") # July 2025
df_2025_08 = pd.read_csv("202508-divvy-tripdata.csv") # August 2025
df_2025_09 = pd.read_csv("202509-divvy-tripdata.csv") # September 2025
df_2025_10 = pd.read_csv("202510-divvy-tripdata.csv") # October 2025
df_2025_11 = pd.read_csv("202511-divvy-tripdata.csv") # November 2025
df_2025_12 = pd.read_csv("202512-divvy-tripdata.csv") # December 2025
df_2026_01 = pd.read_csv("202601-divvy-tripdata.csv") # January 2026
df_2026_02 = pd.read_csv("202602-divvy-tripdata.csv") # February 2026
df_2026_03 = pd.read_csv("202603-divvy-tripdata.csv") # March 2026
df_2026_04 = pd.read_csv("202604-divvy-tripdata.csv") # April 2026
df_2026_05 = pd.read_csv("202605-divvy-tripdata.csv") # May 2026
df_2026_06 = pd.read_csv("202606-divvy-tripdata.csv") # June 2026
df_2026_07 = pd.read_csv("202607-divvy-tripdata.csv") # July 2026

#_____________________________________________

#print(set(df["rideable_type"]))
#print(set(df["member_casual"]))

def find_rider_counts(dataframe):
    total_rider_count = 0
    casual_rider_count = 0
    member_rider_count = 0

    for rider in dataframe["member_casual"]:
        if rider == "member" or rider == "casual":
            total_rider_count += 1
        if rider == "member":
            member_rider_count += 1
        if rider == "casual":
            casual_rider_count += 1

    percentage_of_member_riders = round((member_rider_count / total_rider_count) * 100, 4)
    percentage_of_casual_riders = round((casual_rider_count / total_rider_count) * 100, 4)

    return [total_rider_count, member_rider_count, casual_rider_count, percentage_of_member_riders, percentage_of_casual_riders]

def find_average_time_biking(dataframe):
    dataframe["started_at"] = pd.to_datetime(dataframe["started_at"])
    dataframe["ended_at"] = pd.to_datetime(dataframe["ended_at"])
    dataframe["duration"] = dataframe["ended_at"] - dataframe["started_at"]

    casual_riders = dataframe[dataframe["member_casual"] == "casual"]
    member_riders = dataframe[dataframe["member_casual"] == "member"]

    average_time_biking_casual = str(casual_riders["duration"].mean())
    average_time_biking_member = str(member_riders["duration"].mean())

    return [average_time_biking_casual, average_time_biking_member]

def coordinates_to_distance(start_latitude, end_latitude, start_longitude, end_longitude, is_degrees = True, in_km = False):

    """
    Returns the distance between 2 points on earth using the Haversine formula
    Assumes earth is perfect sphere (not as accurate since earth is ovoid)
    Can take either degree or radian coordinates, but units must match
    """

    R_km = 6371
    R_mi = 3959

    if is_degrees:
        start_latitude = start_latitude * (math.pi / 180.0)
        start_longitude = start_longitude * (math.pi / 180.0)
        end_latitude = end_latitude * (math.pi / 180.0)
        end_longitude = end_longitude * (math.pi / 180.0)

    a = math.sin((end_latitude - start_latitude) / 2)**2 + math.cos(start_latitude) * math.cos(end_latitude) * math.sin((end_longitude - start_longitude) / 2)**2
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))

    if not in_km:
        return R_mi * c
    else:
        return R_km * c

def find_average_distance_biking(dataframe):
    dataframe["start_lat"] = pd.to_numeric(dataframe["start_lat"])
    dataframe["end_lat"] = pd.to_numeric(dataframe["end_lat"])

    dataframe["start_lng"] = pd.to_numeric(dataframe["start_lng"])
    dataframe["end_lng"] = pd.to_numeric(dataframe["end_lng"])

    dataframe["distance"] = dataframe.apply(lambda x: coordinates_to_distance(x["start_lat"], x["end_lat"], x["start_lng"], x["end_lng"]), axis=1)

    casual_riders = dataframe[dataframe["member_casual"] == "casual"]
    member_riders = dataframe[dataframe["member_casual"] == "member"]

    average_distance_biking_casual = float(casual_riders["distance"].mean())
    average_distance_biking_member = float(member_riders["distance"].mean())
    

    return [round(average_distance_biking_casual, 5), round(average_distance_biking_member, 5)]


#testing
print(find_rider_counts(df_2025_10))
print(find_average_distance_biking(df_2026_01))
print(find_average_time_biking(df_2026_05))