# Third Party Library
from aws_lambda_powertools.utilities.data_classes import S3Event
from aws.lambda_client import LambdaClient
from database.base import Image


class ImageProceccor:

    client = LambdaClient()

    def __init__(self, event: S3Event) -> None:
        self._event = event
        self._bucket_name = event.bucket_name
        self._object_key = event.object_key

    def find_page(self) -> None:
        # 該当ページ見つける or 作成処理
        pass

    def parse_object_key(self) -> None:
        # オブジェクトキーから情報を抽出
        pass

    def find_image(self) -> None:
        # 画像を取得 or 作成処理
        pass

    def find_matching(self) -> None:
        # マッチングを取得 or 作成処理
        pass

    def calculate_macthing_score(self, target_image: Image) -> None:
        # 画像のマッチング計算
        pass

    def calculate_differential(self, target_image: Image) -> None:
        # 差分計算
        pass
