from fastapi import Response, status, HTTPException, Depends , APIRouter
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schema import CreatePost, PostResponse
from .. import oauth2 as oauth
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user), post_limit: int = 10, skip:int=0, search: str | None = ""):
    
    posts = db.query(models.Post,func.count(models.Votes.post_id.label("Votes"))).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(post_limit).offset(skip).all()
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostResponse)
def get_single_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    post =  db.query(models.Post,func.count(models.Votes.post_id.label("Votes"))).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
       
    return post
            
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actionn")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=PostResponse)
def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actionn")
     
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    return updated_post.first()

