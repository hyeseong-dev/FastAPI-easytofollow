from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title: str
    description: str


class MyArticleSchema(ArticleSchema):
    class Config:
        orm_mode = True

class UpdateArticle(BaseModel):
    id: int
    title: str
    description: str

