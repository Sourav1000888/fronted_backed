from fastapi import FastAPI, status, BackgroundTasks, requests
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import sqlalchemy
from sqlalchemy import text
from contextlib import asynccontextmanager
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os



@asynccontextmanager
async def life_spaning(app : FastAPI):
    global conn, session_local
    backend_url = os.environ.get('backend_url')
    conn = sqlalchemy.create_engine(url=f'{backend_url}')
    try:
        with conn.begin() as connection:
            connection.execute(
                text("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT, password TEXT)"))

            connection.commit()
    except Exception as e:
        print(f'{e}')

    yield


app = FastAPI(title='testing', version='1.3.22', summary='testing apis', lifespan=life_spaning)


origin = ["http://127.0.0.1:5555", "http://127.0.0.1:2222", "http://127.0.0.1:8501"]

app.add_middleware(
    CORSMiddleware,allow_origins=origin, 
    allow_headers=['*'], allow_methods=['*'],
    allow_credentials=True,
)




class validate(BaseModel):
    username : str
    password : str


def insert_into_database(username : str, password : str):
    try:
        with conn.begin() as connection:
            connection.execute(
                text("""INSERT INTO users (username, password) VALUES 
                     (:username, :password);"""), 
                     {"username" : username, "password": password}
            )

            connection.commit()
            return True
    except Exception as e:
        return JSONResponse(content=f'{e}', status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return False

@app.post('/v1/user/data')
def saving_data(data : validate, back : BackgroundTasks):
    if data != None:
        back.add_task(insert_into_database, data.username, data.password)
        return JSONResponse(content='data is saved successfully', status_code=200)
    else:
        return JSONResponse(content='none value, plese enter value', status_code=status.HTTP_204_NO_CONTENT)
    


@app.get('/v1/user/data')
def get_save_data(username : str):
    if username != None:
        return pd.read_sql_query('select * from users', con=conn).to_dict(orient='records')
    elif username == None:
        return JSONResponse(content='none value', status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse(content='not found', status_code=status.HTTP_404_NOT_FOUND)
        