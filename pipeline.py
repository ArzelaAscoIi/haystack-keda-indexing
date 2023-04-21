from haystack import Pipeline


def get_pipeline(yaml_path: str) -> Pipeline:
    return Pipeline.load_from_yaml(yaml_path, pipeline_name="indexing")
