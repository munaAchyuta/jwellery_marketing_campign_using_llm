import yaml

def read_config(file_path):
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(
                f"Error in reading {file_path} file: with exception->{exc}")

    return data