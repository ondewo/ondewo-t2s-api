# Ondewo Text-2-Speech

Repository containing code for training and deployment of ONDEWO text synthesis (text-2-speech) models.

### Organization

The repository is organized into several folders. Main folders are:

- __training:__ scripts for data processing and training t2s models
- __rest_server:__ HTTP server which takes text as input and returns synthesized speech
- __inference:__ model inference code
- __config:__ configuration for server and inference
- __models:__ t2s models and model configs
- __normalization:__ normalization of text for text-2-speech

### Inference

There are two ways to run the rest server, depending on the type of inference you want to use. The two types of inference are:

- __NeMo inference__ (inference directly in PyTorch using NeMo)
- __Triton inference__ (inference using Triton inference server)

It is suggested to use NeMo inference for deveopment/testing and Triton inference for production.
You can set the type of inference in the config. For NeMo inference, make sure you have the models present locally (in the `models` folder.)
For Triton inference, make sure that Triton server is running with the required models.

### How to Run in Docker

Before running the server, depening on the type of inference you want to use, either make sure you have the models locally or start the Triton server.

To run the rest server, build the image by `make build_rest_server` and then run the server by `make run_rest_server`
You can now try the server by going to  `http://0.0.0.0:50550`

Check if the server is working by running `docker logs -f ondewo-t2s-rest-server`.

Try out inference by running `curl -X POST --form "text=Hallo User wie geht es dir? Was hast du heute gemacht?" http://0.0.0.0:50550/text2speech > sample.wav`.

### How to Run Locally

If you just want to use the servers, it is recommended to run them in Docker. Run locally only for development purposes.

Create a new conda environment (which you are going to use for development of this repository), then install all dependencies locally by doing `make install_dependencies_locally`.

When this is all done, use the following commands to start the servers
(you'll need to run these commands from the project root):

__Rest server:__ `export PYTHONPATH="${PWD}" && export FLASK_APP=rest_server && export CONFIG_FILE=config/config.yaml && python -m flask run --host=0.0.0.0 --port=50550`

__Streaming server:__ `export PYTHONPATH="${PWD}" && python streaming_server/server.py`

__Demo server:__ `export PYTHONPATH="${PWD}" && export FLASK_APP=demo_server &&  flask run --host=0.0.0.0 --port=40012`

### Development Guide

Once you are done implementing a feature, follow the procedure below (activate the model you want to e2e test in config/config.yaml):
1. Run `make build_rest_server` to build the inference server
2. Run `make run_rest_server` to start the server and `docker logs -f ondewo-t2s-rest-server` to connect to the logs stream
3. Run all python tests in your IDE or in docker with `make run_tests`
4. Once you are done with testing, kill the server by running `docker kill ondewo-t2s-rest-server`
5. Repeat the above steps for `release` (cythonized) version of the server
6. Stage changes, run `pre-commit run` and fix all the inconsistencies
7. Commit+push your code and make sure the Jenkins pipeline is <span style="color:green">GREEN</span>
8. Merge __develop__ into your feature branch and resolve conflicts
9. Create a PR to __develop__ branch and tick "delete feature branch"

### Ports used

- Triton gRPC: 50511
- Triton Rest: 50510
- Rest Server: 50550
- gRPC Server: 50555