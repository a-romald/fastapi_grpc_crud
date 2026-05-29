from typing import List
import typing as t

from fastapi import APIRouter, Path, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from google.protobuf.json_format import MessageToDict
from google.protobuf import wrappers_pb2
import grpc

from . schema import Article, ArticleCreate, ArticleUpdate
from . client import grpc_article_client
import proto.article_pb2


router = APIRouter()


@router.get("/", response_model=List[Article])
async def get_all(client: t.Any = Depends(grpc_article_client)) -> JSONResponse:    
    articles = await client.ListArticle(proto.article_pb2.ListArticleResponse())
    return JSONResponse(MessageToDict(articles))


@router.get("/{id}/", response_model=Article)
async def get(id: int, client: t.Any = Depends(grpc_article_client)) -> JSONResponse:    
    # Read article by ID using the gRPC stub
    try:
        article = await client.ReadArticle(proto.article_pb2.ReadArticleRequest(id = id))
    except grpc.RpcError as e:
        status_code = e.code()
        details = e.details()
        if status_code == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail=details)
    return JSONResponse(MessageToDict(article))


@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
async def post(payload: ArticleCreate, client: t.Any = Depends(grpc_article_client)) -> JSONResponse:
    # Create new article
    try:
        article = await client.CreateArticle(
            proto.article_pb2.CreateArticleRequest(
                title = payload.title,
                content = payload.content,
                published = payload.published
            )
        )
    except grpc.RpcError as e:
        status_code = e.code()
        details = e.details()
        if status_code == grpc.StatusCode.INVALID_ARGUMENT:
            raise HTTPException(status_code=422, detail=details)

    return JSONResponse(MessageToDict(article))


@router.put("/{id}/", response_model=Article)
async def put(payload: ArticleUpdate, id: int = Path(..., gt=0), client: t.Any = Depends(grpc_article_client)) -> JSONResponse:        
    pub_val = False if payload.published is None else True

    article_obj = {
        'id': id,
        'title': payload.title if payload.title else None,
        'content': payload.content if payload.content else None
    }

    if pub_val:
        article_obj.update({"published": wrappers_pb2.BoolValue(value=payload.published)})

    try:
        article = await client.UpdateArticle(
            proto.article_pb2.UpdateArticleRequest(
                **article_obj
            )
        )
    except grpc.RpcError as e:
        status_code = e.code()
        details = e.details()
        if status_code == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail=details)
        if status_code == grpc.StatusCode.INVALID_ARGUMENT:
            raise HTTPException(status_code=422, detail=details)

    return JSONResponse(MessageToDict(article))


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, client: t.Any = Depends(grpc_article_client)) -> None:
    try:
        await client.DeleteArticle(proto.article_pb2.DeleteArticleRequest(id=id))
    except grpc.RpcError as e:
        status_code = e.code()
        details = e.details()
        if status_code == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail=details)
