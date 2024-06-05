# sentiment_MS_app
An microservices app using RESTful API to predict the sentiment of a social media comment. 

## How to run the code

Execute the docker-compose.yaml file using command

If you are on mac silicon: 
```DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose up```
If you are on linux: 
```docker compose up```

Once the docker file is up and running, you can utilize it as feddit api. The Feddit API is running at http://localhost:8080/docs. 

To Run the flask server, go to terminal or command prompt in the root folder and run ``` python app.py ```

The server is running at: http://127.0.0.1:5000/polarity/admin_1

User can utilize the api for 3 subfeddit categories i.e ```Admin_1, Admin_2,Admin_3```
### Querry parameters
The comment sentiment API has 3 querry parameters: 

1) sort: To sort comments based on polarity. User sort=Desc for desc order, sort=any value for asc value and 'sort=' for the original order. 
2) limit: parameter to limit the no of comments. 
3) date_range: parameter to filter the comments between the given date range. Format is YYYYMMDD. 

An example url with all parameters: http://127.0.0.1:5000/polarity/admin_1?sort=&limit=100&date_range=20240101,20240401

### Output 

Output is a JSON object with the format: 

{
"UID_comment": 1,
"date": "20240604",
"polarity_score": 1.0,
"sentiment_class": "Positive",
"text_comment": "It looks great!"
}




