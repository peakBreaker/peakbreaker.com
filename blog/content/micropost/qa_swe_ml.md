---
title: "Smarter QA"
date: 2020-11-06
description: Micropost on doing QA using various tools
titleWrap: wrap
enableSidebar: false
enableToc: false
---

## Quality Assurance in Software Engineering

There are some timeless classics when it comes to quality assurance of codebases:
- Write tests
- Do code review

But other than that, here are some tools and techniques for analyzing
a codebase and doing smarter software development:

### Static code analysis

- Count lines of code (cloc)
- https://radon.readthedocs.io/en/latest/
- https://gource.io/
- `find -iname '.' | xargs cat |sed -e 's/^[ \t]//' | sort | uniq -c | sort -nr`
- https://github.com/src-d 

Use some python magic:

```python
from subprocess import check_output
files = check_output('find -iname *.<type>'.split())\
       .decode().splitlines()
from itertools import chain
from collections import Counter
Counter(chain.from_iterable(open(f).read().split() for f in files)).most_common()


from keyword import iskeyword
from tokenizer import tokenizer
Counter(
  chain.from_iterable((t.string for t in tokenize(open(f, 'rb').readline)
    if len(t.string) > 5 and t.string.strip() and t.string.isalnum() and not iskeyword(t.string))
    for f in files)
  ).most_common()
```

Check imports

```python
#!/usr/bin/env python3

import distutils.sysconfig as sysconfig
import os
import sys
import subprocess

def build_std_lib_stoplist():
    std_lib_stoplist = []
    std_lib = sysconfig.get_python_lib(standard_lib=True)

    for top, dirs, files in os.walk(std_lib):
        for nm in files:
            prefix = top[len(std_lib)+1:]
            if prefix[:13] == 'site-packages':
                continue
            if nm == '__init__.py':
                std_lib_stoplist.append(top[len(std_lib)+1:].replace(os.path.sep,'.'))
            elif nm[-3:] == '.py':
                std_lib_stoplist.append(os.path.join(prefix, nm)[:-3].replace(os.path.sep,'.'))
            elif nm[-3:] == '.so' and top[-11:] == 'lib-dynload':
                std_lib_stoplist.append(nm[0:-3])

    return [*[f' {s} ' for s in std_lib_stoplist],
            *[f' {s},' for s in std_lib_stoplist]]

def stoplist_match(_stoplist, value):
    for s in _stoplist:
        if s in value:
            return False
    else:
        return True

def get_most_used():
    _mostused_raw = subprocess.check_output("find -iname '*.py' | xargs cat |sed -e 's/^[ \t]*//'  | sort | uniq -c | sort -nr | sed -e 's/^[ \t]*//'", shell=True).decode().split('\n')
    print(f'raw : {_mostused_raw[:5]}')
    return list(filter(lambda x: x is not None,
        [(int(m.split(' ')[0]), ' '.join(m.split(' ')[1:]))
            if m.split(' ')[0].isdigit() else None 
            for m in _mostused_raw]))

if __name__ == '__main__':
    imports = list(filter(lambda x: x is not None, 
        [v if 'import' in v[1] else None for v in get_most_used()]))

    stoplist = build_std_lib_stoplist()
    # Filter against stoplist
    user_imports = list(filter(lambda x: stoplist_match(stoplist, x[1]+' '), imports))
    total_imports = 0
    for i in user_imports:
        print(f'{i[1].split(" ")[-1]} imported {i[0]} times')
        total_imports+=i[0]

    print(f'Total user imports : {total_imports}')
```

Use this together with cloc to figure out imports per LoC. My code is typically around 0.05 imports per LoC

### Dynamic analysis

- Use strace to see syscalls used https://strace.io/
- Monkeypatch os.environ:

```python
import os
from sys import stderr
class debug(dict):
  def get(self, item):
    stderr.write(f'{item}\n')
    return super().get(item)
  def __getitem__(self, item):
    stderr.write(f'{item}\n')
    return supert().__getitem__(item)
  # ...
os.environ = debug(os.environ)
```

Use linetracer:
```python
from collections import Counter
hist = Counter()
def trace(f, *_):
  hist[frame.f_code.co_filename, frame.f_fileno] += 1
from sys import settrace
settrace(trace)
# ...
hist.most_common(10)
```

### Testing

Use the testing framework most applicable to your stack, though in python it is
advisable to use pytest:

- https://docs.pytest.org/en/stable/
- Coverage : https://pypi.org/project/pytest-cov/

### Performance
- docker stats
```shell
docker stats --no-stream \
  --format "{\"container\": \"{{ .Container }}\", \"memory\": { \"raw\": \"{{ .MemUsage }}\", \"percent\": \"{{ .MemPerc }}\"}, \"cpu\": \"{{ .CPUPerc }}\"}"
```
