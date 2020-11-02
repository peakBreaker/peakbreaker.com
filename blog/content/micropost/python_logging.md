---
title: "Logging with python"
date: 2020-08-19
description: Micropost on python logging
titleWrap: wrap
enableSidebar: false
enableToc: false
tags: ['python', 'logging', 'micropost']
---

## Logging

So this is a simple python script which is useful for me to add logging to my application quickly. Just add this to a file and import it to get the right format.  Add additional logic as needed.  The formatting here works well with stackdriver logging.

```python
#!/usr/bin/env python

"""Logging setup

To use this module, just import it to set up the logger.
It should persist from import across the runtime.

"""

import logging

# Three of my favourite formats for stackdriver
FORMAT1 = '{"severity": "%(levelname)s", "message": "%(message)s", "component": "%(component)s"}'
FORMAT2 = '{"severity": "%(levelname)s", "message": "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"}'
FORMAT3 = '{"severity": "%(levelname)s", "message": "{%(pathname)s:%(lineno)d} - %(message)s"}'

# I prefer format3, as stackdriver had alot built in for time etc already 
logging.basicConfig(format=FORMAT3, level='INFO') # Level is 'WARNING' by default

if __name__ == '__main__':
  logger = logging.getLogger(__name__)
  logger.info('Hello info world')
  logger.warning('Hello warning world')
  logger.error('Hello error world')
```
