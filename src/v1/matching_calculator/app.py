# type: ignore

# Third Party Library
import cv2
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service="MatchingScoreCalculator")


def score_similarity(desc_0, desc_1) -> float:
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(desc_0, desc_1)
    dist = [m.distance for m in matches]
    ret = sum(dist) / len(dist)
    return ret


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    body = event.body
    print(body)

    return {
        "statusCode": 200,
        "body": "OK",
    }
