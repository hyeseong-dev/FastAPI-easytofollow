from typing import List

from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Depends
from starlette.status import HTTP_204_NO_CONTENT
from .database import engine, sessionLocal
from . import models
from . import schemas
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/articles', status_code=status.HTTP_200_OK, response_model=List[schemas.MyArticleSchema])
def get_all_articles(db:Session = Depends(get_db)):
    my_articles = db.query(models.Article).all()
    return my_articles

@app.get('/articles/{id}', status_code=status.HTTP_200_OK, response_model=schemas.MyArticleSchema)
def article_details(id:int, db:Session = Depends(get_db)):
    # my_articles = db.query(models.Article).filter(models.Article.id == id).first()
    my_articles = db.query(models.Article).get(id)

    if my_articles: 
        return my_articles
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.post('/articles/', status_code=status.HTTP_201_CREATED)
def add_article(article: schemas.ArticleSchema , db:Session = Depends(get_db)):
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@app.put('/articles/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_article(id:int, article: schemas.ArticleSchema, db:Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).update({'title': article.title, 'description': article.description} )
    db.commit()
    return {'message': 'The Data Is Updated'}

@app.delete('/articles/{id}', status_code=HTTP_204_NO_CONTENT)
def delete_article(id:int, db:Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)