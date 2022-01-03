import logging
from random import randrange

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor

import app.helper_functions as helper_func
from app.data.test_data import posts
from app.models.post import Post

logging.basicConfig(filename='fastapi.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
app = FastAPI()
try:
    conn = psycopg2.connect(host='localhost',
                            database='fastapi',
                            user='fastapi',
                            password='fastapi',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
except psycopg2.Error as err:
    print(f'DB connection error: {err}')


@app.get("/")
def read_root():
    """
    [summary]

    Returns:
        [type]: [description]
    """
    return {"message": "Hello to FastApi!"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# or create_post(pay_load: dict = Body(...)):
def create_post(post: Post):
    '''
    create a new post
    '''
    print(f'Post(pydantic model) = {post}')
    print(f'Post(python dict) = {post.dict()}')
    post.post_id = randrange(10, 10000)
    # Save new post
    posts.append(post)
    return {
        "message": "Post created successfully",
        "post": post
    }


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    '''
      Retrieve all posts
    '''
    return {"data": posts}


@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
def get_post(post_id: int):
    '''
    Retrieve a specific post based on post_id
    '''
    post = helper_func.find_post(post_id, posts)
    if not post:
        logging.error('Get Post. post_id:%s does not exist!', post_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with post_id={post_id} was not found!")
    return post


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, post: Post):
    '''
    Update a post
    '''
    updated = helper_func.is_update_post(post_id, post.dict(), posts)
    if not updated:
        logging.error('Update Post. post_id:%s does not exist!', post_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with post_id: {post_id} does not exist!')

    return {"message": "Post has been updated",
            "post": helper_func.find_post(post_id, posts)
            }


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    '''
    Delete a post
    '''

    deleted = helper_func.is_delete_post(post_id, posts)
    if not deleted:
        logging.error('Delete Post. post_id:%s does not exist!', post_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with post_id = {post_id} does not exist!')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
