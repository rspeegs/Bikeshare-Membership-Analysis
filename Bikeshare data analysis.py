import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

#___________________________________________
#                       DATA

df = pd.read_csv("202507-divvy-tripdata.csv") # July 2025
#df = pd.read_csv("202508-divvy-tripdata.csv") # August 2025
#df = pd.read_csv("202509-divvy-tripdata.csv") # September 2025
#df = pd.read_csv("202510-divvy-tripdata.csv") # October 2025
#df = pd.read_csv("202511-divvy-tripdata.csv") # November 2025
#df = pd.read_csv("202512-divvy-tripdata.csv") # December 2025
#df = pd.read_csv("202601-divvy-tripdata.csv") # January 2026
#df = pd.read_csv("202602-divvy-tripdata.csv") # February 2026
#df = pd.read_csv("202603-divvy-tripdata.csv") # March 2026
#df = pd.read_csv("202604-divvy-tripdata.csv") # April 2026
#df = pd.read_csv("202605-divvy-tripdata.csv") # May 2026
#df = pd.read_csv("202606-divvy-tripdata.csv") # June 2026
#df = pd.read_csv("202607-divvy-tripdata.csv") # July 2026

#_____________________________________________

#print(set(df["rideable_type"]))
#print(set(df["member_casual"]))

total_rider_count = 0
casual_rider_count = 0
member_rider_count = 0
for rider in df["member_casual"]:
    total_rider_count += 1
    if rider == "member":
        member_rider_count += 1
    if rider == "casual":
        casual_rider_count += 1

print(f"Total # of Riders: {total_rider_count}")
print(f"# of Member Riders: {member_rider_count}\n# of Causal Riders: {casual_rider_count}")
print(f"Percentage of Member Riders: {(member_rider_count / total_rider_count):.2%}")
print(f"Percentage of Casual Riders: {(casual_rider_count / total_rider_count):.2%}\n")

#TODO: Examine the average length (time and distance) of bike trips for both member types

df["started_at"] = pd.to_datetime(df["started_at"])
df["ended_at"] = pd.to_datetime(df["ended_at"])
df["duration"] = df["ended_at"] - df["started_at"]

df["start_lat"] = pd.to_numeric(df["start_lat"])
df["end_lat"] = pd.to_numeric(df["end_lat"])

df["start_lng"] = pd.to_numeric(df["start_lng"])
df["end_lng"] = pd.to_numeric(df["end_lng"])


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

df["distance"] = df.apply(lambda x: coordinates_to_distance(x["start_lat"], x["end_lat"], x["start_lng"], x["end_lng"]), axis=1)

casual_riders = df[df["member_casual"] == "casual"]
member_riders = df[df["member_casual"] == "member"]

casual_rider_duration_avg = casual_riders["duration"].mean()
member_rider_duration_avg = member_riders["duration"].mean()


casual_rider_distance_avg = casual_riders["distance"].mean()
member_rider_distance_avg = member_riders["distance"].mean()

print(f"Average casual rider duration: {casual_rider_duration_avg}")
print(f"Average member rider duration: {member_rider_duration_avg}\n")

print(f"Average distance travelled by casual riders: {casual_rider_distance_avg:.4f}")
print(f"Average distance travelled by member riders: {member_rider_distance_avg:.4f}")