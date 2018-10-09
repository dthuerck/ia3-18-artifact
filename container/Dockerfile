FROM nvidia/cuda:9.2-devel-ubuntu18.04

MAINTAINER Daniel Thuerck (dthuerck@culip.org)

# install necessary evil
RUN apt-get update
RUN apt-get -y install wget build-essential gcc gfortran git cmake unzip libhwloc-dev libopenblas-dev liblapacke-dev

# create culip's folder structure
RUN mkdir /culip
RUN mkdir /culip/code
RUN mkdir /culip/data
RUN mkdir /culip/cuda-samples

# download CUDA samples (mainly for helper_cuda.h)
WORKDIR /culip/cuda-samples
RUN git clone https://github.com/NVIDIA/cuda-samples.git .

# clone culip code and build
WORKDIR /culip/code
RUN git clone https://github.com/dthuerck/culip.git .
WORKDIR /culip/code/build
RUN /bin/bash -c "cmake -DCMAKE_BUILD_TYPE=Release -DCUDA_SDK_ROOT_DIR=/culip/cuda-samples .. && make || make"

# download benchmark data from IA3
ADD http://download.hrz.tu-darmstadt.de/media/FB20/GCC/project_files/culip/ia3_2018/ia3-2018-data.zip /culip/data
RUN cd /culip/data && unzip ia3-2018-data.zip && rm ia3-2018-data.zip

# add volume to interface with host data
WORKDIR /culip/external
