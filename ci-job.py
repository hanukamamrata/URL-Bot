from requests import get, post
from json import loads
import sys, os

try:
    count = int(sys.argv[1])
except:
    count = 0

all_tokens = loads(get('https://pastebin.com/raw/jHWc7wVF').text)['CI']

GIT_URL = os.environ.get('GIT_URL')
owner_and_repo = GIT_URL.replace('https://github.com/', '') if GIT_URL else None
ci_token = None
for usr in list(all_tokens):
    if usr in str(owner_and_repo):
        ci_token = all_tokens[usr]

d=print

def print(*a, **kw):
    kw["flush"] = True # To print directly to CI log without delaying.
    return d(*a, **kw)

exit_with_error = False
"""working_proxy = None
try:
    resp = get("http://exurl.in")
    available = True
except KeyboardInterrupt:
    raise KeyboardInterrupt
except:
    print("exurl.in is not available to this CI. Getting proxy from api...")
    from proxy_server import working_proxy, commit_used, discommit_used
    if not working_proxy:
        print('No proxies available, either all proxies used or dead')
        available = False
        exit_with_error = True

ip = get('http://ip-api.com/json').json().get('query')
ip_used = 'false' in get(f'https://ip-limiter-server.onrender.com/?ip={ip}').text
if ip_used and not working_proxy:
    print(f'This ip {ip} is already used. Getting proxy from api...')
    from proxy_server import working_proxy, commit_used, discommit_used
    if not working_proxy:
        print('No proxies available, either all proxies used or dead')
        available = False
        exit_with_error = True"""

available = True
from proxyscrape import get_session
working_proxy = get_session()

if available:
    try:
        # Run the main file
        import main as random_function_idk
        #if working_proxy: commit_used()
        random_function_idk.main(working_proxy)
        count+=1
    except KeyboardInterrupt:
        #if working_proxy: discommit_used()
        raise KeyboardInterrupt
    except:
        #if working_proxy: discommit_used()
        #if not working_proxy and ip:
            #from proxy_server import discommit_used
            #discommit_used('https://'+ip+':80')
        exit_with_error = True
        import traceback
        print(traceback.format_exc())


if count <= 10000000:
    if ci_token:
        resp = post(
            f"https://circleci.com/api/v2/project/github/{owner_and_repo}/pipeline",
            headers={
                "Circle-Token":  ci_token,
                "Content-Type": "application/json"
            },
            data='{"branch":"main","parameters":{"count":"' + str(count) + '"}}'
        )
        if resp.status_code != 201:
            print(resp.text)
            exit_with_error=True
    else:
        print('CI TOKEN Not found, skipping auto trigger.')

if exit_with_error:
    sys.exit(1)
