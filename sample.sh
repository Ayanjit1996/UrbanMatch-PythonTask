#!/bin/bash

declare -a users=(
    '{"name": "John", "age": 21, "gender": "M", "email": "john.doe@gmail.com", "city": "CityA", "interests": ["reading", "coding", "music"]}'
    '{"name": "Jane", "age": 22, "gender": "F", "email": "jane.doe@gmail.com", "city": "CityB", "interests": ["reading", "coding", "yoga"]}'
    '{"name": "Tom", "age": 23, "gender": "M", "email": "tom.smith@yahoo.com", "city": "CityC", "interests": ["sports", "coding", "travelling"]}'
    '{"name": "Lucy", "age": 24, "gender": "F", "email": "lucy.brown@hotmail.com", "city": "CityD", "interests": ["music", "travelling", "painting"]}'
    '{"name": "Mike", "age": 25, "gender": "M", "email": "mike.jones@outlook.com", "city": "CityE", "interests": ["reading", "photography", "yoga"]}'
    '{"name": "Emily", "age": 26, "gender": "F", "email": "emily.wilson@protonmail.com", "city": "CityF", "interests": ["sports", "gardening", "coding"]}'
    '{"name": "Chris", "age": 27, "gender": "M", "email": "chris.lee@icloud.com", "city": "CityG", "interests": ["photography", "music", "reading"]}'
    '{"name": "Sara", "age": 28, "gender": "F", "email": "sara.kim@aol.com", "city": "CityH", "interests": ["gardening", "reading", "yoga"]}'
    '{"name": "Dave", "age": 29, "gender": "M", "email": "dave.martin@gmx.com", "city": "CityI", "interests": ["sports", "music", "travelling"]}'
    '{"name": "Sophia", "age": 30, "gender": "F", "email": "sophia.miller@zoho.com", "city": "CityJ", "interests": ["painting", "dancing", "yoga"]}'
    '{"name": "Jack", "age": 21, "gender": "M", "email": "jack.evans@mail.com", "city": "CityA", "interests": ["travelling", "gaming", "sports"]}'
    '{"name": "Olivia", "age": 22, "gender": "F", "email": "olivia.jones@ymail.com", "city": "CityB", "interests": ["coding", "painting", "music"]}'
    '{"name": "Luke", "age": 23, "gender": "M", "email": "luke.moore@inbox.com", "city": "CityC", "interests": ["gaming", "music", "reading"]}'
    '{"name": "Ava", "age": 24, "gender": "F", "email": "ava.taylor@tutanota.com", "city": "CityD", "interests": ["gardening", "dancing", "travelling"]}'
    '{"name": "Ethan", "age": 25, "gender": "M", "email": "ethan.white@me.com", "city": "CityE", "interests": ["photography", "yoga", "coding"]}'
    '{"name": "Isabella", "age": 26, "gender": "F", "email": "isabella.harris@live.com", "city": "CityF", "interests": ["sports", "painting", "reading"]}'
    '{"name": "Noah", "age": 27, "gender": "M", "email": "noah.walker@msn.com", "city": "CityG", "interests": ["coding", "travelling", "music"]}'
    '{"name": "Mia", "age": 28, "gender": "F", "email": "mia.green@rediffmail.com", "city": "CityH", "interests": ["gaming", "music", "reading"]}'
    '{"name": "Liam", "age": 29, "gender": "M", "email": "liam.king@att.net", "city": "CityI", "interests": ["sports", "gardening", "yoga"]}'
    '{"name": "Amelia", "age": 30, "gender": "F", "email": "amelia.scott@fastmail.com", "city": "CityJ", "interests": ["reading", "photography", "travelling"]}'
)

for user in "${users[@]}"
do
   curl -X POST "http://localhost:8000/user/" -H "Content-Type: application/json" -d "$user"
done