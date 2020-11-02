---
title: "Extracting data from Github"
date: 2020-09-05
description: Micropost on GitHub api ETL
titleWrap: wrap
enableSidebar: false
enableToc: false
tags: ['python', 'github', 'api', 'micropost']
---

## GitHub ETL

So I have been interested in looking at my GitHub activity, and for this reason
I built a simple class in python for handling this task while keeping to github
rate limiting:

```python
#!/usr/bin/env python

"""Logging setup

To use this module, just import it to set up the logger.
It should persist from import across the runtime.

"""
from github import GithubException
from datetime import datetime
from time import sleep

class GithubRequester():
    def __init__(self, gh, rate_lim_sensitivity=100, cooldown_s=360):
        self.gh = gh
        self.rate_lim_sensitivity = rate_lim_sensitivity
        self.cooldown_s = cooldown_s

    def check_ratelim(self):
        while self.gh.get_rate_limit().raw_data['core']['remaining'] < self.rate_lim_sensitivity:
            print(f"RATELIM: Reached ratelim : {self.gh.get_rate_limit().raw_data['core']} -- Sleeping {self.cooldown_s} secs")
            sleep(self.cooldown_s)

    def wrap_request(self, request_gen):
        done = False
        while not done:
            try:   
                for value in request_gen:
                    self.check_ratelim()
                    yield value
            except GithubException as e:
                print(f'An error occured for {repo.name}')
                err.write(f'AN ERROR OCCURED FOR {repo.name} : \n\n' + str(e) + '\n\n')
            else:
                done = True

if __name__ == '__main__':
    # Just shows off how to use the class
    from github import Github
    GH_TOKEN = os.environ['GITHUB_API_TOKEN'].strip()
    g = Github(GH_TOKEN)
    ghr = GithubRequester(g)
    
    # wrap requests so that we check the ratelim on requests and wait if necessary
    for repo in ghr.wrap_request(g.get_user().get_repos()):
        print(repo.name)
        repo.edit(has_wiki=False)
```


Generate the GITHUB_API_TOKEN by getting this from your profile.

I suppose in a later iteration, it may make more sense to subclass the github perhaps. Or fork PyGithub and make an open source contribution? We'll see.
