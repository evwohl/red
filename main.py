import random
import threading
import time

import requests
import secrets
import string

from twocaptcha import TwoCaptcha


def create(integ):
    num = integ
    while True:
        try:
            ses = requests.session()
            line = open('proxy.txt').readlines()[num]
            IP = line.split(":")[0]
            port = line.split(":")[1]
            proxies = {'https': f'http://{IP}:{port}',
                        'http': f'http://{IP}:{port}'}
            ses.proxies.update(proxies)
            r = ses.get("https://www.reddit.com/register/").text
            csrf = r.split('name="csrf_token" value="')[1].split('">')[0]
            sesid = ses.cookies['session']

            cookies = {
                'session': sesid,
             }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.reddit.com',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Referer': 'https://www.reddit.com/register/',
                'Connection': 'keep-alive',
                'TE': 'trailers',
            }
            solver = TwoCaptcha('233ae44e78b9072bc0fd7f46e885ca00')
            result = solver.recaptcha(sitekey='6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC',
                                        url='https://reddit.com/')
            key = result['code']
            letters = string.ascii_lowercase
            email = ''.join(random.choice(letters) for i in range(8)) + '@1secmail.com'
            user = ''.join(random.choice(letters) for i in range(8))
            alphabet = string.ascii_letters + string.digits
            pw = ''.join(secrets.choice(alphabet) for i in range(20))
            data = {
                'csrf_token': csrf,
                'g-recaptcha-response': key,
                'password': pw,
                'dest': 'https://www.reddit.com',
                'lang': 'en_US',
                'username': user,
                'email': email
            }

            response = ses.post('https://www.reddit.com/register', headers=headers, cookies=cookies, data=data)

            if '' in response.text:
                f = open("reddit.txt", "a")
                print(f"{user}:{email}:{pw}")
                f.write(f"{user}:{email}:{pw}\n")
                f.close()
            if num+30 < 1000:
                num = num+30
            else:
                num = integ
                time.sleep(300)
        except Exception as e:
            print(e)
            if num+30 < 1000:
                num = num+30
            else:
                num = integ
                time.sleep(300)
            pass

if __name__ == '__main__':
    jobs = []
    count = 0
    valid = 0
    threads = int(input("How many threads would you like to run? INTEGERS ONLY\n"))
    for i in range(0, int(threads)):
        t = jobs.append(threading.Thread(target=create, args=(i,)))

    # start  threads
    for j in jobs:
        j.start()
