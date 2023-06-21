import json
from nostraio.event import Request, Filter


def test_request_filter_keys():
    # test these json keys with hash prefixes
    filtr = Filter(e=["test123"], p=["123test"])
    req = Request(sub_id="asd123", filter=filtr)
    assert json.loads(req.to_json())[2]["#e"] == filtr.e
