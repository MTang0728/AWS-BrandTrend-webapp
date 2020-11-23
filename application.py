from flask import Flask, render_template
import pandas as pd
import boto3

# EB looks for an 'application' callable by default.
application = Flask(__name__)

bucket = "brandtrend"
file_name = "2020-11-22_Lululemon.csv"

s3 = boto3.client('s3') 
# 's3' is a key word. create connection to S3 using default config and all buckets within S3

obj = s3.get_object(Bucket= bucket, Key= file_name) 


###
date = '2020-11-23'
response = s3.list_objects_v2(Bucket= bucket, Prefix = date)

brands_with_date= [item['Key'] for item in response['Contents']]

brands = []
trends_df = pd.DataFrame(columns = ['date'])
for brand in brands_with_date:
    brand_name = brand[11:-4]
    brands.append(brand_name)
    
    obj = s3.get_object(Bucket= bucket, Key= brand) 
    temp_df = pd.read_csv(obj['Body'])
    trends_df = pd.merge(trends_df, temp_df, on = 'date', how = 'outer')
    
# trends_df.set_index('date', inplace = True)
# trends_df = trends_df.transpose()
records = tuple(trends_df.to_records(index = False))
headings = brands[:]
headings.insert(0, 'Date')
headings = tuple(headings)
print(headings)

###

# get object and file (key) from bucket

# initial_df = pd.read_csv(obj['Body']) # 'Body' is a key word
# records = tuple(initial_df.to_records(index=False))
# headings = ('Date','Trend')

@application.route("/")
def table():
    return render_template("display.html",headings=headings,data=records)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='0.0.0.0',port=8080)