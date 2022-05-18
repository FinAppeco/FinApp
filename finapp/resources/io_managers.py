from dagster import Field, StringSource, io_manager

from finapp.resources.parquetgcsiomanager import ParquetGCSIOManager, JsonGCSIOManager


@io_manager(config_schema={
        "gcs_bucket": Field(StringSource),
        "gcs_prefix": Field(StringSource, is_required=False, default_value="dagster"),
    },
    required_resource_keys={"gcs"},)
def gcs_parquet_io_manager(init_context):
    """Built-in filesystem IO manager that stores as a parquet file and retrieves values as Dataframe.

    Allows users to specify a base directory where all the step outputs will be stored. By
    default, step outputs will be stored in the directory specified by local_artifact_storage in
    your dagster.yaml file (which will be a temporary directory if not explicitly set).

    Example usage:

    1. Specify a pipeline-level IO manager using the reserved resource key ``"io_manager"``,
    which will set the given IO manager on all solids across a pipeline.

    .. code-block:: python

        @solid
        def solid_a(context, df):
            return df

        @solid
        def solid_b(context, df):
            return df[:5]

        @pipeline(
            mode_defs=[ModeDefinition(resource_defs={
            "io_manager": parquet_io_manager.configured({"base_path": "/my/base/path"})
                    }
                )
            ]
        )
        def pipe():
            solid_b(solid_a())


    2. Specify IO manager on :py:class:`OutputDefinition`, which allows the user to set
    different IO managers on different step outputs.

    .. code-block:: python

        @solid(output_defs=[OutputDefinition(io_manager_key="my_io_manager")])
        def solid_a(context, df):
            return df

        @solid
        def solid_b(context, df):
            return df[:5]

        @pipeline(
            mode_defs=[ModeDefinition(resource_defs={"my_io_manager": parquet_io_manager})]
        )
        def pipe():
            solid_b(solid_a())

    """
    client = init_context.resources.gcs
    parquet_io_manager = ParquetGCSIOManager(
        init_context.resource_config["gcs_bucket"],
        client,
        init_context.resource_config["gcs_prefix"],
    )
    return parquet_io_manager

@io_manager(
    config_schema={
        "gcs_bucket": Field(StringSource),
        "gcs_prefix": Field(StringSource, is_required=False, default_value="dagster"),
    },
    required_resource_keys={"gcs"},
)
def gcs_json_io_manager(init_context):
    """Persistent IO manager using GCS for storage.

    Serializes objects via pickling. Suitable for objects storage for distributed executors, so long
    as each execution node has network connectivity and credentials for GCS and the backing bucket.

    Attach this resource definition to a :py:class:`~dagster.ModeDefinition`
    in order to make it available to your pipeline:

    .. code-block:: python

        pipeline_def = PipelineDefinition(
            mode_defs=[
                ModeDefinition(
                    resource_defs={'io_manager': gcs_pickle_io_manager, 'gcs': gcs_resource, ...},
                ), ...
            ], ...
        )

    You may configure this storage as follows:

    .. code-block:: YAML

        resources:
            io_manager:
                config:
                    gcs_bucket: my-cool-bucket
                    gcs_prefix: good/prefix-for-files-
    """
    client = init_context.resources.gcs
    json_io_manager = JsonGCSIOManager(
        init_context.resource_config["gcs_bucket"],
        client,
        init_context.resource_config["gcs_prefix"],
    )
    return json_io_manager