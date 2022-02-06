# Random Object Generator API
Random Object Generator API is a microservice backend system which providing endpoints:
  - As mentioned on the title, it has main function to generate printable random-objects: (1) Alphabetical strings, (2) Real numbers, (3) Integers, and (4) Alphanumerical strings; each object is separated by comma mark (","). The generated objects then are stored as a text file (.txt) which 2 MB in size.
  - After successfully generating a file, there is a url / link in its response to access / download the file.
  - There is a specific endpoint to analyze the file to get some total number from each random object types.
  - As an extra endpoint to list of all existing files in the backend system.

## Download the source
To evaluate this project you can clone the repo
```
git clone https://github.com/subajat1/random-object-generator-api
```

## On-premises deployment
   - for demo purpose, please rename the `.env-dev` to `.env`
```
$ cd {project_dir}
$ python manage.py run --reload
```


## Deployment using docker container
```
$ cd {project_dir}
$ docker-compose build
$ docker-compose up -d
```

## Internal use docs (Swagger)
After successfuly deploying the project, please access `http://127.0.0.1:5000/` using browser, or use tools like Postman.
