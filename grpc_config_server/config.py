
PORT = 7777

# path to active config in project directory (copy of config in ./models/ directory)
ACTIVE_CONFIG_YAML = "./config/config.yaml"

# path to config.yaml in model config
# -> ./models/<company>/<language>/<domain>/<speaker>/<model config>$CONFIG_YAML_PATH
CONFIG_YAML_RELATIVE = "/config/config.yaml"

# name of deployed t2s server (not grpc managing server)
T2S_CONTAINER_NAME = "ondewo-t2s-batch-server"
