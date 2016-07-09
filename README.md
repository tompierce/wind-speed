# wind-speed-lambda

Produces a daily graph of windspeeds on the Forth Road Bridge. All the data and the graph are saved to a spreadsheet, which is stored in S3. A link to the spreadsheet and a summary of the data are emailed to the recipient.

## Requirements

- Python 2.7
- virtualenv
- Mailgun account (Free)
- AWS account

## Setup

### Download dependencies

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

### (Optional) Install emulambda

If you want to test locally, install emulambda: https://github.com/fugue/emulambda

### Create the config file

```
echo "MAIL_GUN_URL = 'https://api.mailgun.net/v3/sandboxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.mailgun.org/messages'" > config.py
echo "MAIL_GUN_API_KEY = 'api:key-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'" >> config.py
echo "RECIPIENT_EMAIL = 'XXXXXXXX@XXXXXXXX.com'" >> config.py
echo "BUCKET_NAME = 'a-bucket-that-you-own'" >> config.py
```

**replace the X's with your own keys/emails**

### Create package

```
chmod +x create_package.sh
./create_package.sh
```

### Upload to AWS Lambda

Not automated yet - Upload via the AWS console

- Runtime: Python 2.7
- Handler: lambda_handler.lambda_handler
- Role: (Create, or use existing role with access to the bucket BUCKET_NAME)

### Create a trigger "CloudWatch Events - Schedule"

e.g. cron(25 0 * * ? *)