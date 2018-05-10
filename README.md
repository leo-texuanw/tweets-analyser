# Cluster_Assign2

## Overview
This is a project for assignment 2 of Cluster and Cloud Computing, semester
one, 2018, The University of Melbourne.  
Here is a link to a [introduction video](https://youtu.be/UMS-4cq4-KQ) of this project.
### Components
- [app](http://115.146.95.248:5985)/ - the front-end website to visulize this application.
- crawler/ - the application to crawl raw data from AURIN API and the Internet
(Twitter API).
- [database](http://115.146.95.248:5984/_utils/)/ - the application to store data (CouchDB, even Hadoop/Spark can be
        considered).
- analyser/ - the application for analysing data.
- deploy/ - for autimate deployment

### Authors
- Nai Wang -            927209 -  naiw1@student.unimelb.edu.au
- Texuan Wu -           984730 -  texuanw@student.unimelb.edu.au
- Siran L1 -            906730 -  siranl2@student.unimelb.edu.au
- Yujing Jiang -        720903 -  yujingj@student.unimelb.edu.au
- Ratih Putri Pertiwi - 969864 -  pertiwir@student.unimelb.edu.au


# DEADLINE - 10<sup>th</sup> May 1 pm
- [\* ] **Twitter harvesting application**, multiple instances are expected ([AURIN](https://portal.aurin.org.au), [AURIN openAPI](https://aurin.org.au/aurin-apis/)).
- [\* ] **CouchDB Database**, by using MapReduce (single node or cluster)
- [\* ] A range of **analytic scenarios**, must support sentiment analysis
- [\* ] A ReSTful **front-end web** application for visulising these data sets/scenarios (25% for these above todos)
- [\* ] (10%) Proper handling of the errors and removal of duplicate tweets.
- [\* ] (25%) **Dynamic deployment**, using [Ansible](http://www.ansible.com/home).
- [\* ] (20%) Detailed documentation on the system architecture and design
- [\* ] (20%) **Collective Report**, including pros and cons of the NeCTAR Research
Cloud and suppoting twitter data analytics, more detail in __Final packaging and
delivery__ part of assignment pdf. (20-25 pages).
- [\* ] A **video** of our system to be uploaded to YouTube.

### Some notice
- Details about each part will be updated in the `README.md` file of each part.
- We can also use OpenStack, Docker, Hadoop, Spark or any pre-existing software
sysmtems. Include sentiment analysis libraries, gender identification libraries, and machine
learning systems as well as front-end Javascript libraries and visualisation
capabilities, e.g. Googlemaps.
- To record all the problems and challenges encountered during thi project are prefered, to make it easier for our final report.
