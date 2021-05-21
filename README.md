# notif.ai task

## About
This is my solution to a recruitment task

## Deployment
The app is deployed on heroku.com, 
it runs on ```https://notifai-task.herokuapp.com```.

### Environment

The app should use Python 3.8.

To run the app one needs to set up the following environment variables:
| Variable              | Description                                       |
| --------------------- | ------------------------------------------------- |
| ```MONGODB_URI```     | An URI to connect to the database.                |
| ```SECRET_KEY```      | A secret key used, to encode access tokens.       |
| ```PASSWORD```        | A password to obtain the access token.            |
| ```TOKEN_EXP_TIME```  | Time after which the token expires, in minutes    |
| ```DATABASE_NAME```   | The name of the database, the app will connect to |

### Database
The app uses a MongoDB cluster, and assumes the following schema:

- database, named ```$DATABASE_NAME```
  - collection, named ```posts```
    - elements with schema: 
      | Key           | Type of value   |
      | ------------- | --------------- |
      | ```_id```     | ```ObjectId```  |
      | ```content``` | ```string```    |
      | ```views```   | ```int```       |
  
The "production" app 
(the one that runs on ```https://notifai-task.herokuapp.com```)
uses database called ```notidai-task-db``` and has a dedicated database user,
called ```app```, that has access only to that database.

There is also a database, created for testing, 
named ```notifai-task-db-test```, and a user, called ```tester```, 
that has access only to ```notifai-task-db-test```.

### Access to the database
If you want, to deploy the app yourself:
- You can use the following 
  ```MONGODB_URI```:
  ```mongodb+srv://tester:9o0GybiOxzoLs1iA@cluster0.i3cvv.mongodb.net/notifai-task-db-test?retryWrites=true&w=majority```

  Your app have access to the test database ```notifai-task-db-test```, 
  you will then need to set ```DATABASE_NAME``` to ```notifai-task-db-test```.

- Or you can create your own MongoDB cluster and obtain your own link
  

## API - Design decisions

Authentication is done in the fallowing way:
- the client provides a password in a request to a dedicated ```/login```  
  endpoint. 
- If the password is correct, the response contains an access token
  (JSON Web Token), 
  that the client can then send in requests, to authenticate itself.
- The token expires after a certain amout of time.

The posts are identified by an id, that is part of the endpint.

Since, the API is supposed to be used by other app, 
I decided, that all data and information will be passed through JSON, 
in the body of the request or response.
That includes error messages and password.

One exception is the access token, which will be passed in a header
```x-access-tokens```. The reasons for that are:
- This is the way It was done in a youtube tutorial,
- The token will be passed along with other data 
  and I don't want to mix the two.

The reason why do not pass the password with any of the standard methods, is
that all of the methods I've seen either are too complicated or involve a 
username and there are no users in this scenario.


## API - Documentation

You can also check out this API on SwaggerHub:
https://app.swaggerhub.com/apis/JankaGramofonomanka/notifai-task-api/1.0.0

### Paths

#### ```/login```
    
Allowed methods: ```POST```.

Methods:

- ```POST```
  
  Summary: Returns an access token, if request contains the correct password
  
  Request Body (required):
    - format: JSON
    - schema: [JSONPassword](#jsonpassword)
    
  Responses:
    - ```200``` - The password is correct
      
      Content:
        - format: JSON
        - schema: [JSONToken](#jsontoken)
    
    - ```401``` - Could not Verify
      
      Content:
        - format: JSON
        - schema: [JSONMessage](#jsonmessage)
  
  
#### ```/create```
    
Allowed methods: ```POST```.

Methods:

- ```POST```
      
  Summary: Creates a post and returns it's id.
  
  Headers:
    - (required) [AccessTokenHeader](#accesstokenheader)
  
  Request Body (required):
    - format: JSON
    - schema: [JSONPost](#jsonpost)
  
  Responses:
    - ```201``` - The post has been created
      
      Content:
        - format: JSON
        - schema: [JSONPostId](#jsonpostid)
    
    - ```401``` - [Unauthorized](#unauthorized)
  
  
#### ```/{postId}```

Allowed methods: ```GET```, ```PUT```, ```DELETE```.

Path parameters:
  - ```postId```
    - description: Id of the post
    - schema: [PostIdSchema](#postidschema)

Methods:

- ```GET```
  
  Summary: Returns the content of the post and the number of its views
    
  Responses:
  
    - ```200``` - Content of the post and number of it's views
      
      Content:
        - format: JSON
        - schema: [PostWithViews](#postwithviews)
            
    - ```404``` - [PostNotFound](#postnotfound)


- ```PUT```

  Summary: Overwrites the post and sets the view counter to 0
  
  Headers:
    - (required) [AccessTokenHeader](#accesstokenheader)
  
  Request Body (required):
    - format: JSON
    - schema: [JSONPost](#jsonpost)  
  
  Responses:
    - ```200``` - The post has been updated
      
      Content:
        - format: JSON
        - schema: [JSONMessage](#jsonmessage)

    - ```404``` - [PostNotFound](#postnotfound)
    - ```401``` - [Unauthorized](#unauthorized)



- ```DELETE```
  
  Summary: Deletes the post

  Headers:
    - (required) [AccessTokenHeader](#accesstokenheader)
  
  Responses:
    - ```200``` - The post has been deleted
      
      Content:
        - format: JSON
        - schema: [JSONMessage](#jsonmessage)

    - ```404``` - [PostNotFound](#postnotfound)
    - ```401``` - [Unauthorized](#unauthorized)



### Components - Responses
    
#### PostNotFound
  - description: Post does not exist.
  - content:
    - format: JSON
    - schema: [JSONMessage](#jsonmessage)
    
#### Unauthorized
  - description: Access token is missing or invalid.
  - content:
    - format: JSON
    - schema: [JSONMessage](#jsonmessage)


### Components - Headers
    
    
#### AccessTokenHeader
  - description: An access token, containing an encoded expiration date
  - header: ```x-access-tokens```
  - schema: [AccessToken](#accesstoken)
  
  
  
### Components - Schemas


#### PostIdSchema
  - description: Id of a post
  - type: ```string```
  - format: a 24-digit hexadecimal number
  - example: 
    ```
    "a213cdaf3453bbfcf44423fa"
    ```
    
#### PostContent
  - description: Content of a post
  - type: ```string```
  - format: A string of length between 1 and 160    
  - example: 
    ```
    "Today I ate 6 hamburgers."
    ```
  


#### AccessToken
  - description: An access token, containing an encoded expiration date
  - type: ```string```
  - example: 
    ```
    "t0T4l1y.VaL1D.T0k3n"
    ```

    
#### PostWithViews
  - description: Content of a post an the number of it's views
  - type: ```json```
  - fields:
    - ```"content"```
      - schema: [PostContent](#postcontent)
    
    - ```"views"```
      - type: ```int```
    
  - example: 
      
    ```
    {
        "content": "Today I ate 6 hamburgers.",
        "views": 123456
    }
    ```


#### JSONPost
  - description: Content of a post
  - type: ```json```
      
  - fields:
    - ```"content"```
      - schema: [PostContent](#postcontent)
  
  - example: 
    ```
    {"content": "Today I ate 6 hamburgers."}
    ```

    
#### JSONPassword
  - description: A password to obtain the access token
  - type: ```json```  
  - fields
    - ```"password"```
      - type: ```string```
      
  - example: 
    ```
    {"password": "drowssap"}
    ```

     
#### JSONMessage
  - description: A message about an error or other event
  - type: ```json```
  - fields
    - ```"message"```
      - type: ```string```
      
  - example: 
    ```
    {"message": "Aliens attacked our database."}
    ```
    
    
#### JSONToken
  - description: An access token, containing an encoded expiration date
  - type: ```json```    
  - fields:
    - ```"token"```
      - schema: [AccessToken](#accesstoken)
  
  - example: 
    ```
    {"token": "t0T4l1y.VaL1D.T0k3n"}
    ```
    
    
#### JSONPostId
  - description: Id of a post
  - type: ```json```
      
  - fields:
    - ```"id"```
      - schema: [PostIdSchema](#postidschema)
  
  - example: 
    ```
    {"id": "a213cdaf3453bbfcf44423fa"}
    ```





## Testing
Lookup ```./testing/README.md``` to read about testing.

Note: there are to ```requirements.txt``` files:
- ```./requirements.txt``` - requirements to run the app
- ```./testing/requirements.txt``` - requirements to run tests

Make sure to satisfy the right requirements, if you run the app or tests.


