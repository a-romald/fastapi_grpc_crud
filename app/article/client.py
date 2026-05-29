from typing import Callable, Any

import grpc
import proto.article_pb2_grpc

from config import settings


class APIKeyInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def intercept_unary_unary(self, continuation: Callable, client_call_details: Any, request: Any):
        # Create new metadata with API Key
        metadata = []
        if client_call_details.metadata:
            metadata = list(client_call_details.metadata)
        
        metadata.append((settings.GRPC_KEY_NAME, self._api_key))
        
        # Update details with new metadata
        client_call_details = client_call_details._replace(metadata=metadata)
        
        # Continue the call
        return await continuation(client_call_details, request)


async def grpc_article_client():
    """
    Creates an asynchronous gRPC client for the ArticleService.

    This function creates an unsecured gRPC channel with the server using the host and port parameters
    specified in the settings and returns a client object for communicating with the ArticleService.

    When creating a channel, we use the interceptors parameter to add our interceptor, into which we pass the secret key

    Returns:
    -----------
    article_pb2_grpc.ArticleServiceStub
        A client object for interacting with the gRPC service ArticleService.
    """
   
    channel = grpc.aio.insecure_channel(
        f'{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}',
        interceptors=[
            APIKeyInterceptor(settings.GRPC_KEY_VAL),
        ]
    )

    client = proto.article_pb2_grpc.ArticleServiceStub(channel)
    return client
