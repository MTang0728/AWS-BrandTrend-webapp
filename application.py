from flask import Flask, render_template
import numpy as np
import pandas as pd
import boto3
import matplotlib.pyplot as plt
from datetime import date

# EB looks for an 'application' callable by default.
application = Flask(__name__)

bucket = "brandtrend"

s3 = boto3.client('s3') 

###
# 's3' is a key word. create connection to S3 using default config and all buckets within S3
# get all items in the bucket
all_responses = s3.list_objects_v2(Bucket= bucket)
# information stored in 'Contents', file name stored in 'Keys'
brands_with_all_dates= [item['Key'] for item in all_responses['Contents']]
# get unique dates and store as list
dates = set([item[:10] for item in brands_with_all_dates])
dates = list(dates)

# define a function that fetches trends based on chosen date
def get_trends(date):
    response = s3.list_objects_v2(Bucket= bucket, Prefix = date)
    brands_with_date= [item['Key'] for item in response['Contents']]
    # define an empy list to store brand names
    brands = []
    # create an empty dataframe to store trends data
    trends_df = pd.DataFrame(columns = ['date'])
    # loop through file names 
    for brand in brands_with_date:
        # get brand name and update the brand name list
        brand_name = brand[11:-4]
        brands.append(brand_name)
        # read the csv file as a dataframe
        obj = s3.get_object(Bucket= bucket, Key= brand) 
        temp_df = pd.read_csv(obj['Body'])
        # merge dataframe
        trends_df = pd.merge(trends_df, temp_df, on = 'date', how = 'outer')
        pass
    # set date as index
    trends_df = trends_df.set_index('date')
    # safe a copy of data for visualization
    full_df = trends_df.copy()
    # transpose so date is used as column
    trends_df = trends_df.transpose()
    
    # create headings
    headings = trends_df.columns.values[:]
    # only use month, day, time for headings
    headings = list([item[5:] for item in headings])
    # change the index used in full_df
    full_df.index = np.array(headings)
    # add a placeholder for 'Brands'
    headings.insert(0, 'Brands')
    headings = tuple(headings)
    # get brand names as part of records
    trends_df = trends_df.reset_index()
    # save as a tuple of records
    records = tuple(trends_df.to_records(index = False))
    # return data
    return records, headings, full_df

# define a function to plot data
def plot_trend(data):
    plt.figure(figsize= (40, 10))
    plt.plot(data.iloc[:, :5])
    plt.legend(labels = data.columns.values[:5])
    plt.xticks(rotation = 'vertical')
    plt.tight_layout()
    plt.savefig('./static/trend.png', bbox_inches = "tight")

# get today's date
today = date.today().strftime('%Y-%m-%d')
# check if today's data is collected in S3
if today in dates:
    records, headings, full_data = get_trends(today)
    plot_trend(full_data)
    pass
else:
    headings = ('Brands', 'Time')
    data = ('Not Available Yet', 'Not Available Yet')

@application.route("/")
def table():
    return render_template("display.html",headings=headings,data=records, date = today)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='0.0.0.0',port=8080)