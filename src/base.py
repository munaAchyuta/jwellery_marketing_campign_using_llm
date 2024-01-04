import yaml

def read_config(file_path):
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(
                f"Error in reading {file_path} file: with exception->{exc}")

    return data

config_file_path = "./config.yaml"
GLOBAL = read_config(config_file_path)


class BaseClass:
    '''
    holds global level attributes.
    '''

    def __init__(self) -> None:
        self.env_vars = GLOBAL
        self.app_name = GLOBAL.get("app_name", "nl_to_sql")
        self.log_path = GLOBAL.get("log_path", None)
        
        self.openai_url = GLOBAL.get("openai_url","https://api.openai.com/v1/completions")
        self.openai_token = GLOBAL.get("openai_token", None)
        self.openai_model = GLOBAL.get("openai_model", "text-davinci-003")
        self.openai_max_token = GLOBAL.get("openai_max_token", 1000)
        self.openai_temperature = GLOBAL.get("openai_temperature", 0.9)

        self.embedding_model = GLOBAL.get('embedding_model','all-MiniLM-L6-v2')
        self.embedding_max_seq_length = GLOBAL.get('embedding_max_seq_length',256)
        self.embedding_size = GLOBAL.get('embedding_size',384)

        self.doc_save_path = GLOBAL.get('doc_save_path')

        self.doc_retrieval_config = GLOBAL.get('doc_retrieval_config')
        #self.logger = logger