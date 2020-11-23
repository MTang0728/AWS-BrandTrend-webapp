from flask import Flask, render_template
import pandas as pd
import boto3

# EB looks for an 'application' callable by default.
application = Flask(__name__)

bucket = "brandtrend"
file_name = "2020-11-22_The North Face.csv"

s3 = boto3.client('s3') 
# 's3' is a key word. create connection to S3 using default config and all buckets within S3

obj = s3.get_object(Bucket= bucket, Key= file_name) 

# get object and file (key) from bucket

initial_df = pd.read_csv(obj['Body']) # 'Body' is a key word
records = tuple(initial_df.to_records(index=False))
headings = ('Date','Trend')

@application.route("/")
def table():
    return render_template("table.html",headings=headings,data=records)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(host='0.0.0.0',port=8080)