# notif.ai task - testing


Testing is done by the python script ```testing.py```. 
To run that stript, you need to set up the following envoronment variables:
| Variable              | Description                         |
| --------------------- | ----------------------------------- |
| ```HOST```            | the host of the tested app          |
| ```PASSWORD```        | password to obtain an access token  |
| ```TOKEN_EXP_TIME```  | (optional) expiration time of the access token in minutes. If ```TOKEN_EXP_TIME``` is not in the environment, the test for expiration of the token will be skipped (This might be useful if you want to "test on production", where the expiration time is 30 minutes.) |


You can run the tested app either locally or remotely.

- locally:
  
  - To run the app locally, you can run the script ```run_test_app```.
    You will then need the following environment to run the tests:
    | Variable              | Value                       |
    | --------------------- | --------------------------- |
    | ```HOST```            | ```http://127.0.0.1:5000``` |
    | ```PASSWORD```        | ```password```              |
    | ```TOKEN_EXP_TIME```  | ```0.1```                   |
  
  - You can then run the tests with the ```run_tests_local``` script, 
    where the environment is set up for you.

  - Note that there are 2 ```requiremetns.txt``` files:
    - ```./requirements.txt``` - requirements to run the app,
    - ```./testing/requirements.txt``` - requirements to run tests.
    
    Make sure you run ```run_test_app``` and ```run_tests_local``` in
    environments where appropriate requirements are installed.

- remotely:
  - You can run the app on a hosting service of your choice 
    (lookup ```../README.md``` to see how to deploy the app)
    or use a test instance of the app that runs on 
    ```https://notifai-task-test.herokuapp.com```.
    To run the tests on that instance,
    you will then need the following environment:
    | Variable              | Value                                         |
    | --------------------- | --------------------------------------------- |
    | ```HOST```            | ```https://notifai-task-test.herokuapp.com``` |
    | ```PASSWORD```        | ```password```                                |
    | ```TOKEN_EXP_TIME```  | ```0.1```                                     |

  - similarly to running the tests locally, there is a script
    ```run_tests_remote```, that sets up the environment for you 
    and runs the tests.

The app that runs on ```https://notifai-task-test.herokuapp.com```,
ass well as the app that is being run in the ```run_test_app``` script,
has acces to a seperate database  ```notifai-task-db-test```, 
created for testing. And they have a dedicated database user, 
called ```tester```, that has acces only to that database, 
therefore I allowed myself, to put the name of that user, 
and the password of that user in this publicly accessible repository.
(see ```MONGODB_URI``` in ```run_test_app```)

