from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
from sqlalchemy import MetaData, or_
from typing import Optional, List

app = FastAPI()

Base.metadata.create_all(bind=engine)

metadata = MetaData()
metadata.reflect(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def convert_to_string(interests: List[str]):
    return ",".join(item.capitalize() for item in interests)

def convert_to_list(interests: str):
    return [item.lower() for item in interests.split(',')] if interests else []

def sort_on_match_percentage(user_interests, matched_users):
    match_percentage = {}

    for matched_user in matched_users:
        matched_user.interests = convert_to_list(matched_user.interests)
        count = sum(1 for interest in matched_user.interests if interest in user_interests)
        
        percentage = 0
        if matched_user.interests:
            percentage = count / len(matched_user.interests)
        
        match_percentage[matched_user.id] = percentage

    sorted_users = sorted(matched_users, key=lambda user: (match_percentage.get(user.id, 0), user.age), reverse=True)
    return sorted_users

def special_sort(user, user_list):
    age_limit = 0
    result_list = []
    
    while age_limit <= 10:
        temp = []
        
        for matched_user in user_list:
            if matched_user.age == user.age - age_limit or matched_user.age == user.age + age_limit:
                temp.append(matched_user)
        
        if temp:
            temp = sort_on_match_percentage(user.interests, temp)
            result_list.extend(temp)
        
        age_limit += 1
    
    return result_list

# User registration
@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump()
    user_data["interests"] = convert_to_string(user_data["interests"])
    user_data["city"] = user_data["city"].lower().capitalize()
    
    if user_data["gender"].upper() not in ["M", "F"]:
        raise HTTPException(status_code=404, detail="Gender only 'F' or 'M' allowed")
    
    user_data["gender"] = user_data["gender"].upper()
    
    if user_data["age"] < 21 or user_data["age"] > 100:
        raise HTTPException(status_code=404, detail="Age should be between 21 and 100 both included")
    
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.interests = convert_to_list(db_user.interests)
    return db_user

# List of all users in DB
@app.get("/users/all_users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    if limit is not None and limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")

    query = db.query(models.User).offset(skip)
    if limit is not None:
        query = query.limit(limit)

    try:
        users = query.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving users")

    for user in users:
        user.interests = convert_to_list(user.interests)

    return users

# Read user by id
@app.get("/user/view_profile/{user_id}", response_model=schemas.User)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.interests = convert_to_list(user.interests)
    return user

# User update end point
@app.patch("/user/update/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_data = user.model_dump(exclude_unset=True)

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if 'email' in user_data:
        existing_user = db.query(models.User).filter(models.User.email == user_data['email']).filter(models.User.id != user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

    if 'interests' in user_data and user_data['interests']:
        user_data['interests'] = convert_to_string(user_data['interests'])

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    db_user.interests = convert_to_list(db_user.interests)
    return db_user

# Find match
@app.post("/users/find_match/{user_id}", response_model=List[schemas.User])
def user_match(user_id: int, min_age: Optional[int] = None, max_age: Optional[int] = None, city: Optional[List[str]] = None, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = db.query(models.User)

    if min_age is not None and max_age is not None:
        query = query.filter(models.User.age.between(min_age, max_age))
    elif min_age is not None:
        query = query.filter(models.User.age >= min_age)
    elif max_age is not None:
        query = query.filter(models.User.age <= max_age)

    if city:
        city_conditions = [models.User.city == ct.lower().capitalize() for ct in city]
        query = query.filter(or_(*city_conditions))

    if user.gender == 'M':
        query = query.filter(models.User.gender == 'F')
    else:
        query = query.filter(models.User.gender == 'M')

    matched_users = query.all()

    user_interests = convert_to_list(user.interests)

    if min_age or max_age:
        matched_users = sort_on_match_percentage(user_interests, matched_users)
    else:
        matched_users = special_sort(user, matched_users)
    
    return matched_users

# User delete
@app.delete("/user/delete/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"status": "success", "message": f"User with id {user_id} deleted from table"}

# Delete all users
@app.delete("/delete-all-users/confirm")
def delete_all_entries():
    db = SessionLocal()
    try:
        for table in reversed(metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        return {"status": "success", "message": "All entries deleted from all tables"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()