from typing import Optional

import aioboto3

from app.config.config import settings


class AsyncS3Client:
    """
    Async S3 client using aioboto3. Use as async context manager:

        async with AsyncS3Client() as s3:
            await s3.upload_file(...)
    """

    def __init__(self, bucket: Optional[str] = None):
        self.bucket = bucket or settings.S3_BUCKET
        self._session = None
        self._client = None

    async def __aenter__(self):
        self._session = aioboto3.Session()
        self._client = await self._session.client(
            "s3",
            region_name=settings.S3_REGION,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL or None,
        ).__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._client:
            await self._client.__aexit__(exc_type, exc, tb)
        self._client = None
        self._session = None

    async def upload_file(self, fileobj, key: str, content_type: Optional[str] = None):
        extra_args = {"ContentType": content_type} if content_type else {}
        await self._client.upload_fileobj(fileobj, self.bucket, key, ExtraArgs=extra_args)

    async def download_file(self, key: str, fileobj):
        await self._client.download_fileobj(self.bucket, key, fileobj)

    async def delete_file(self, key: str):
        await self._client.delete_object(Bucket=self.bucket, Key=key)
