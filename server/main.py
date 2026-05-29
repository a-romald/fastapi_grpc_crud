import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from grpc import aio

import proto.article_pb2_grpc
from service import ArticleService
from settings import GRPC_PORT, GRPC_KEY_VAL
from interceptor import APIKeyInterceptor
from db.model import Article
from database import init_db


async def serve():
    server = aio.server(
        ThreadPoolExecutor(max_workers=10),
        interceptors=(APIKeyInterceptor(GRPC_KEY_VAL),)        
    )
    #listen_addr = "[::]:50051"
    listen_addr = "[::]:{}".format(GRPC_PORT)
    proto.article_pb2_grpc.add_ArticleServiceServicer_to_server(
        ArticleService(), server
    )
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)

    # Table creating
    await init_db()

    await server.start()    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)


if __name__ == "__main__":
    logging.basicConfig()
    print("gRPC server started on port {}".format(GRPC_PORT))
    asyncio.run(serve())
