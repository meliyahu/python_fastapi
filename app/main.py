# import uuid
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
from fastapi import FastAPI, HTTPException, status, Response
from app.models.post import Post
from app.data.test_data import posts
import app.helper_functions as helper_func

logging.basicConfig(filename='fastapi.log', level=logging.DEBUG)
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
    return {"message": "Hello to FastApi!"}
# 
'''  '''
# 
'''  '''
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# or create_post(pay_load: dict = Body(...)):
def create_post(post: Post):
    '''
    create a new post
    '''
    print(f'Post(pydantic model) = {post}')
    print(f'Post(python dict) = {post.dict()}')
    post.id = randrange(10, 10000)
    #Save new post
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

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    '''
    Retrieve a specific post based on id
    '''
    post = helper_func.find_post(id, posts)
    if not post:
        logging.error(f'Get Post. id:{id} does not exist!')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} was not found!")
    return post
        
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    '''
    Update a post
    '''
    # TODO implement
    updated = helper_func.is_update_post(id, post.dict(), posts)
    if not updated:
        logging.error(f'Update Post. id:{id} does not exist!')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id: {id} does not exist!')
    
    return {"message": "Post has been updated",
            "post": helper_func.find_post(id, posts)
            }
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    '''
    Delete a post
    '''
    
    # TODO implement
    deleted = helper_func.is_delete_post(id, posts)
    if not deleted:
        logging.error(f'Delete Post. id:{id} does not exist!')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with id = {id} does not exist!')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    