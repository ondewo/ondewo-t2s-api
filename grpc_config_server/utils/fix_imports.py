import os


def fix_imports_in_ondewoapis() -> None:
    """
    when generating python files from protos into a subdirectory, there is a known issue with imports
    currently no fix exists, so this fct will fix them
    """
    script_path = os.path.realpath(__file__)
    server_dir_name = script_path.split("ondewo-t2s/")[1].split("/")[0]
    proto_output_dir = f"./{server_dir_name}/ondewo/audio/"
    files = os.listdir(proto_output_dir)
    for file in files:
        if "_pb2_grpc.py" in file:
            path = proto_output_dir + file
            with open(path, "rt") as f:
                data = f.read()
                print(f"    FIXING SUBDIRECTORY IMPORTS IN: {path}")
                data = data.replace("from ondewo.audio import", f"from {server_dir_name}.ondewo.audio import")
            with open(path, "wt") as f:
                f.write(data)


if __name__ == "__main__":
    """called by Makefile when (re)generating protos"""
    fix_imports_in_ondewoapis()
