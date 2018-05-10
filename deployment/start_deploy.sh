# Start Crawler
cd ./boto
python3 main.py CRAWLER_WEB 1

cd ../ansible
ansible-playbook -i hosts --key-file=~/.ssh/nectar.key -u ubuntu start_crawler_web.yaml

# Start analyser
cd ../boto
python3 main.py DB_ANALYSER 1 vol-37379a33

cd ../ansible
ansible-playbook -i hosts --key-file=~/.ssh/nectar.key -u ubuntu start_analyser.yaml

# Start Web
cd ../boto
python3 main.py CRAWLER_WEB 1

cd ../ansible/
ansible-playbook -i hosts --key-file=~/.ssh/nectar.key -u ubuntu start_crawler_web.yaml
