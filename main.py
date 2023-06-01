from typing import Annotated
from datetime import date, timedelta
from pydantic import BaseModel
from transformers import pipeline

from fastapi import FastAPI, Body, Request, Depends, HTTPException, status, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordRequestForm

from news_portal.scrape import Scrape

from db.fake_user_db import fake_users_db
from db.connection import get_connection_and_cursor, update_news
from job.jobs import scheduler, trigger
from job.tasks2 import scrape_and_classify
from models.news import News
from security.auth import (oauth2_scheme, User, get_current_user, UserInDB, 
                           get_current_active_user, Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES,
                           create_access_token, COOKIE_NAME, get_current_active_user_from_cookie)

# from security.auth import (oauth2_scheme, User,  UserInDB,  Token, authenticate_user, 
#                            ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, COOKIE_NAME, 
#                            get_current_active_user_from_cookie)


scheduler.start()
clf = pipeline(model="dimassamid/IndobertNewsTest")
type_clf = pipeline(model="rizalmilyardi/IndobertTypeNews")
origins = ["*"]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/js", StaticFiles(directory="static"), name="js")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")
news_portals = [
    {"id": "detiknewsjabar","name": "Detik News Jabar"},
    {"id": "antaranewsjabar","name": "Antara News Jabar"},
    {"id": "tribunjabar","name": "Tribun Jabar"},
    {"id": "sekitarbandung","name": "Sekitar Bandung"},
    {"id": "prbandung","name": "Pikiran Rakyat Bandung"},
]


@app.get("/users/me/items")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    print("hello world from /users/me/items")
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {
        "token": token
    }

# class News(BaseModel):
#     news: str

class Feedback(BaseModel):
    news_content: str
    content_type_feedback: str
    event_category_feedback: str

class ScrapeInfo(BaseModel):
    portal: list
    
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
@app.get("/login")
def login(request: Request):
# def redirect_from_slash():
    # return RedirectResponse("http://127.0.0.1:8000/scrape")
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/dashboard")
def admin_dashboard(request: Request):
    return templates.TemplateResponse(r"soft-ui-dashboard-main/pages/dashboard.html", {"request": request})

@app.get("/tables")
def admin_dashboard(request: Request):
    connection, cursor = get_connection_and_cursor()
    # column_to_retrieve = ["content_type_id", "feedback_content_type_id", "event_category_id", "feedback_event_category_id", 
    #                       "region_code", "region_level_2_code","region_level_3_code", "region_level_4_code",
    #                       "address", "coordinates", "impact_score", "content_text", "news_source_url"]
    column_to_retrieve = ["news_id","content_type_id", "feedback_content_type_id", "event_category_id", "feedback_event_category_id", "content_text"]
    columns = ", ".join(column for column in column_to_retrieve)
    # columns = columns[:-2]
    sql = f"SELECT {columns} FROM news;"
    print(f"sql: {sql}")
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    news = []
    for data in result:
        news_id, content_type_id, feedback_content_type_id, event_category_id, feedback_category_id, content_text = data
        print(f"news_id: {news_id}")
        print(f"feedback_category_id: {feedback_category_id}")
        news.append({
            "news_id": news_id,
            "content_type_id": content_type_id,
            "feedback_content_type_id": feedback_content_type_id,
            "event_category_id": event_category_id,
            "feedback_category_id": feedback_category_id,
            "content_text": content_text
        })
    return templates.TemplateResponse(r"soft-ui-dashboard-main/pages/tables.html", {"request": request, "result": news})
# @app.put("/tables/")
# def update_news(feedback: Feedback):
#     print("hello world from put tables. Feedback from admin: ")
#     print(feedback)
#     # return {
#     #     "message": "hello world from put tables. Feedback from admin: "
#     # }
#     return RedirectResponse(url='/tables', status_code=status.HTTP_303_SEE_OTHER)
    
@app.put("/tables/edit/{news_id:path}",name='path-conventor')
def edit_news(news_id: str, news: News):
    print("hello world from put tables. Feedback from admin: ")
    update_news(news_id, news.feedback_content_type, news.feedback_event_category, news.news_content)
    print(f"Row successfully updated")
    return RedirectResponse("http://localhost:8000/tables",status_code=303)
@app.get("/tables/{news_id:path}",name='path-conventor', response_class=HTMLResponse )
def get_news(request: Request, news_id: str):
    
    connection, cursor = get_connection_and_cursor()
    columns_to_retrieve_from_table_news = ["news_id","content_type_id", "feedback_content_type_id", "event_category_id", "feedback_event_category_id", "content_text"]
    columns = ", ".join(column for column in columns_to_retrieve_from_table_news)
    sql = f"SELECT {columns} FROM news where news_id='{news_id}';"
    cursor.execute(sql)
    result_news = cursor.fetchone()
    print(f"result news type: {result_news}")
    news_id_, content_type_id, feedback_content_type_id, event_category_id, feedback_category_id, content_text = result_news
    columns_to_retrieve_from_table_content_type = ["content_type_id"]
    columns = ", ".join(column for column in columns_to_retrieve_from_table_content_type)
    sql = f"SELECT {columns} FROM ref_content_type;"
    cursor.execute(sql)
    result_content_type = cursor.fetchall()
    result_content_type_list = list()
    for content_type in result_content_type:
        result_content_type_list.append(content_type[0])
    
    columns_to_retrieve_from_table_event_category = ["event_category_id"]
    columns = ", ".join(column for column in columns_to_retrieve_from_table_event_category)
    sql = f"SELECT {columns} FROM ref_event_category;"
    cursor.execute(sql)
    result_event_category = cursor.fetchall()
    result_event_category_list = list()
    for event_category in result_event_category:
        result_event_category_list.append(event_category[0])
    cursor.close()
    connection.close()
    result = {
        "news": {
            "news_id": news_id_,
            "content_type_id": content_type_id,
            "feedback_content_type_id": feedback_content_type_id,
            "event_category_id": event_category_id,
            "feedback_category_id": feedback_category_id,
            "content_text": content_text
        },
        "content_type": result_content_type_list,
        "event_category": result_event_category_list
    }
    return templates.TemplateResponse(r"soft-ui-dashboard-main/pages/edit.html", {"request": request, "result": result})

@app.post("/login-attempt")
def login():
    print("Hello world from post login")
@app.get("/classify", response_class=HTMLResponse)
def classify_news_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/scrape",response_class=HTMLResponse)
def scrape_news(request: Request):
    return templates.TemplateResponse("scrape.html", {"request":request})
@app.get("/scrape-instagram",response_class=HTMLResponse)
def scrape_instagram(request: Request):
    print("Hello world from scrape instagram")
    return templates.TemplateResponse("scrape_instagram.html",{"request": request})

# @app.post("/klasifikasi")
# def classify_news(news_: News, request: Request):    
#     news = r"{}".format(news_.news)
#     print(f"request method: {request.method}")
#     news_type = type_clf(news)[0]['label']
    
#     if news_type == "non-kejadian":
#         return {
#             "message" : "success",
#             "news_type" : news_type,
#             "news_topic" : "-"
#         }
#     news_topic =clf(news)[0]['label']
#     score = clf(news_.news)[0]['score']
#     return {
#         "message" : "success",
#         "news_type" : news_type,
#         "news_topic" : news_topic
#     }

@app.on_event('startup')
def cronjob():
    scheduler.add_job(scrape_and_classify, trigger)