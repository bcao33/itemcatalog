# Item Catalog Project

## Objective
This application will provide a list of item within a set of categories. The items will have descriptions and the application will allow for registration and authentication.

## Requirements
To get started with the project, you'll need the following tools.
1. [Python3](https://www.python.org/downloads/)
2. [Vagrant](https://www.vagrantup.com/)
3. [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
4. [VM Configuration](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
5. The files provided in this Zip download

## Installation
Follow the steps below to get started:
1. Download and install the latest version of Python3, Vagrant, VirtualBox and Git using the links above.
2. Using the VM Configuration link above, unpack the zip file and it will give you a directory. cd into the directory to the 'vagrant' folder.
3. Using GIT in a terminal, you can use `vagrant up` to initialize the VM.
4. Once the VM is finished installing, you can use `vagrant ssh` to get into the VM.
5. In the terminal, run `python3 database_setup.py` to create the database.
6. In the terminal, run `python3 populate_database.py` to populate the database with data.
7. In the terminal, run `python3 application.py` to start the application on port 5000.
8. From any browser, go to `http://localhost:5000` to access the application. 
