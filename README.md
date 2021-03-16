# CAD-depth-images-generation
Generate realistic dataset of depth images from CAD models

## Install GP-GAN using a docker container

### Download GP-GAN repository
1. ```cd TO_A_DOWNLOAD_LOCATION```
2. ```git pull https://github.com/wuhuikai/GP-GAN.git```

### Download and install docker
1. ```apt install docker.io```
2. ```docker pull nivida/cuda 10.1-devel-ubuntu18.04```

### Setup NVIDIA container toolkit
To setup container toolkit, go to the [this](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) link and follow the instruction from "Setting up NVIDIA containter toolkit". The last command is using the wrong version, so to test the install with the following command: 
* ```docker run --rm --gpus all nvidia/cuda:10.1-devel-ubuntu18.04 nvidia-smi```

To start container, run:
* ```docker run --it --gpus all -v "PATH TO OUTPUT IMAGES FOLDER":"/imgs", "PATH TO GP_GAN FOLDER":"/gp-gan" nvidia/cuda:10.1-devel-ubuntu18.04```

PATH TO OUTPUT IMAGES FOLDER is the folder where generated images are saved and PATH TO GP_GAN FOLDER is the path to the download loaction of the GP-GAN repository.

### Install python in docker:
The following steps are a modefied version of the steps found [here](https://tecadmin.net/install-python-3-5-on-ubuntu/).

1. ```apt-get update```
2. ```apt-get upgrade```
3. ```apt-get install build-essential checkinstall```
4. ```apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev```
5. ```cd /usr/src```
6. ```apt-get install wget```
7. ```wget https://www.python.org/ftp/python/3.5.9/Python-3.5.9.tgz```
8. ```tar xzf Python-3.5.9.tgz```
9. ```cd Python-3.5.9```
10. ```./configure --enable-optimizations```
11. ```make altinstall```

### Install GP-GAN requirements
1. ```cd ~/../gp-gan```
2. ```pip3.5 install -r requirements/test/requirements.txt```