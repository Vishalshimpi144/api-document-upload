import boto3
from botocore.exceptions import ClientError
import time

class S3():
    def upload_file_to_s3(self, bucketName, name, srcPath, aws_access_key_id, aws_secret_access_key):
        """
        upload the file to bucket...
        Args : bucketName : name of S3 bucket
                fileName: name of the file after being uploaded to S3 
                filePath : path of the file being uploaded
                aws_access_key_id = access id 
                aws_secret_access_key: secrete key
        returns : url and file Object name stored in S3
        
        """
        session = boto3.Session(
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                    )
        s3 = session.resource('s3')
        try:
            s3.Bucket(bucketName).upload_file(srcPath, name)
            client = boto3.client('s3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
            url = client.generate_presigned_url(ClientMethod='get_object',
                    Params={
                        'Bucket' : bucketName,
                        'Key' : srcPath,            
                    })
        except ClientError as e:
            return e, e

        return url, name

    #---------------------------------------------------------------------------------------
    def download_file_from_s3(self, bucketName, objName, aws_access_key_id,
                            aws_secret_access_key,
                            newName=None):
        """
        download the file from bucket...
        Args : bucketName : name of S3 bucket
                objName: name of the file in S3 
                newName : absolute path to store the downlaoded file
                aws_access_key_id = access id 
                aws_secret_access_key: secrete key
        """
        session = boto3.Session(
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key
                    )
        s3 = session.resource('s3')
        try:
            if newName is not None:
                s3.Bucket(bucketName).download_file(objName, newName)
            else: 
                s3.Bucket(bucketName).download_file(objName, objName)
        except ClientError as e:
            #logging.error(e)
            return e

        return True

    def create_s3_custom_document_name(self, lab_name: str, document_name: str):
        return f"{lab_name}_{document_name}_{time.time()}"

#=====================================================================================

# if __name__ == '__main__':
#     url, name = upload_file_to_s3( bucketName='vaibs-test-s3',
#                         srcPath='./screenshot.png', 
#                         name='temp.png',
#                         aws_access_key_id="", 
#                         aws_secret_access_key=""
#                         )


#     download_file_from_s3(bucketName='vaibs-test-s3',objName='temp.png', newName='./OCRFinal/test.png',
#                         aws_access_key_id="", 
#                         aws_secret_access_key=""
#                         # )
