from fastapi import Response, status, HTTPException, Depends , APIRouter
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schema import Vote
from .. import oauth2 as oauth

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(
    vote: Vote, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth.get_current_user)
):
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, 
        models.Votes.user_id == current_user.id
    )
    
    found_vote = vote_query.first()
    
    # check if post exist
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist") 

    # check direction of post
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"User {current_user.id} has already liked post {vote.post_id}"
            )
        new_like = models.Votes(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_like)
        db.commit()
        return {"message": "Successfully liked post"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully unliked post"}
