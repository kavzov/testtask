It can be tested with load testing tools. For example jMeter, Yandex.Tank, Taurus etc.

Here is the simple example of such a test that using Nginx server, configured to limit with 600 requests per minute, and load-creating tool Yandex.Tank.

Docker image of the server:  
docker pull kavzov/nginx-limit-req-sandbox

Start:  
docker run -d --rm -p 8080:8080 kavzov/nginx-limit-req-sandbox

Docker image of Yandex.Tank:
docker pull direvius/yandex-tank

It's obligatory to have the file load.yaml inside the working directory.  
Start:  
docker run -v $(pwd):/var/loadtest -v $HOME/.ssh:/root/.ssh --net host --rm -it direvius/yandex-tank

Web results of such a testing are here:  
https://overload.yandex.net/167927

The graph of HTTP codes shows that when a number of requests exceeds 10 per second, the server responses with 429 http code:    
![http_codes](http_codes.jpg)