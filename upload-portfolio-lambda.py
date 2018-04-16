import boto3
import io
import zipfile
import mimetypes
import os
    
def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    topic = sns.Topic(os.environ['publishTopic'])
    location = {
        'bucketName': 'portfoliobuild.andreluizmelo.com',
        'objectKey': 'portfoliobuild.zip'
    }
    try:
        job = event.get("CodePipeline.job")
        if job:
            for artifact in job['data']['inputArtifacts']:
                if artifact['name'] == 'MyAppBuild':
                    location = artifact['location']['s3Location']
                    
        print("Building portfolio from " + str(location))
        portfolio_bucket = s3.Bucket('portfolio.andreluizmelo.com')
        build_bucket = s3.Bucket(location['bucketName'])
        
        # download to memory the zip file
        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj(location['objectKey'], portfolio_zip)
        
        # unzip and upload to the public facing bucket
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
    
        topic.publish(Subject='Portfolio Deployed', Message='Portfolio deployed successfully!')
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job['id'])
    except:
        topic.publish(Subject='Portfolio Not Deployed', Message='Portfolio was not deployed successfully!')
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_failure_result(jobId=job['id'])
        raise
    return 'Hello from Lambda'