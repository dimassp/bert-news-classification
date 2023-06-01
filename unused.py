

# @app.post("/token", response_model=Token)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     response: Response
# ):
#     print("hello world from endpoint /token. Http method: POST")
#     print(f"form data username: {form_data.username}")
#     print(f"form data password: {form_data.password}")
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#         # data={"sub": "Dimas Samid"}, expires_delta=access_token_expires
#     )
#     print(f"access_token: {access_token}")
#     response.set_cookie(
#         key=COOKIE_NAME, 
#         value=f"{access_token}",
#         httponly=True,
#         expires=ACCESS_TOKEN_EXPIRE_MINUTES
#     )
#     response = RedirectResponse(url='/users/me', status_code=status.HTTP_303_SEE_OTHER)
#     print(f"access token generated: {access_token}")
#     print(f"response: {response}")
#     return response

# @app.post("/token", response_model=Token)


# @app.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ):
#     print("hello world from endpoint /token. Http method: POST")
#     print(f"form data: {form_data}")
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#         # data={"sub": "Dimas Samid"}, expires_delta=access_token_expires
#     )
#     print(f"access token generated: {access_token}")
#     return {"access_token" : access_token, "token_type": "bearer"}

# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     print("hello world from /users/me/")
#     return current_user
