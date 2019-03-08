# WG Forge test task
To run the tasks:
- Pull docker image of the environment:  
`docker pull yzh44yzh/wg_forge_backend_env:1.1`  
- Pull docker image of the tasks:  
`docker pull kavzov/wg_tasks`  
- Run the environment:  
`docker run -d -p 5432:5432 --name backenv yzh44yzh/wg_forge_backend_env:1.1`
- Run docker image of the tasks:  
`docker run -it -p 8080:8080 --name tasks --link backenv:localhost kavzov/wg_tasks bash`

Use cli commands inside the 'tasks' container:  
`task1` handles cats colors info and fill the database with the data. The results are places in the database table 'cat_colors_info'.    
`task2` calculates means, medians and modes of cats tails and whiskers and stores the statistics to the database table 'cats_stat'.
`task3` starts simple http server. The server responses on GET request http://localhost:8080/ping from a HTTP client.  
`task4` starts Python http server which handles GET requests with parameters.  
`task5` starts Python http server which handles POST requests and stores valid cat data to the database table 'cats'.  
`tests` runs unit tests for both of task 4 and task 5.

Task 6 are placed in [task_6](https://github.com/kavzov/testtask/tree/master/task_6) directory in [text.md](https://github.com/kavzov/testtask/blob/master/task_6/text.md) file.  
