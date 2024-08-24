#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
import requests


service_url = 'http://{}:{}'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


def get_options():
    parser = ArgumentParser(description='Recommendations service test script')
    parser.add_argument('-c', '--cold', help='use cold user id', action='store_true', required=False)
    parser.add_argument('-r', '--personal', help='use user id with personal recommendations', action='store_true', required=False)
    parser.add_argument('-u', '--user', help='use specific user id', type=int, required=False)
    parser.add_argument('-t', '--track', help='post specified track id to online history', type=int, required=False)
    parser.add_argument('-k', '--count', help='quantity of recommendations', type=int, default=10)
    parser.add_argument('-p', '--port', help='port', type=int, default=8000)
    parser.add_argument('-i', '--ip',   help='ip address', type=str, default='127.0.0.1')
    args = parser.parse_args()
    cnt = sum([1 if a else 0 for a in [args.cold, args.personal, args.user]])
    if 0 == cnt:
        parser.print_help()
        sys.exit(1)
    elif 1 < cnt:
        parser.print_help()
        print('-c, -r and -u options are mutually exclusive')
        sys.exit(2)
    return args


def get_recs(user_id: int, k: int):
    print(f'Get recommendations for {user_id}, k={k}')
    resp = requests.get(
        service_url + "/recommendations", headers=headers, params={'user_id': user_id, "k": k})
    if resp.status_code != 200:
        print(f"status code: {resp.status_code}")
    print(resp.json())


def post_event(user_id: int, item_id: int):
    resp = requests.post(
        service_url + "/store_event", headers=headers, params={'user_id': user_id, "item_id": item_id})
    if resp.status_code not in [200, 201]:
        print(f"status code: {resp.status_code}")
    print(resp.json())


if __name__ == '__main__':
    options = get_options()
    service_url = service_url.format(options.ip, options.port)
    if options.cold:
        user_id = 1
    elif options.personal:
        user_id = 778110
    else:
        user_id = options.user
    # print(options, user_id)
    post_event(user_id, options.track) if options.track else get_recs(user_id, options.count)
