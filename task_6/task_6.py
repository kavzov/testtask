#!/usr/bin/env python
from requests_threads import AsyncSession
from time import time


session = AsyncSession()


async def main():
    SESSION_TIME = 5
    cnt_total = 0   # Total requests
    cnt_200 = 0     # Count of 200 responses
    cnt_429 = 0     # 429
    res_str = ''

    start = time()
    while True:
        end = time()
        total_time = end - start
        if total_time >= SESSION_TIME:
            break

        resp = await session.get('http://localhost:8080/')

        cnt_total += 1
        if resp.status_code == 200:
            cnt_200 += 1
        if resp.status_code == 429:
            cnt_429 += 1

        # clear previous string with ' ' of the string length
        print(' ' * len(res_str),  end='\r')

        # print new string
        res_str = 'Time: {} s, Requests: {}; 200: {}, 429: {}'.format(round(total_time, 2), cnt_total, cnt_200, cnt_429)
        print(res_str, end='\r', flush=True)

    print()

if __name__ == '__main__':
    session.run(main)
