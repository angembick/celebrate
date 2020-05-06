import boto3

def send_text(event, context):
#create sns client
    client = boto3.client(
        "sns",
        region_name="us-east-1"
        )
    s3client = boto3.client(
        's3',
        region_name='us-east-1'
    )  
    fileobj = s3client.get_object(
        Bucket='[bucket_name]',
        Key='bfile.txt'
        ) 
    filedata = fileobj['Body'].read()
    contents = filedata.decode('utf-8')
    #send sms message if there is data
    if filedata:
        response = client.publish(
            PhoneNumber="[phone_number]",
            Message=contents,
            MessageAttributes={
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Promotional'
                }
            }
        )
    return contents






