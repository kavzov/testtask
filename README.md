# WG Forge test task
To run the tasks:
- Pull docker image of the environment and run it:  
`docker pull yzh44yzh/wg_forge_backend_env:1.1`  
`docker run -d --name backenv yzh44yzh/wg_forge_backend_env:1.1`

- Pull docker image of the tasks and run it:  
`docker pull kavzov/wg_tasks`  
`docker run -it -p 8080:8080 --name tasks --link backenv:localhost kavzov/wg_tasks bash`

Use cli commands inside the 'tasks' container:  
- `task1` performs task 1. It handles cats colors info and adds the results to the database.  
- `task2` performs task 2. It calculates means, medians and modes of the cats tails and whiskers. The results are placed to the database.  
- `task3` fires up the socket server. The server responses the GET request of http://localhost:8080/ping from a host HTTP client.  
- `task4` fires up the server that handles GET requests with parameters from a host HTTP client and send back a JSON response.  
- `task5` fires up the server that handles POST requests from a host HTTP client and adds valid data to the database.  
- `tests` runs unit tests for both of the task 4 and the task 5.

There are some optional handy commands:  
- `info cats` shows content of the 'cats' table  
- `info colors` shows content of the 'cat_colors_info' table  
- `info lengths` shows content of the 'cats_stat' table
- `clear cats` delete data from the 'cats' table  
- `clear colors` or `clear task1` delete data from the 'cat_colors_info' table  
- `clear lengths` or `clear task2` delete data from the 'cats_stat' table
  
Task 6 are placed in the [task_6](https://github.com/kavzov/testtask/tree/master/task_6) directory in the [text.md](https://github.com/kavzov/testtask/blob/master/task_6/text.md) file.  
