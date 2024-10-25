# from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# app = FastAPI()

# #pydantic classes
# # pydantic is used to validate the data passed in post request similar to kotlin data class

# class Post(BaseModel):
#     title : str
#     content : str
#     published : bool = True
    

# #database connection
# while True:
#     try:
#         conn = psycopg2.connect(host= 'localhost', database = 'fastapi', user = 'postgres', password = '2003', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected successfully")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error: ", error)
#         time.sleep(2)



# #async does not matter
# #order of function does matter in python
# my_post = [{'title' : 'title of post1', 'content' : 'content of post1', 'id': 1}, {'title' : 'fav food', 'content' : 'pizza', 'id': 2}]

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p


# def find_index(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i
        

# @app.get('/')
# async def root():
#     return {"message" : "Hello"}


# @app.get('/posts')
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {"data" : posts}

# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_posts(post : Post):
#     # print (post.rating)
#     # post.dict() .dict is depreceated
#     # print(post.model_dump())
#     # post_dict = post.model_dump()
#     # post_dict['id'] = randrange(0, 10000000)
#     # my_post.append(post_dict)   
#     cursor.execute ("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()

#     return {"data" :new_post}
# #title : string, content : String, category, bool published



# #  get a single post
# @app.get('/posts/{id}')
# def get_post(id:int, response: Response):
#     # print(type(id))

#     # post = find_post(int(id)) # in python default datatype is str so we have to convert it to int
#     # post = find_post(id)
#     # if not post:
#     #     response.status_code = status.HTTP_404_NOT_FOUND
#     #     return {'message' : f'post with id : {id} not found '}
#     # return {"post_detail" : f"this is the post {id}"}

#     # db
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
#     post = cursor.fetchone()


#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail= f'post with id : {id} not found')
#     return {"data" : post}

# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id : int):
#     # delete post
#     # index = find_index(id)

#     # if index == None:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exits")
#     # my_post.pop(index)

#     # return Response(status_code=status.HTTP_204_NO_CONTENT)
#     # db
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))

#     deleted_post = cursor.fetchone()
#     conn.commit()

#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exits")

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# @app.put("/posts/{id}")
# def update_post(id : int, post: Post):
#     # print(post)
#     # index = find_index(id)
#     # if index == None:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id= {id} not found")
    
#     # post_dict = post.model_dump()
#     # post_dict['id'] = id
#     # my_post[index] = post_dict
#     cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content, id, ))
#     post = cursor.fetchone()
#     conn.commit()

    
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id= {id} not found")

#     return {'data' : post}
