FROM nvcr.io/nvidia/pytorch:19.10-py3

RUN apt-get -y update && apt-get -y upgrade

# Download NeMo
RUN pip install nemo-toolkit && \
    pip install nemo-asr && \ 
    pip install nemo-nlp && \ 
    pip install nemo-tts 

# Fix NeMo dependencies
RUN pip install Pillow==6.2.2 --force-reinstall

WORKDIR /opt
