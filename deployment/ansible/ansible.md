# Introduction
Ansible scripts are called __playbooks__, and written as simple `YAML` files.  
folder hierarchy:
> Playbook folder
> |- variables
> |  |\_ vars
> |- inventory
> |  |\_ inventory.ini
> |- roles
> |  |- files
> |  |- tasks
> |  |  |- task1.yml
> |  |  |\_ task2.yml
> |  |\_ templates
> |\_ playbook.yml

## [Variables](https://www.youtube.com/watch?v=ZAdJ7CdN7DY)
Specify apache version and what port apache shall run on, etc..  

## [Inventories](http://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)
Things you want to automatic, and what hosts that ansible can access to. They can be grouped and
stored in `.ini` file by default.  

``` ansible
    ---
    [web]
    web-1.example.com
    web-2.example.com
    [db]
    db-a.example.com
    db-b.example.com
```

assume we write above lines in `hosts`, then we can test by: [ref](https://www.youtube.com/watch?v=xew7CMkL7jY)

    ansible web -i hosts -m command -a "uptime" -u root --key-file=<key-file>

# Playbooks
**Playbooks** contain **plays**
Plays contain **tasks**
Tasks call **modules**

Tasks run sequentially. **Handlers** are triggered by tasks, and are run once, at the end of plays.

```
    ---
    - name: install and start apache
      hosts: web
      remote_user: ubuntu
      become_method: sudo
      become_user: ubuntu
      vars:
        http_port: 80
        max_clients: 200

      tasks:
      - name: install httpd
        yum: name=httpd state-latest
      - name: write apache config file
        template: src=srv/httpd.j2 dest=/etc/httpd.conf
        notify:
        - restart apache
      - name: start httpd
        service: name-httpd state=running

      handlers:
      - name: restart apache
        service: name=httpd state=restarted
```

* Other youtube resource: [1](https://www.youtube.com/watch?v=ZAdJ7CdN7DY)
## Modules
## How to run
### Ad-Hoc commands
Runs a command or calls a module directly from the command line, no Playbook required.  

    ansible <inventory> <options>
    ansible -i inventory_file -u ubuntu -m shell -a "reboot"

    ansible web -a /bin/date
    ansible web -m ping # call a module
    ansible web -m yum -a "name=openssl state=latest"
### Playbooks
Runs a Playbook on selected inventories from the command line.  

    ansible-playbook <options>

    $ ansible-playbook -i <host-file> -u ubuntu --key-file=<your-key-file> <playbook>
### Check mode
Dry-run for ad-hoc commands and Playbooks.  
Validate Playbook runs before making state changes on target systems.

    ansible web -C -m yum -a "name=httpd state=lastest"
    ansible-playbook -C my-playbook.yml
### Automation Framework
    Ansible Tower
