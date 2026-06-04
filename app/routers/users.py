from fastapi import status, HTTPException, Depends, APIRouter
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schema import CreateUser, UserResponse
from .. import utils
from .. import oauth2

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
  
@router.get('/', response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User( **user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserResponse)
def get_single_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    return user