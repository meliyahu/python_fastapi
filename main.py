# import uuid
from random import randrange
from fastapi import FastAPI, HTTPException, status
from models.post import Post
from data.test_data import posts
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello to FastApi!"}
# 
'''  '''
# 
'''  '''
@app.post("/posts")
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
    
@app.get("/posts")
def get_posts():
    '''
      Retrieve all posts
    '''
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int):
    '''
    Retrieve a specific post based on id
    '''
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} was not found!")
    return post
        
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    '''
    Update a post
    '''
    # TODO implement
    update(id, post.dict())
    return {"message": "Post has been updated",
            "post": find_post(id)
            }
    
@app.delete("/posts/{id}")
def delete_post(id: int):
    '''
    Delete a post
    '''
    
    # TODO implement
    message = delete(id)
    return {"message": message}

def find_post(id: int):
    for post in posts:
        if post['id'] == id:
            return post
    return None

def update(id: int, post: Post):
    print(posts)
    for index, p in enumerate(posts):
        print(f'p={p}')
        if p['id'] == id:
            posts[index] = post
            break
def delete(id: int):
    found = None
    for post in posts:
        if post['id'] == id:
            found = post
            break
    if found:
        posts.remove(found)
        message = f'Post with id = {id} was deleted successfully'
    else:
        message = f'Post with id = {id} was not found!'                  
    return message
    