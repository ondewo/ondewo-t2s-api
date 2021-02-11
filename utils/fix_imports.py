import argparse
import os


def fix_imports_in_ondewoapis(server_dir_name: str) -> None:
    """
    when generating python files from protos into a subdirectory, there is a known issue with imports
    currently no fix exists, so this fct will fix them
    INFO: https://github.com/protocolbuffers/protobuf/pull/7470
    """

    proto_output_dir = f"./{server_dir_name}/ondewo/t2s/"
    files = os.listdir(proto_output_dir)
    for file in files:
        if "_pb2_grpc.py" in file:
            path = proto_output_dir + file
            with open(path, "rt") as f:
                data = f.read()
                print(f"    FIXING SUBDIRECTORY IMPORTS IN: {path}")
                data = data.replace("from ondewo.t2s import", f"from {server_dir_name}.ondewo.t2s import")
            with open(path, "wt") as f:
                f.write(data)


if __name__ == "__main__":
    """called by Makefile when (re)generating protos"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-sp', '--server_path',
        help='Path of the grpc server.',
        required=True,
    )

    args = parser.parse_args()

    fix_imports_in_ondewoapis(args.server_path)
