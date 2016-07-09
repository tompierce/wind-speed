import datetime

LIMIT_DATE_RANGE = True

def extract_data(json_obj):
    end_date_time = datetime.datetime.strptime(json_obj["windspeedMean"][-1]["date"], "%Y-%m-%d %H:%M:%S" )
    start_date_time = datetime.datetime.strptime(json_obj["windspeedMean"][0]["date"], "%Y-%m-%d %H:%M:%S" )

    if LIMIT_DATE_RANGE: # limit date range from midnight to midnight
        today = datetime.datetime.today()
        end_date_time = min(end_date_time, datetime.datetime(today.year, today.month, today.day))
        start_date_time = max(start_date_time, end_date_time - datetime.timedelta(days=1))

    mean_datapoints = []
    max_datapoints = []

    _extract_data_set(json_obj["windspeedMean"], start_date_time, end_date_time, mean_datapoints)
    _extract_data_set(json_obj["windspeedMax"], start_date_time, end_date_time, max_datapoints)

    return {"mean": mean_datapoints, "max": max_datapoints}


def _extract_data_set(json_list, start_date_time, end_date_time, result):
    for data_point in json_list:
        date_time = datetime.datetime.strptime(data_point["date"], "%Y-%m-%d %H:%M:%S" )
        speed = data_point["speed"]
        if start_date_time <= date_time <= end_date_time:
            result.append({"timestamp":date_time, "speed": speed})


def make_report(obj):
   
    interval_in_mins = 10    
    windspeedLimits = [
                    {'limit': 35.0, 'time_above': 0, 'gusts': 0}, 
                    {'limit': 45.0, 'time_above': 0, 'gusts': 0}, 
                    {'limit': 50.0, 'time_above': 0, 'gusts': 0}, 
                    {'limit': 65.0, 'time_above': 0, 'gusts': 0}, 
                    {'limit': 80.0, 'time_above': 0, 'gusts': 0}
                  ]

    end_date_time = datetime.datetime.strptime(obj["windspeedMean"][-1]["date"], "%Y-%m-%d %H:%M:%S" )
    start_date_time = datetime.datetime.strptime(obj["windspeedMean"][0]["date"], "%Y-%m-%d %H:%M:%S" )

    if LIMIT_DATE_RANGE: # limit date range from midnight to midnight
        today = datetime.datetime.today()
        end_date_time = min(end_date_time, datetime.datetime(today.year, today.month, today.day))
        start_date_time = max(start_date_time, end_date_time - datetime.timedelta(days=1))
             
    for windspeed_mean_datapoint in obj["windspeedMean"]:
        date_time = datetime.datetime.strptime(windspeed_mean_datapoint["date"], "%Y-%m-%d %H:%M:%S" )
        speed = windspeed_mean_datapoint["speed"]
        if start_date_time <= date_time <= end_date_time:
            for x in windspeedLimits:
                if speed > x['limit']:
                    x['time_above'] += interval_in_mins
    max_speed = 0
    for windspeed_max_datapoint in obj["windspeedMax"]:
        date_time = datetime.datetime.strptime(windspeed_max_datapoint["date"], "%Y-%m-%d %H:%M:%S" )
        speed = windspeed_max_datapoint["speed"]
        if start_date_time <= date_time <= end_date_time:
            max_speed = max(max_speed, speed)
            for x in windspeedLimits:
                if speed > x['limit']:
                    x['gusts'] += 1
       
    report_output = ""
    report_output += "---- Windspeed Report ----\n"
    report_output += str(start_date_time) + " - " + str(end_date_time) + "\n\n"

    for x in xrange(0, len(windspeedLimits)):
        a = windspeedLimits[x]
        report_output += "Mean wind speed on the bridge was above Limit " + str(x+1) + " (" + str(a['limit']) + " mph) for " + str(round(a['time_above']/60.0, 1)) + " hours\n"
        report_output += "Gusting above Limit " + str(x+1) + " (" + str(a['limit']) + " mph) on " + str(a['gusts']) + " occasions\n\n"
    
    report_output += "Max wind speed during this time period: " + str(max_speed) + " mph"
    
    return report_output
