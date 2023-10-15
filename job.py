from requests import get, post
import sys

try:
    count = int(sys.argv[1])
except:
    count = 0

gh_token = sys.argv[2]
owner_and_repo = sys.argv[3]

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
        random_function_idk.main(working_proxy, headless=False)
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
    resp = post(
        f"https://api.github.com/repos/{owner_and_repo}/actions/workflows/Job.yml/dispatches",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization":  f"Bearer {gh_token}",
            "Content-Type": "application/json"
        },
        data='{"ref":"main","inputs":{"count":"' + str(count) + '"}}'
    )
    if resp.status_code != 204:
        print(resp.text)
        exit_with_error=True

if exit_with_error:
    sys.exit(1)
