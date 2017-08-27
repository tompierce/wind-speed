from __future__ import print_function
import json
import base64, urllib, urllib2
import datetime
import boto3
import wind.wind_speed_report as wind_speed
import wind.wind_speed_data as spreadsheet
from config import MAIL_GUN_URL, MAIL_GUN_API_KEY, RECIPIENT_EMAIL, BUCKET_NAME


def lambda_handler(event, context):
    log('Initialising')

    report_id = str(datetime.datetime.today().date() - datetime.timedelta(days=1))

    log('Gathering data')
    response_json = urllib2.urlopen("http://www.theforthbridges.org/Umbraco/Api/Windspeed/GetWindfeedHistory").read()
    obj = json.loads(response_json)

    data = wind_speed.extract_data(obj)

    log('Persisting data to spreadsheet')
    xslx_file = spreadsheet.store_data(data)
    log('Spreadsheet: ' + xslx_file)

    log('Upload to S3')

    s3 = boto3.resource('s3')
    data = open(xslx_file, 'rb')
    key = 'wind-speed-' + report_id + '.xlsx'
    s3.Bucket('wind-speed-reports').put_object(Key=key, Body=data)
    url = boto3.client('s3').generate_presigned_url('get_object', {"Bucket": BUCKET_NAME, "Key": key }, ExpiresIn=604800)

    log('Download from: ' + url)

    log('Creating report')
    msg = '<pre>\n'
    msg += wind_speed.make_report(obj)
    msg +='\n</pre>\n'
    msg += '<a href="'+url+'">Click here to download the spreadsheet (including chart)</a>'
    msg += '\n\n<a href="http://wind-speed-reports.s3-website-eu-west-1.amazonaws.com/">Click here for all the previous reports</a>'

    log('\n' + msg)

    log('Sending emails')
    send_email(RECIPIENT_EMAIL, "Forth Bridge Wind Speed Report: " + report_id, msg)

    log('Complete.')


def log(msg):
    print("Wind Speed Report Service: " + msg)


def send_email(recipient, subject, body):
    post_data = {
        'from': 'do-not-reply@windspeedservice.com',
        'to': recipient,
        'cc': 'tom.pierce0@gmail.com',
        'subject': subject,
        'html': body
        }

    headers = {
        'Authorization': 'Basic {0}'.format(base64.b64encode(MAIL_GUN_API_KEY)),
        'Content-Type': 'application/x-www-form-urlencoded'
        }

    post_data = urllib.urlencode(post_data)
    req = urllib2.Request(MAIL_GUN_URL, post_data, headers)
    response = urllib2.urlopen(req)
    log('\n' + response.read())
