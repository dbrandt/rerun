# `rerun.py`
A simple script that tries to recreate an approximate docker run command from the metadata of a running container.

It's naïve, not complete and it's not tested in very many situations. If you want to extend it, please do. I'll accept any pull request within the scope.

```
% ./rerun.py
Recreate an approximate docker run-command from a running container.

  ./rerun.py <container_id>
```

Be careful out there.
