# Introduction
## Inventories
things you want to automatic

``` ansible
    ---
    [web]
    web-1.example.com
    web-2.example.com
    [db]
    db-a.example.com
    db-b.example.com
```

# Playbooks
**Playbooks** contain **plays**
Plays contain **tasks**
Tasks call **modules**

Tasks run sequentially
**Handlers** are triggered by tasks, and are run once, at the end of plays.

```
    ---
    - name: install and start apache
      hosts: web
      remote_user: justin

      tasks:
```

## Modules
