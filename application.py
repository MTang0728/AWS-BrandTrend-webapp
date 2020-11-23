from flask import Flask, render_template
import pandas as pd
import boto3

# EB looks for an 'application' callable by default.
application = Flask(__name__)

bucket = "brandtrend"
file_name = "2020-11-22_Lululemon.csv"

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
    # save as a tuple of records
    records = tuple(trends_df.to_records(index = False))
    # create headings
    headings = brands[:]
    headings.insert(0, 'Date')
    headings = tuple(headings)
        
    return records, headings
    
# using '2020-11-23' as a sample
records, headings = get_trends('2020-11-23')

@application.route("/")
def table():
    return render_template("display.html",headings=headings,data=records)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='0.0.0.0',port=8080)