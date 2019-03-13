### Task 6

It can be tested with a self written script or using a load testing tool.  
Here are two examples of each of them.  
They use Nginx server, configured to limit with 600 requests per minute.  

#### Script
Here is the example of the test using the [script](https://github.com/kavzov/testtask/raw/master/task_6/task_6.py).

It sending requests within 10 seconds to `http://localhost:8080/cats` and there the statistics in the console.  
After the script completing, you'll see the statistics of the total count of requests and the responses corresponding to status codes.  
It shows that the server responses with code 200 only to 10 requests per second, and for the others requests it responses with 429 http code.  

If you try to send the request `curl -X GET http://localhost:8080/cats` from the host, during the script performing, you'll receive  429 error.

To perform the script:  
- Pull docker image of the server:  
`docker pull kavzov/nginx-limit-req-sandbox:noburst`

- Run it:  
`docker run -d -p 8080:8080 --name nginx kavzov/nginx-limit-req-sandbox:noburst`

- Run the script in the container:  
`docker run -it --rm --link nginx:localhost kavzov/wg_tasks task6`
 
#### Load testing tools 
It also can be tested with a load testing tool such as jMeter, Yandex.Tank, Taurus etc.

Here is the simple example of such a test.  
It uses load-creating tool Yandex.Tank.

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
