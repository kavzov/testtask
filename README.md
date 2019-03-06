# WG Forge test task
The tasks solutions are in the numbered files.  
They use (except the task 3) the WG Forge test task backend environment.

`task_1.py` handles cats colors info and fill the database with the data.  
`task_2.py` calculates means, medians and modes of cats tails and whiskers and stores the statistics to the database.  
`task_3.py` starts simple http server. The server responses on GET request http://localhost:8080/ping from a HTTP client.  
`task_4.py` starts Python http server and handles GET requests with parameters.  
`task_5.py` starts Python http server, handles POST requests and stores valid data to the database.  
Inside the `tests` directory are the test files `test_task_4.py` and `test_task_5.py` which are run unit tests for task 4 and task 5 respectively.

To run the tasks pull docker image of the environment:  
`docker pull yzh44yzh/wg_forge_backend_env:1.1`  
and run it by:  
`docker run -d -p 5432:5432 --name backenv yzh44yzh/wg_forge_backend_env:1.1`

Requirements:  
`python 3.6`  
`psycopg2`

You may pull and run docker image of the repository:  
`docker pull kavzov/wg_tasks`  
`docker run -it -p 8080:8080 --name tasks --link backenv:localhost kavzov/wg_tasks bash`  

and use the cli commands inside the 'tasks' container:  
`task1` runs `task_1.py`, `task2` runs `task_2.py` etc.  
`tests` runs unit tests for both of task 4 and task 5.
---
[Image at hub.docker.com](https://cloud.docker.com/u/kavzov/repository/docker/kavzov/wg_tasks)
