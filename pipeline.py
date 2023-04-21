from haystack import Pipeline


def get_pipeline(yaml_path: str) -> Pipeline:
    return Pipeline.load_from_yaml(yaml_path, pipeline_name="indexing")


## example usage
# pipeline = get_pipeline("./pipelines/pipeline.yaml")
# documents = pipeline.run(file_paths=[Path(".your-file.txt")])
