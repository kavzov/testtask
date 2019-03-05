FROM python:3.6
RUN git clone https://github.com/kavzov/testtask.git
WORKDIR /testtask
RUN pip install -r requirements.txt
ENV PYTHONPATH='/testtask'
RUN chmod +x settings.sh
RUN ./settings.sh
