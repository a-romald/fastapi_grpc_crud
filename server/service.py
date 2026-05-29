import grpc
from google.protobuf import wrappers_pb2

import proto.article_pb2
import proto.article_pb2_grpc
from db.repository import ArticleRepository


class ArticleService(proto.article_pb2_grpc.ArticleServiceServicer):    

    # all articles
    async def ListArticle(self, request, context):
        all_articles = await ArticleRepository.get_all()
        article_list = [{
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'published': wrappers_pb2.BoolValue(value=article.published),
            'created_at': article.created_at
        } for article in all_articles]

        return proto.article_pb2.ListArticleResponse(articles = article_list)


    # single article
    async def ReadArticle(self, request, context):        
        article_id = request.id
        article = await ArticleRepository.get_by_id(article_id)        
        if article:
            article_obj = {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'published': wrappers_pb2.BoolValue(value=article.published),
                'created_at': article.created_at
            }            
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Article not found")
            return proto.article_pb2.Article()        
        
        return proto.article_pb2.ReadArticleResponse(article = article_obj)


    # create article
    async def CreateArticle(self, request, context):        
        article_obj = {            
            "title": request.title,
            "content": request.content,
            "published": request.published            
        }

        try:
            article = await ArticleRepository.add(article_obj)

            new_article_obj = dict()
            if article:
                new_article_obj = {
                    'id': article.id,
                    'title': article.title,
                    'content': article.content,
                    'published': wrappers_pb2.BoolValue(value=article.published),
                    'created_at': article.created_at
                }        

            return proto.article_pb2.CreateArticleResponse(article = new_article_obj)
        except Exception as e:
            print('ORIG: ', e.orig)
            details = str(e.args[0]).replace("(", "").replace(")", "")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(details)
            return proto.article_pb2.Article()


    # update article
    async def UpdateArticle(self, request, context):        
        id = request.id
        article = await ArticleRepository.get_by_id(id)
        if not article:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Article not found")
            return proto.article_pb2.Article()
        
        if request.HasField('published'):
            pub_value = request.published.value  # Get True or False            
        else:
            pub_value = None            

        article_obj = {
            "id": id,
            "title": request.title,
            "content": request.content           
        }
        if pub_value is not None:
            article_obj.update({"published": wrappers_pb2.BoolValue(value=pub_value).value})

        try:
            upd_article = await ArticleRepository.update_one_by_id(id, article_obj)

            upd_article_obj = dict()
            if upd_article:
                upd_article_obj = {
                    'id': upd_article.id,
                    'title': upd_article.title,
                    'content': upd_article.content,
                    'published': wrappers_pb2.BoolValue(value=upd_article.published),
                    'created_at': upd_article.created_at
                }

            return proto.article_pb2.UpdateArticleResponse(article = upd_article_obj)
        except Exception as e:
            print('ORIG: ', e.orig)
            details = str(e.args[0]).replace("(", "").replace(")", "")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(details)
            return proto.article_pb2.Article()


    # delete article
    async def DeleteArticle(self, request, context):
        article_id = request.id
        article = await ArticleRepository.get_by_id(article_id)        
        if not article:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Article not found")
            return proto.article_pb2.Article()

        await ArticleRepository.delete(article_id)
        return proto.article_pb2.DeleteArticleResponse(result = True)
