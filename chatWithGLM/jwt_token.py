"""
鉴权 token 组装过程
"""
import time
import jwt
import os

os.environ["ZHIPUAI_API_KEY"] = "c9013ab959212d97e15a990157aca180.Vnts9vS3PzWscsJm"


def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )
