from flask import Flask, render_template
import pandas as pd
import datetime
from datetime import timedelta, datetime

app = Flask(__name__)

@app.route("/")
def home():
    currently_down, recently_down, flapping = get_data()
    return render_template("home.html", currently_down=currently_down, recently_down=recently_down, flapping=flapping)



def get_data():
    current_time = datetime.strptime("2019-07-06 22:18:00", '%Y-%m-%d %H:%M:%S')
    outages_df = pd.read_json(path_or_buf="outages.json", orient="records")
    outages_df["startTime"] = pd.to_datetime(outages_df["startTime"], infer_datetime_format=True)
    outages_df["duration"] = pd.to_timedelta(outages_df["duration"], unit="minute")
    currently_down = get_currently_down_services(current_time, outages_df)
    recently_down = get_recently_down_services(current_time, outages_df)
    flapping = get_flapping_services(current_time, outages_df)

    return currently_down, recently_down, flapping


def get_currently_down_services(current_time, outages_df):
    currently_down = outages_df.loc[(outages_df["startTime"] >= (current_time - timedelta(minutes=2))) &
    (outages_df["startTime"] <= current_time)].copy()
    currently_down["endTime"] = currently_down["startTime"] + currently_down["duration"]
    if currently_down.empty:
        return build_empty_table("id", "startTime", "duration", "endTime")
    else:

        return currently_down.to_html(index=False)


def get_recently_down_services(current_time, outages_df, interval=15):
    recently_down = outages_df.loc[(outages_df["startTime"] <= current_time) & (outages_df["startTime"] >=
        (current_time + timedelta(minutes=interval)))].copy()
    recently_down["endTime"] = recently_down["startTime"] + recently_down["duration"]
    if recently_down.empty:
        return build_empty_table("id", "startTime", "duration", "endTime")
    else:
        return recently_down.to_html(index=False)


def get_flapping_services(current_time, outages_df):
    # flapping = outages_df.loc[outages_df["startTime"] >= current_time - timedelta(minutes=180)].copy()
    # flapping["amountOfOutages"] = 1
    # flapping["sumOfOutages"] = flapping["duration"]
    # flapping["endTime"] = flapping["startTime"] + flapping["duration"]
    # flapping = flapping.groupby(["service"], as_index=False).agg({"id": "last", "startTime": "last", "duration": "last",
    #     "sumOfOutages": "sum", "amountOfOutages": "count"})
    # flapping = flapping.loc[flapping["sumOfOutages"] >= timedelta(minutes=15)].copy()

    flapping = pd.DataFrame()
    if flapping.empty:
        return build_empty_table("id", "startTime", "duration", "endTime", "sumOfOutages", "amountOfOutages")
    else:
        return flapping.to_html(index=False)


def build_empty_table(*args):
    d = pd.DataFrame(0, index=[0], columns=list(args))
    return d.to_html(index=False)


if __name__ == "__main__":
    app.run(debug=True)