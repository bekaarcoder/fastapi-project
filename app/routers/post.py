from typing import List
from fastapi import status, Response, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..schemas import Post, PostResponse
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# @app.get("/posts/")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data": posts}


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
def create_post(
    post: Post,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @app.post("/posts/", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     cursor.execute(
#         """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
#         (post.title, post.content, post.published),
#     )
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}


@router.get("/{id}/")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found.",
        )
    return {"data": post}


# @app.get("/posts/{id}/")
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} was not found.",
#         )
#     return {"data": post}


@router.delete("/{id}/")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found.",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.delete("/posts/{id}/")
# def delete_post(id: int):
#     cursor.execute(
#         """DELETE FROM posts where id = %s RETURNING *""", (str(id),)
#     )
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} was not found.",
#         )
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}/", status_code=status.HTTP_200_OK)
def update_post(
    id: int,
    post: Post,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found.",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


# @app.put("/posts/{id}/", status_code=status.HTTP_200_OK)
# def update_post(id: int, post: Post):
#     cursor.execute(
#         """UPDATE posts set title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#         (post.title, post.content, post.published, str(id)),
#     )
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id {id} was not found.",
#         )
#     return {"data": updated_post}
