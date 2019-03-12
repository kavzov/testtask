FROM python:3.6
RUN git clone https://github.com/kavzov/wg_test_tasks.git
WORKDIR /wg_test_tasks
RUN pip install -r requirements.txt
ENV PYTHONPATH='/wg_test_tasks'
RUN chmod +x settings.sh
RUN ./settings.sh
