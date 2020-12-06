# Course CRUD:

###Create
Endpoint:

```
POST /api/course/
```

Example Body:

```
{
  "content": {
    "course_id": 123123124,
    "course_name": "PHYS 259"
  }
}
```

Example Successful Response:

```
{
  "response": {
    "course_id": 123123124,
    "course_name": "PHYS 259"
    "prerequisites": []
  }
}
```

###Update
Endpoint:

```
PUT /api/course/
```

Example Body:

```
{
  "content": { # You can send any one
    "course_id": 123123124, 
    "course_name": "PHYS 259"
    "
  }
}
```

Example Successful Response:

```
{
  "response": {
    "course_id": 123123124,
    "course_name": "PHYS 259"
    "prerequisites": []
  }
}
```
