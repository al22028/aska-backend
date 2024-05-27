import json
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config

BUCKET_NAME = 'nakayama-aska-test'
DIRECTORY_UPLOAD = '~/'

s3_client = boto3.client("s3", config=Config(signature_version="s3v4"))

def presigned_url(event, context):
    #presigned URLを作成-----------------------------------------
    # 戻り値の初期化
    return_obj = dict()
    return_obj["body"] = dict()
    
    # バケット名の設定
    return_obj["body"]["bucket"] = BUCKET_NAME
    # フォルダー名の設定
    directory_upload = event.get("queryStringParameters", {}).get("directory_upload")
    if not directory_upload:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "directory_upload parameter is missing"})
        }
    return_obj["body"]["prefix"] = directory_upload

    target_info = s3_client.generate_presigned_post(BUCKET_NAME,
                                                    directory_upload + "${filename}", 
                                                    Fields=None,
                                                    Conditions=None,
                                                    ExpiresIn=3600)
    
    # 取得した各情報の戻り値への設定
    return_obj["body"]["contents"] = target_info
    
    return_obj["statusCode"] = 200
    return_obj["body"] = json.dumps(return_obj["body"])

    return return_obj


def search(event, context):
    title = event.get("queryStringParameters", {}).get("title")
    created = event.get("queryStringParameters", {}).get("created")
    modified = event.get("queryStringParameters", {}).get("modified")
    path = event.get("queryStringParameters", {}).get("path")  # Add path parameter
    if not title and not created and not modified and not path:  # Update condition
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Title, created, modified, or path parameter is missing"})  # Update error message
        }
    
    try:
        # バケット内のファイル一覧を取得
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=DIRECTORY_UPLOAD, Delimiter='/')
        
        # タイトルに一致するファイルを検索
        matching_files = []
        for content in response.get("Contents", []):
            key = content["Key"]
            file_title = key.replace(DIRECTORY_UPLOAD, "").replace("/", "")
            if title and title.lower() in file_title.lower():
                matching_files.append({
                    "name": file_title,
                    "size": "{:,} Bytes".format(content["Size"]),
                    "lastModified": content["LastModified"].strftime('%Y/%m/%d %H:%M:%S'),
                    "created": content["LastModified"].strftime('%Y/%m/%d'),
                    "key": key,
                    "etag": content["ETag"]
                })
            if created and created.lower() in content["LastModified"].strftime('%Y/%m/%d').lower():
                matching_files.append({
                    "name": file_title,
                    "size": "{:,} Bytes".format(content["Size"]),
                    "lastModified": content["LastModified"].strftime('%Y/%m/%d %H:%M:%S'),
                    "created": content["LastModified"].strftime('%Y/%m/%d'),
                    "key": key,
                    "etag": content["ETag"]
                })
            if modified and modified.lower() in content["LastModified"].strftime('%Y/%m/%d').lower():
                matching_files.append({
                    "name": file_title,
                    "size": "{:,} Bytes".format(content["Size"]),
                    "lastModified": content["LastModified"].strftime('%Y/%m/%d %H:%M:%S'),
                    "created": content["LastModified"].strftime('%Y/%m/%d'),
                    "key": key,
                    "etag": content["ETag"]
                })
            if path and path.lower() in key.lower():  # Add path condition
                matching_files.append({
                    "name": file_title,
                    "size": "{:,} Bytes".format(content["Size"]),
                    "lastModified": content["LastModified"].strftime('%Y/%m/%d %H:%M:%S'),
                    "created": content["LastModified"].strftime('%Y/%m/%d'),
                    "key": key,
                    "etag": content["ETag"]
                })
        
        # サブフォルダ内のファイルを検索
        for prefix in response.get("CommonPrefixes", []):
            subfolder = prefix["Prefix"]
            subfolder_response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=subfolder)
            for content in subfolder_response.get("Contents", []):
                key = content["Key"]
                file_title = key.replace(subfolder, "").replace("/", "")
                if title and title.lower() in file_title.lower():
                    matching_files.append({
                        "name": file_title,
                        "size": "{:,} Bytes".format(content["Size"]),
                        "lastModified": content["LastModified"].strftime('%Y/%m/%d %H:%M:%S'),
                        "created": content["LastModified"].strftime('%Y/%m/%d'),
                        "key": key,
                        "etag": content["ETag"]
                    })
                if created and created.lower() in content["LastModified"].strftime('%Y/%m/%d').lower():
                    matching_files.append({
                        "name": file_title,
                        "size": "{:,} Bytes".format(content["Size"]),
                        "lastModified": content["LastModified"].strftime('%Y/%m/%d %H:%M:%S'),
                        "created": content["LastModified"].strftime('%Y/%m/%d'),
                        "key": key,
                        "etag": content["ETag"]
                    })
                if modified and modified.lower() in content["LastModified"].strftime('%Y/%m/%d').lower():
                    matching_files.append({
                        "name": file_title,
                        "size": "{:,} Bytes".format(content["Size"]),
                        "lastModified": content["LastModified"].strftime('%Y/%m/%d %H:%M:%S'),
                        "created": content["LastModified"].strftime('%Y/%m/%d'),
                        "key": key,
                        "etag": content["ETag"]
                    })
                if path and path.lower() in key.lower():  # Add path condition
                    matching_files.append({
                        "name": file_title,
                        "size": "{:,} Bytes".format(content["Size"]),
                        "lastModified": content["LastModified"].strftime('%Y/%m/%d %H:%M:%S'),
                        "created": content["LastModified"].strftime('%Y/%m/%d'),
                        "key": key,
                        "etag": content["ETag"]
                    })
        
        if matching_files:
            return {
                "statusCode": 200,
                "body": json.dumps(matching_files)
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "No files found with the given title, created date, modified date, or path"})  # Update error message
            }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }


def rename_file(event, context):
    old_key = event.get("queryStringParameters", {}).get("old_key")
    new_key = event.get("queryStringParameters", {}).get("new_key")
    if not old_key or not new_key:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "old_key or new_key parameter is missing"})
        }
    
    try:
        # ファイルをコピー
        s3_client.copy_object(Bucket=BUCKET_NAME, CopySource={'Bucket': BUCKET_NAME, 'Key': old_key}, Key=new_key)

        # 元のファイルを削除
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=old_key)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File renamed successfully"})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

def rename_folder(event, context):
    old_folder_key = event.get("queryStringParameters", {}).get("old_folder_key")
    new_folder_key = event.get("queryStringParameters", {}).get("new_folder_key")
    
    if not old_folder_key or not new_folder_key:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "old_folder_key or new_folder_key parameter is missing"})
        }
    
    try:
        # フォルダ内のすべてのオブジェクトを取得
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=old_folder_key)
        
        # 各オブジェクトに対して
        for obj in response.get('Contents', []):
            old_key = obj['Key']
            new_key = old_key.replace(old_folder_key, new_folder_key, 1)
            
            # ファイルをコピー
            s3_client.copy_object(Bucket=BUCKET_NAME, CopySource={'Bucket': BUCKET_NAME, 'Key': old_key}, Key=new_key)
            
            # 元のファイルを削除
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=old_key)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Folder renamed successfully"})
        }
    
    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

def delete(event, context):
    key = event.get("queryStringParameters", {}).get("key")
    if not key:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Key parameter is missing"})
        }
    
    try:
        # ファイルを削除
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File deleted successfully"})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }