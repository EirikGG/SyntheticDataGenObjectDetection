# Install tools used to enhance images
Tools used to enhance images are projects created by others and are therefore installed with docker to contain the custom versions. The following steps describe installing docker, add python to it, and to run an image. Next induvidual install steps are listed. Some steps may not be required, they should serve as a recreation of what has been done and not a tutorial.

## Download and install docker
1. ```apt install docker.io```
2. ```docker pull cupy/cupy:v6.3.0```

## Setup NVIDIA container toolkit
To setup container toolkit, go to the [this](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) link and follow the instruction from "Setting up NVIDIA containter toolkit". The last command is using the wrong version, so to test the install with the following command: 
* ```docker run --rm --gpus all cupy/cupy:v6.3.0 nvidia-smi```

## Install python3.5 in docker container:
The following steps are a modefied version of the steps found [here](https://tecadmin.net/install-python-3-5-on-ubuntu/) and should be done in a running docker container.

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

# Install GP-GAN

GP-GAN is a system created by Hui-Kai Wu, github user wuhuikai, to blend parts of one image together with another based on a mask. It is used in this project to add background to the generated images. The following tutorial is a replication of the steps used to install the system and to use it to complete the dataset generation.


## Download GP-GAN repository
1. ```cd TO_A_DOWNLOAD_LOCATION```
2. ```git pull https://github.com/wuhuikai/GP-GAN.git```
3. Download pre-trained models from [Google drive](https://drive.google.com/drive/folders/0Bybnpq8dvwudVjBHNWNHUmVSV28).
4. Extract models to GP-GAN models folder

To start container, run:
* ```docker run --it --gpus all -v "PATH TO OUTPUT IMAGES FOLDER":"/imgs", "PATH TO GP_GAN FOLDER":"/gp-gan" cupy/cupy:v6.3.0```

PATH TO OUTPUT IMAGES FOLDER is the folder where generated images are saved and PATH TO GP_GAN FOLDER is the path to the download loaction of the GP-GAN repository.


## Install GP-GAN requirements
1. ```cd ~/../gp-gan```
2. ```pip3.5 install -r requirements/test/requirements.txt```

## Fix cupy install
* ```pip3.5 uninstall cupy==6.3.0```

## Train
1. Download "outdoor_64.hdf5" from [the github link](http://efrosgans.eecs.berkeley.edu/iGAN/datasets/outdoor_64.zip)
2. ```apt-get install libhdf5-dev```
3. ```pip3.5 install -U git+https://github.com/mila-udem/fuel.git#egg=fuel```


# Install Deep Image Blending

## Download and install docker
1. ```apt install docker.io```
2. ```docker pull nvidia/cuda:10.1-devel-ubuntu18.04```

## Download DeepImageBlending repository
1. ```cd TO_A_DOWNLOAD_LOCATION```
2. ```git pull https://github.com/owenzlz/DeepImageBlending```

## Run docker 
* ```sudo docker run -it --gpus all -v "PATH_TO_DEEPIMAGEBLENDING_REPO":"/dim" nvidia/cuda:10.1-devel-ubuntu18.04```

## Install requirements (repo do not provide a requirements file)
1. ```pip3.5 install numpy```
2. ```pip3.5 install torch```
3. ```pip3.5 install pillow```
4. ```pip3.5 install matplotlib```
5. ```pip3.5 install scikit-image```
6. ```pip3.5 install scikit-build```
7. ```pip3.5 install cmake```
8. ```pip3.5 install opencv-python```
9. ```pip3.5 install torchvision```
10. ```pip3.5 install aiohttp```

## Download model
* ```python3.5 run.py```

## Test install
