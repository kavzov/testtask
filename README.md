# WG Forge test task
To run the tasks:
- Pull docker image of the environment:  
`docker pull yzh44yzh/wg_forge_backend_env:1.1`  
- Pull docker image of the tasks:  
`docker pull kavzov/wg_tasks`  
- Run the environment:  
`docker run -d --name backenv yzh44yzh/wg_forge_backend_env:1.1`
- Run docker image of the tasks:  
`docker run -it -p 8080:8080 --name tasks --link backenv:localhost kavzov/wg_tasks bash`

Use cli commands inside the 'tasks' container:  
- `task1` handles cats colors info. The results are placed in the database.  
- `task2` calculates means, medians and modes of cats tails and whiskers and stores the statistics to the database.  
- `task3` starts socket server. The server responses the GET request of http://localhost:8080/ping from a host HTTP client.  
- `task4` starts http server which handles GET requests with parameters from a host HTTP client and send back a JSON response.  
- `task5` starts http server which handles POST requests from a host HTTP client and adds valid data to the database.  
- `tests` runs unit tests for both of task 4 and task 5.

Task 6 are placed in the [task_6](https://github.com/kavzov/testtask/tree/master/task_6) directory in the [text.md](https://github.com/kavzov/testtask/blob/master/task_6/text.md) file.  
