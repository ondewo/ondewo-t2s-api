import argparse

from grpc_server.server import Server

parser = argparse.ArgumentParser()
parser.add_argument(
    '-p', '--port',
    help='Port of the server.',
    required=True,
)
parser.add_argument(
    '-h', '--host',
    help='Host of the server.',
    required=True,
)
args = parser.parse_args()
server = Server(host=args.host, port=args.port)
server.run()
