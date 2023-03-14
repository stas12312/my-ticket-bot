import io
from urllib import parse

import aioboto3

from services.config import Config


def create_session(
        config: Config,
) -> aioboto3.Session:
    """Формирование сессии"""
    return aioboto3.Session(
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        region_name=config.region_name,
    )


def get_filename(
        config: Config,
        user_id: int,
        filename: str,
):
    """Получение полного пути к файлу"""
    return f'{config.folder}/{user_id}/{filename}'


async def upload_file(
        s3_client,
        name: str,
        filename: str,
        bucket: str,
        body: io.BytesIO,
        content_type: str,
) -> None:
    """Загрузка файла в S3 хранилище"""
    url_filename = parse.quote_plus(name)
    extra_args = {
        'ContentType': content_type,
        'ContentDisposition': f'attachment; filename="{url_filename}"'
    }
    await s3_client.upload_fileobj(body, bucket, filename, ExtraArgs=extra_args)


async def get_object_url(
        filename: str,
        config: Config,
) -> str:
    """Получение URL файла"""
    return f'{config.s3_endpoint_url}/{config.bucket}/{filename}'
