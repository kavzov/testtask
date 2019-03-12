### Task 6

#### Script
It can be tested with a self written script like [this](https://github.com/kavzov/testtask/raw/remaster/task_6/task_6.py).

To perform it:  
- Pull docker image of the server:  
`docker pull kavzov/nginx-limit-req-sandbox:noburst`

- Run it:  
`docker run -d -p 8080:8080 --name nginx kavzov/nginx-limit-req-sandbox:noburst`

- Run docker image of the tasks in console mode:  
`docker run -it --link nginx:localhost --rm kavzov/wg_tasks bash`
 
- Inside the tasks container run `task6` command.  

It starts sending requests (within 10 seconds) to `http://localhost:8080/cats` and there will the statistics in the console.  
After the task completing, you'll see the statistics of total count of requests and responses by status code.  
It shows that the server handles only 10 requests per second, and for the others requests it responses with 429 http code.  

If you'll try to send request from the host like `curl -X GET http://localhost:8080/cats`, during the script performing, you will receive a 429 error.
 
#### Load testing tools 
It also can be tested with a load testing tool such as jMeter, Yandex.Tank, Taurus etc.

Here is the simple example of such a test.  
It using Nginx server, configured to limit with 600 requests per minute, and load-creating tool Yandex.Tank.

Web results of the test are here:  
https://overload.yandex.net/167927

The graph of HTTP codes shows that when a number of requests exceeds 10 per second, the server responses with 429 http code:    
![http_codes](http_codes.jpg)

To perform it:
- Pull docker image of the server:  
`docker pull kavzov/nginx-limit-req-sandbox`

- Pull docker image of Yandex.Tank:  
`docker pull direvius/yandex-tank`

- Start the server:  
`docker run -d -p 8080:8080 kavzov/nginx-limit-req-sandbox`

- Put the [load.yaml](https://github.com/kavzov/testtask/raw/master/task_6/load.yaml) file to your working directory

- Start the load test:  
`docker run -it -v $(pwd):/var/loadtest --net host direvius/yandex-tank`

_It is necessary to have an account at [overload.yandex.net](http://overload.yandex.net) and 'overload' section in config file (as described at [Overload documentation](https://overload.yandex.net/mainpage/guide)) to get online statistics of a test._
