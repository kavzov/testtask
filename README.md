# WG Forge Test task
Works with the WG Forge test task environment.  
Get docker image:  
`docker pull yzh44yzh/wg_forge_backend_env:1.1`  
Run it:  
`docker run -d -p 5432:5432 --name backenv yzh44yzh/wg_forge_backend_env:1.1`  

Requirements:  
`python 3.6`  
`psycopg2`

Docker image of the repository files:  
`docker push kavzov/wg_tasks`  
You may run it by:  
`docker run -it -p 8080:8080 --name tasks --link backenv:localhost kavzov/wg_tasks bash`  
and use cli commands inside the 'tasks' container:  
`task1` - handles cats colors and fill db with the data  
`task2` - calculates mean, medial and mode of cats tails and whiskers and store the statistics to db  
`task3` - starts simple http server. Response the string on GET request http://localhost:8080/ping  
`task4` - start Python http server and handles GET requests with parameters  
`task5` - start Python http server, handles POST requests and stores correct data to db  
`tests` - run unit tests for task 4 and task 5
---
[Image page at hub.docker.com](https://cloud.docker.com/u/kavzov/repository/docker/kavzov/wg_tasks)

