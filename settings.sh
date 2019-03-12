#!/usr/bin/env bash

chmod +x task_* tests/tests.sh

ln -s /wg_test_tasks/task_1.py /usr/local/bin/task1
ln -s /wg_test_tasks/task_2.py /usr/local/bin/task2
ln -s /wg_test_tasks/task_3.py /usr/local/bin/task3
ln -s /wg_test_tasks/task_4.py /usr/local/bin/task4
ln -s /wg_test_tasks/task_5.py /usr/local/bin/task5
ln -s /wg_test_tasks/task_6/task_6.py /usr/local/bin/task6

ln -s /wg_test_tasks/tests/tests.sh /usr/local/bin/tests

ln -s /wg_test_tasks/extra/clear.py /usr/local/bin/del
ln -s /wg_test_tasks/extra/info.py /usr/local/bin/inf
