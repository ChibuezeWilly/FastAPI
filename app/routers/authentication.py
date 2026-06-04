from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schema import UserLogin
from ..database import get_db
from .. import models
from .. import utils 
from .. import oauth2
from ..schema import UserTokenResponse

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=UserTokenResponse, status_code=status.HTTP_200_OK)
def get_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # get user's password.
    user_details = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    # if user is not found
    if user_details == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    # verify if true and return user details and token
    if utils.verify(user_credentials.password, user_details.password):
        # generate access_token
        access_token = oauth2.create_access_token(data={"user_id": user_details.id})
        return {"access_token": access_token,
                "token_type": "bearer", 
                "user": user_details
            }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    