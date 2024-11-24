from datetime import datetime, timezone
from pathlib import Path

import requests
from pydantic import BaseModel


class RequestResult(BaseModel):
    request_err: str | None = None
    status_code: int | None = None
    response_text: str | None = None
    response_json: dict | None = None


class Env(StrEnum):
    development = "development"
    production = "production"


class BaseAPI:
    @staticmethod
    def utc_date() -> datetime:
        return datetime.now(tz=timezone.utc)

    @staticmethod
    def utc_date_short() -> str:
        return datetime.now(tz=timezone.utc).strftime("%Y%m%d%H%M%S")

    @staticmethod
    def write2file(data: str, file_path: str) -> None:
        """"""
        with open(file_path, "w") as f:
            f.write(data)

    @staticmethod
    def save_session_file(root_dir: Path, file_name: str, data: str) -> Path:
        date = BaseAPI.utc_date_short()
        path = Path(root_dir / date)
        path.mkdir(parents=True, exist_ok=True)
        fullpath = path / file_name.strip().lower()
        with open(fullpath, "w") as f:
            f.write(data)
        return fullpath

    @staticmethod
    def post_request_text(url: str, data: bytes, headers: dict | None = None) -> RequestResult:
        request_err: str | None = None
        status_code: int | None = None
        response_text: str | None

        try:
            r = requests.post(url, headers=headers, data=data, verify=False)
            status_code = r.status_code
            if status_code == 200:
                response_text = r.text
            else:
                request_err = r.text
        except Exception as exc:
            request_err = str(exc)

        return RequestResult(request_err=request_err, status_code=status_code, response_text=response_text)

    @staticmethod
    def post_request_json(url: str, data: bytes, headers: dict | None = None) -> RequestResult:
        request_err: str | None = None
        status_code: int | None = None
        response_text: str | None

        try:
            r = requests.post(url, headers=headers, data=data, verify=False)
            status_code = r.status_code
            if status_code == 200:
                response_text = r.text
            else:
                request_err = r.text
        except Exception as exc:
            request_err = str(exc)

        return RequestResult(request_err=request_err, status_code=status_code, response_text=response_text)
