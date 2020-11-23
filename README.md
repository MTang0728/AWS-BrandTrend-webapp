# AWS-BrandTrend0-webapp

![shopping](shopping.jpg)

## Introduction
Welcome to our **Brand Trend WebApp** project. This is the final project of the course IDS 706 - Data Engineering Systems of Duke University. My teammate is [Chenxi Wu](https://www.linkedin.com/in/chenxi-wu-107452175/).  

We built an integrated data pipeline as well as an interactive WebApp to display our result. The main tools we used are Amazon DynamoDB, SQS AWS S3 buckets and Flask. 

We were inspired by the biggest Chinese shopping-guide platform in North America, [Dealmoon](https://www.dealmoon.com/). The website hosts tons of posts that share the newest deal information across the internet. It also has a product leader board that records the real-time most popular items across the site. These brands are being searched everyday on Google, where [Google trends](https://trends.google.com/trends/) keeps the record of these searches. It would be informative to know the most popular items on Dealmoon as well as the search trend of this brand recently, thus to make better decision on what to buy. 

## Flowchart
The process and flowchart of building this project can be summarized as below. 

(insert the picture)

### Web-scraping from Dealmoon

There are many sections on Dealmoon that contain useful information. For example the homepage where all the shopping-guide posts are held. After examining each section, we decided to scrape the product leaderboard. 





