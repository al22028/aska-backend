# mypy: ignore-errors
import time
import boto3
import json
import uuid
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

client = boto3.client("lambda")
s3 = boto3.client("s3")
start_time = time.time()


def get_object_body(bucket: str, key: str) -> bytes:
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8")

def invoke_lambda():
    # 12.11 seconds
    payload = {
        "body": {
            "bucket_name": "aska-image-bucket-dev",
            "before": {"json_object_key":"id231321/3.json","image_object_key":"id231321/3.png"},
            "after": {"json_object_key":"id231321/2.json","image_object_key":"id231321/2.png"},
            "params" : {
                "match_threshold" : 0.85,
                "threshold" : 220,
                "eps" : 20,
                "min_samples" : 50,
            },
        }
    }

    response = client.invoke(
        FunctionName="aska-api-dev-ImageDiffHandler",
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=bytes(json.dumps(payload).encode()),
    )

    print(response["Payload"].read().decode("utf-8"))

def invoke_lambda_conn(conn):
    # 8.949 seconds
    payload = {
        "body": {
            "bucket_name": "aska-image-bucket-dev",
            "before": {"json_object_key":"id231321/10.json","image_object_key":"id231321/10.png"},
            "after": {"json_object_key":"id231321/2.json","image_object_key":"id231321/2.png"},
            "params" : {
                "match_threshold" : 0.85,
                "threshold" : 220,
                "eps" : 20,
                "min_samples" : 50,
            },
        }
    }

    response = client.invoke(
        FunctionName="aska-api-dev-ImageDiffHandler",
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=bytes(json.dumps(payload).encode()),
    )
    conn.send(response["Payload"].read().decode("utf-8"))
    print("--- %s seconds (Function call) ---" % str(time.time() - start_time)[:5] )
    conn.close()

def invoke_lambda_conn_optimized(conn, instance_id):
    payload = {
        "instance_id": instance_id,
        "bucket_name": "aska-image-bucket-dev",
        "before": {"json_object_key": "id231321/4.json", "image_object_key": "id231321/4.png"},
        "after": {"json_object_key": "id231321/2.json", "image_object_key": "id231321/2.png"},
        "params": {
            "match_threshold": 0.85,
            "threshold": 220,
            "eps": 20,
            "min_samples": 50,
        },
    }

    response = client.invoke(
        FunctionName="aska-api-dev-ImageDiffHandler",
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=bytes(json.dumps(payload).encode()),
    )
    conn.send(response["Payload"].read().decode("utf-8"))
    print("--- %s seconds (Function call) ---" % str(time.time() - start_time)[:5])
    conn.close()

if __name__ == "__main__":
    invoke_lambda() # 12.11 seconds
    print("--- %s seconds (Function call) ---" % str(time.time() - start_time)[:5] )

    # process_list = []
    # parent_connection_list = []
    # for i in range(10):
    #     instance_id = str(uuid.uuid4())
    #     parent_conn, child_conn = multiprocessing.Pipe()
    #     parent_connection_list.append(parent_conn)
    #     process_list.append(multiprocessing.Process(target=invoke_lambda_conn, args=(child_conn, )))
    # for process in process_list:
    #     process.start()

    process_list = []
    parent_connection_list = []
    for i in range(10):
        instance_id = str(uuid.uuid4())
        parent_conn, child_conn = multiprocessing.Pipe()
        parent_connection_list.append(parent_conn)
        process_list.append(multiprocessing.Process(target=invoke_lambda_conn_optimized, args=(child_conn, instance_id)))
    for process in process_list:
        process.start()

    print("--- %s seconds ---" % str(time.time() - start_time)[:5])
