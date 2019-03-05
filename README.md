# WG Forge test task
Works with the WG Forge test task environment.

Get docker image:  
`docker pull yzh44yzh/wg_forge_backend_env:1.1`

Run it:  
`docker run -d -p 5432:5432 --name backenv yzh44yzh/wg_forge_backend_env:1.1`

Requirements:  
`python 3.6`  
`psycopg2`

You may pull and run docker image of the repository:  
`docker pull kavzov/wg_tasks`  
`docker run -it -p 8080:8080 --name tasks --link backenv:localhost kavzov/wg_tasks bash`

Use the cli commands inside the 'tasks' container:  
`task1` runs `task_1.py`. It handles cats colors info and fill the database with the data.  
`task2` runs `task_2.py`. It calculates means, medians and modes of cats tails and whiskers and stores the statistics to the database.  
`task3` runs `task_3.py`. It starts simple http server. The server responses on GET request http://localhost:8080/ping from a HTTP client.  
`task4` runs `task_4.py`. It starts Python http server and handles GET requests with parameters.  
`task5` runs `task_5.py`. It starts Python http server, handles POST requests and stores valid data to the database.  
`tests` runs unit tests for task 4 and task 5

---
[Image at hub.docker.com](https://cloud.docker.com/u/kavzov/repository/docker/kavzov/wg_tasks)

