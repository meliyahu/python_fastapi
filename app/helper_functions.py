from typing import Any
from app.models.post import Post
def find_post(id: int, posts: list[Any]):
    for post in posts:
        if post['id'] == id:
            return post
    return None

def is_update_post(id: int, post: Post, posts: list[Any]):
    updated = False
    for index, p in enumerate(posts):
        if p['id'] == id:
            post["id"] = id
            posts[index] = post
            updated = True
            break
    return updated
        
def is_delete_post(id: int, posts: list[Any]):
    deleted = False
    for post in posts:
        if post["id"] == id:
            posts.remove((post))
            deleted = True
            break
    return deleted
    