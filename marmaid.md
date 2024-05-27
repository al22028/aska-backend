"Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "ap-northeast-1",
                "eventTime": "2024-04-25T06:35:24.400Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "AWS:AROAWHW6XYUXJGAIU4EQY:takahashi.k@world-wing.com"
                },
                "requestParameters": {
                    "sourceIPAddress": "152.117.250.35"
                },
                "responseElements": {
                    "x-amz-request-id": "B53Q3196AMGW85HE",
                    "x-amz-id-2": "XMETEfvBJt6gXU7e+78pDJZ5X41IjYb5OajFxD7MWVn4oKtBYY+KV4a6sgyFA+lLarv2iSbHnrot34A/y1h2qW96nmp0kvKR"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "s3-watch-lambda-dev-S3WatchHandler-68a737133cefb25bff959852b8f04754",
                    "bucket": {
                        "name": "s3-watch-test-bucket",
                        "ownerIdentity": {
                            "principalId": "A8NSL6PHSKQJB"
                        },
                        "arn": "arn:aws:s3:::s3-watch-test-bucket"
                    },
                    "object": {
                        "key": "README.md",
                        "size": 5314,
                        "eTag": "b4ec8414b05362d27f8baaa554c55129",
                        "sequencer": "006629F9AC54E3F7CE"
                    }
                }
            }
        ]


```mermaid
erDiagram

Records {
    string eventVersion
    string eventTime
    string eventName
    string principalId
    string x-amz-request-id
    string x-amz-id-2
    string configurationId
    string bucket_name
    string principalId
    string object_key
    string object_size
    string eTag
    string sequencer
}

```
