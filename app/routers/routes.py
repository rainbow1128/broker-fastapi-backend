from fastapi import APIRouter, Request, Depends, Header
from typing import Union
from sqlalchemy.orm import Session
from plaid.api import plaid_api

from ..schemas import schemas
from ..services import crud
from ..config import database, plaid

database.create_tables()

plaid_client = plaid.get_plaid_client()

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Server is running"}


# User signs up for the platform
@router.post("/platform/signup")
async def create_user(user: schemas.User):
    username = user.email
    password = user.password
    signup_result = crud.cognito_signup(username, password)
    return signup_result


# User logs into the platform
@router.post("/platform/login")
async def login_user(user: schemas.User):
    username = user.email
    password = user.password
    login_result = crud.cognito_login(username, password)
    return login_result


# Sign up for brokerage account
@router.post("/accounts/signup")
async def create_brokerage_account(account: schemas.AccountCreate, request: Request, db: Session = Depends(database.get_db)):
    account = crud.create_account(db=db, account=account, request=request)
    return account


# Get brokerage account
@router.get("/accounts/{identifier}", response_model=schemas.Account)
async def get_brokerage_account(identifier: str, request: Request, db: Session = Depends(database.get_db)):
    db_user = crud.get_account(db, identifier=identifier, request=request)
    return db_user

# # Create Plaid link token
# @router.post("/plaid/create_link_token")
# def create_link_token(identifier: schemas.Identifier, 
#                       request: Request,
#                       db: Session=Depends(database.get_db),
#                       access_token: Union[str, None] = Header(default=None)):
#     # Get the client_user_id by searching for the current user
#     link_token = crud.get_link_token(db,
#                                      identifier=identifier.identifier,
#                                      request=request,
#                                      plaid_client=plaid_client)
#     return link_token


# Create Plaid link token
@router.post("/plaid/create_link_token")
def create_link_token( 
                      request: Request,
                      db: Session=Depends(database.get_db)):
                    #   access_token: Union[str, None] = Header(default=None)):
    # Get the client_user_id by searching for the current user
    link_token = crud.get_link_token(db,
                                     identifier='helluva@test.ca',
                                     request=request,
                                     plaid_client=plaid_client)
    print(link_token)
    return {"link_token": link_token}


# Get processesor token from public token
@router.post("/plaid/exchange_public_token")
async def exchange_token(plaid_response: schemas.PlaidExchangeInfo):
    print(plaid_response)
    processor_token = crud.get_processor_token(plaid_response, plaid_client)
    return processor_token
