"""[summary]

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
import logging
import time
# from random import randrange

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor
from psycopg2 import DatabaseError, Error
# from starlette.responses import JSONResponse

# import app.helper_functions as helper_func
# from app.data.test_data import posts
from app.models.post import Post

logging.basicConfig(filename='fastapi.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
app = FastAPI()
while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='fastapi',
                                password='fastapi',
                                cursor_factory=RealDictCursor)
        # cursor = conn.cursor()
        logging.info('Database connection established!')
        print('Database connection established!')
        break
    except Error as error:
        logging.error('Connection failed!')
        logging.error('DB connection error: %s', error)
        logging.info('Retrying...')
        print('Connection failed!')
        print(f'DB connection error: {error}')
        print('Retrying....')
        time.sleep(4)


@app.get("/")
def read_root():
    """
    [summary]

    Returns:
        [type]: [description]
    """
    return {"message": "Hello to FastApi!"}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_class=JSONResponse)
# or create_post(pay_load: dict = Body(...)):
def create_post(post: Post):
    """
    Create a new post
    """

    qry = """
    INSERT INTO posts ("title", "content", "published") VALUES (%s, %s, %s) returning *;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(qry, (post.title, post.content, post.published))
            new_post = cur.fetchone()
    except (Exception, DatabaseError) as ex:
        logging.error(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex) from ex

    conn.commit()

    return {
        "message": "Post created successfully",
        "post": new_post
    }


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(off_set: int = 0, limit: int = 10):
    """
      Retrieve all posts.
      Allows for pagination
    """
    qry = """
    SELECT * FROM posts OFFSET %s LIMIT %s;
    """
    with conn.cursor() as cur:
        cur.execute(qry, (off_set, limit))
        posts = cur.fetchall()
    return {"data": posts}


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
def get_post(post_id: int):
    """
    Retrieve a specific post based on post_id
    """
    qry = """
    SELECT * FROM posts WHERE id=%s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(qry, (post_id, ))
            post = cur.fetchone()
    except (Exception, DatabaseError) as ex:
        logging.error('Get Post. post_id:%s does not exist!', post_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"DB Error: {ex}") from ex
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with post_id={post_id} was not found in the db!")
    return post


@ app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, post: Post):
    """
    Update a post
    """

    qry = """
    UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s returning *;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(qry, (post.title, post.content,
                        post.published, post_id))
            updated_post = cur.fetchone()
    except (Exception, DatabaseError) as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error:{ex}') from ex

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id={post_id} does not exist in db!')

    conn.commit()

    return {"message": "Post has been updated",
            "post": updated_post
            }


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """
    Delete a post
    """
    qry = """
    DELETE FROM posts WHERE id=%s RETURNING *;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(qry, (post_id,))
            post = cur.fetchone()
    except (Exception, DatabaseError) as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex) from ex

    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id={post_id} does not exist!')

    return Response(status_code=status.HTTP_204_NO_CONTENT)
