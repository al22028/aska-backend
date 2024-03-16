# Standard Library
import json

# Third Party Library
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from controllers.dev import DevController
from schemas.diff import DiffSchema

app = APIGatewayRestResolver(debug=True)
router = Router()
tracer = Tracer()

controller = DevController()


@router.post(
    "/diff/<image1_id>/<image2_id>",
    tags=["Dev"],
    summary="差分のjsonを計算",
    description="差分のJsonを計算します",
)
def create_image_diff(image1_id: str, image2_id: str) -> DiffSchema:
    return controller.create_image_diff(image1_id=image1_id, image2_id=image2_id)


v1_json = """
[s
    {
        "version": "1",
        "localIndex": "1",
        "glonbalIndex": "2",
        "index": "1-1-2",
        "id": "42318bc8-c698-4f9d-9c6c-e624778a670c",
        "src": "https://images.u10.teba-saki.net/U01998/1-1-2.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "2",
        "glonbalIndex": "3",
        "index": "1-2-3",
        "id": "722a2c37-7d93-4ef8-8ad5-083a1dee3f23",
        "src": "https://images.u10.teba-saki.net/U01998/1-2-3.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "3",
        "glonbalIndex": "5",
        "index": "1-3-5",
        "id": "ee62b4dc-0ec8-4d91-8baa-47aed6cae368",
        "src": "https://images.u10.teba-saki.net/U01998/1-3-5.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "4",
        "glonbalIndex": "6",
        "index": "1-4-6",
        "id": "51882f55-b1ad-4a27-b1aa-fdf0c31b0e0a",
        "src": "https://images.u10.teba-saki.net/U01998/1-4-6.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "5",
        "glonbalIndex": "7",
        "index": "1-5-7",
        "id": "8239a437-7181-4e73-8a57-723e061e035e",
        "src": "https://images.u10.teba-saki.net/U01998/1-5-7.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "6",
        "glonbalIndex": "8",
        "index": "1-6-8",
        "id": "623fe13e-56d1-4b5f-abfb-13daadc03c7b",
        "src": "https://images.u10.teba-saki.net/U01998/1-6-8.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "7",
        "glonbalIndex": "9",
        "index": "1-7-9",
        "id": "3b376c73-68df-4850-a375-7d4bc5858c59",
        "src": "https://images.u10.teba-saki.net/U01998/1-7-9.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "8",
        "glonbalIndex": "10",
        "index": "1-8-10",
        "id": "053996d3-bbd8-4bdb-b7f1-56387fdaae7e",
        "src": "https://images.u10.teba-saki.net/U01998/1-8-10.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "9",
        "glonbalIndex": "11",
        "index": "1-9-11",
        "id": "a249e381-36a3-43c2-a607-896dc092bd9e",
        "src": "https://images.u10.teba-saki.net/U01998/1-9-11.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "10",
        "glonbalIndex": "12",
        "index": "1-10-12",
        "id": "6a041777-dd27-409b-9e5f-1169a51bd48a",
        "src": "https://images.u10.teba-saki.net/U01998/1-10-12.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "11",
        "glonbalIndex": "13",
        "index": "1-11-13",
        "id": "98114cb0-019f-49df-8397-b03195ba2c86",
        "src": "https://images.u10.teba-saki.net/U01998/1-11-13.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "1",
        "localIndex": "12",
        "glonbalIndex": "14",
        "index": "1-12-14",
        "id": "d1df7c5c-e680-4e62-a8dc-3b50f04cb4c5",
        "src": "https://images.u10.teba-saki.net/U01998/1-12-14.png",
        "objectKey": "U01998/2-1-2.png"
    }
]
"""

v2_json = """

[
    {
        "version": "2",
        "localIndex": "1",
        "glonbalIndex": "2",
        "index": "2-1-2",
        "id": "51e58e7f-7016-4850-844c-5d1b733fa73f",
        "src": "https://images.u10.teba-saki.net/U01998/2-1-2.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "2",
        "glonbalIndex": "3",
        "index": "2-2-3",
        "id": "ca49743c-c5d0-45a5-9da3-ac07102c2b24",
        "src": "https://images.u10.teba-saki.net/U01998/2-2-3.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "3",
        "glonbalIndex": "4",
        "index": "2-3-4",
        "id": "a524cc73-27f6-41d4-90b1-6951155413be",
        "src": "https://images.u10.teba-saki.net/U01998/2-3-4.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "4",
        "glonbalIndex": "5",
        "index": "2-4-5",
        "id": "3d1b7304-7933-450e-a126-5196e949be8c",
        "src": "https://images.u10.teba-saki.net/U01998/2-4-5.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "5",
        "glonbalIndex": "6",
        "index": "2-5-6",
        "id": "048a6642-3627-4095-89e9-9a2f7693aae3",
        "src": "https://images.u10.teba-saki.net/U01998/2-5-6.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "6",
        "glonbalIndex": "7",
        "index": "2-6-7",
        "id": "d68316fc-3492-4fff-8317-3828dc533403",
        "src": "https://images.u10.teba-saki.net/U01998/2-6-7.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "7",
        "glonbalIndex": "8",
        "index": "2-7-8",
        "id": "49beec3f-4b65-4b0d-ad7e-35e23830d258",
        "src": "https://images.u10.teba-saki.net/U01998/2-7-8.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "8",
        "glonbalIndex": "10",
        "index": "2-8-10",
        "id": "f1100a2b-94c0-4385-b4b5-a3ec88b6787b",
        "src": "https://images.u10.teba-saki.net/U01998/2-8-10.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "9",
        "glonbalIndex": "11",
        "index": "2-9-11",
        "id": "21f0ff5f-620f-456c-b1fe-06e16215052c",
        "src": "https://images.u10.teba-saki.net/U01998/2-9-11.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "10",
        "glonbalIndex": "12",
        "index": "2-10-12",
        "id": "2f10a56c-6588-441b-a6a4-c50407979871",
        "src": "https://images.u10.teba-saki.net/U01998/2-10-12.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "11",
        "glonbalIndex": "13",
        "index": "2-11-13",
        "id": "bf24a18a-82c0-4adb-9832-2d4c65a7c958",
        "src": "https://images.u10.teba-saki.net/U01998/2-11-13.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "2",
        "localIndex": "12",
        "glonbalIndex": "14",
        "index": "2-12-14",
        "id": "ea0ed249-4242-4893-ad44-caf7190c5aa8",
        "src": "https://images.u10.teba-saki.net/U01998/2-12-14.png",
        "objectKey": "U01998/2-1-2.png"
    }
]
"""

v3_json = """

[
    {
        "version": "3",
        "localIndex": "1",
        "glonbalIndex": "2",
        "index": "3-1-2",
        "id": "301fb11f-c55c-4b7f-9e92-8c42c86b7e55",
        "src": "https://images.u10.teba-saki.net/U01998/3-1-2.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "3",
        "localIndex": "2",
        "glonbalIndex": "3",
        "index": "3-2-3",
        "id": "9d0a9ccc-f1c2-4d2b-b91c-ffe388898f51",
        "src": "https://images.u10.teba-saki.net/U01998/3-2-3.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "3",
        "localIndex": "3",
        "glonbalIndex": "8",
        "index": "3-3-8",
        "id": "d8d9fe17-710c-46e2-b276-6f14a4204009",
        "src": "https://images.u10.teba-saki.net/U01998/3-3-8.png",
        "objectKey": "U01998/2-1-2.png"
    }
]
"""


v4_json = """
[
    {
        "version": "4",
        "localIndex": "1",
        "glonbalIndex": "1",
        "index": "4-1-1",
        "id": "686d8423-ec35-474c-a877-ef2aa6e94e6e",
        "src": "https://images.u10.teba-saki.net/U01998/4-1-1.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "4",
        "localIndex": "4",
        "glonbalIndex": "5",
        "index": "4-4-5",
        "id": "78362eaf-7eb6-4662-873c-c623aee92bd6",
        "src": "https://images.u10.teba-saki.net/U01998/4-4-5.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "4",
        "localIndex": "3",
        "glonbalIndex": "6",
        "index": "4-3-6",
        "id": "05d27e71-116b-4d8e-9895-b584370e750f",
        "src": "https://images.u10.teba-saki.net/U01998/4-3-6.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "4",
        "localIndex": "2",
        "glonbalIndex": "8",
        "index": "4-2-8",
        "id": "b45431ff-3613-424e-b273-58f7e20bdf32",
        "src": "https://images.u10.teba-saki.net/U01998/4-2-8.png",
        "objectKey": "U01998/2-1-2.png"
    }
]
"""


v5_json = """

[
    {
        "version": "5",
        "localIndex": "1",
        "glonbalIndex": "2",
        "index": "5-1-2",
        "id": "32fba776-7113-45b1-8e3e-8edfb945b6d1",
        "src": "https://images.u10.teba-saki.net/U01998/5-1-2.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "2",
        "glonbalIndex": "3",
        "index": "5-2-3",
        "id": "82426524-a52f-46c8-bb3e-52e05a6aa181",
        "src": "https://images.u10.teba-saki.net/U01998/5-2-3.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "3",
        "glonbalIndex": "5",
        "index": "5-3-5",
        "id": "8d18d843-327a-4d4a-9283-a059ef0fe019",
        "src": "https://images.u10.teba-saki.net/U01998/5-3-5.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "4",
        "glonbalIndex": "6",
        "index": "5-4-6",
        "id": "648460a9-4b54-49cb-8897-95f6f0a3d272",
        "src": "https://images.u10.teba-saki.net/U01998/5-4-6.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "5",
        "glonbalIndex": "7",
        "index": "5-5-7",
        "id": "21e9e96b-735c-4431-bdae-c4b5773d89cf",
        "src": "https://images.u10.teba-saki.net/U01998/5-5-7.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "6",
        "glonbalIndex": "8",
        "index": "5-6-8",
        "id": "c2b39e42-6943-4ad5-bc14-21686f5262d2",
        "src": "https://images.u10.teba-saki.net/U01998/5-6-8.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "7",
        "glonbalIndex": "10",
        "index": "5-7-10",
        "id": "76cb3fab-1a14-41d8-a7ec-3ae3d7a19aa7",
        "src": "https://images.u10.teba-saki.net/U01998/5-7-10.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "8",
        "glonbalIndex": "11",
        "index": "5-8-11",
        "id": "b0491213-7a80-4688-855f-5f634d6cf759",
        "src": "https://images.u10.teba-saki.net/U01998/5-8-11.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "9",
        "glonbalIndex": "12",
        "index": "5-9-12",
        "id": "0c39fb24-1640-4e9b-af33-36c4bd0b9230",
        "src": "https://images.u10.teba-saki.net/U01998/5-9-12.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "10",
        "glonbalIndex": "13",
        "index": "5-10-13",
        "id": "1874bb9d-8b99-4407-82a8-39f78a709c95",
        "src": "https://images.u10.teba-saki.net/U01998/5-10-13.png",
        "objectKey": "U01998/2-1-2.png"
    },
    {
        "version": "5",
        "localIndex": "11",
        "glonbalIndex": "14",
        "index": "5-11-14",
        "id": "2033a0da-b1c8-4050-a49c-aa60feb002bd",
        "src": "https://images.u10.teba-saki.net/U01998/5-11-14.png",
        "objectKey": "U01998/2-1-2.png"
    }
]
"""


dummy_data = {
    "v1": json.loads(v1_json),
    "v2": json.loads(v2_json),
    "v3": json.loads(v3_json),
    "v4": json.loads(v4_json),
    "v5": json.loads(v5_json),
}


@router.get(
    "/versions/<versionId>",
    tags=["Dev"],
    summary="開発用",
    description="全てのユーザーを取得します。",
    response_description="VersionDetail",
    operation_id="devFetchVersionById",
)
def fetch_version_detail_by_id_for_dev(versionId: str) -> str:
    if versionId == "v1":
        return json.dumps(dummy_data["v1"])
    elif versionId == "v2":
        return json.dumps(dummy_data["v2"])
    elif versionId == "v3":
        return json.dumps(dummy_data["v3"])
    elif versionId == "v4":
        return json.dumps(dummy_data["v4"])
    elif versionId == "v5":
        return json.dumps(dummy_data["v5"])
    else:
        raise NotFoundError("Version not found")
