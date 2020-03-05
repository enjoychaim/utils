"""
在Python3.0测试通过
需要在gitlab里面新建一个AccessToken
需要在本地机器设置一个环境变量，比如：GIT_SSH_COMMAND = ssh -i C:/Users/wsq/key/wsq.key
"""
from urllib.request import urlopen
import json
import subprocess
import shlex
import time
import os

gitlabAddr = ''
gitlabToken = ''

for index in range(10):
    url = "http://%s/api/v4/projects?private_token=%s&per_page=100&page=%d&order_by=name" % (gitlabAddr, gitlabToken, index)
    print(url)
    allProjects = urlopen(url)
    allProjectsDict = json.loads(allProjects.read().decode())
    if len(allProjectsDict) == 0:
        break
    for thisProject in allProjectsDict:
        try:
            thisProjectURL = thisProject['ssh_url_to_repo']
            thisProjectPath = thisProject['path_with_namespace']
            print(thisProjectURL + ' ' + thisProjectPath)

            if os.path.exists(thisProjectPath):
                command = shlex.split('git -C "%s" pull' % (thisProjectPath))
            else:
                command = shlex.split('git clone %s %s' % (thisProjectURL, thisProjectPath))

            resultCode = subprocess.Popen(command)
            time.sleep(1)
        except Exception as e:
            print("Error on %s: %s" % (thisProjectURL, e.strerror))
