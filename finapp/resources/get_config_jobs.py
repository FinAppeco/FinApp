import os
from pathlib import Path
from dagster_gcp import gcs_file_manager
from dagster_gcp.gcs import gcs_pickle_io_manager, gcs_resource
from dagster import PresetDefinition
from dagster import fs_io_manager, mem_io_manager
import dagstermill as dm
from finapp.resources.io_managers import gcs_parquet_io_manager

IO_MANAGER = {"parquet_manager": gcs_parquet_io_manager, 'fs_manager': fs_io_manager,
              'mem_manager': mem_io_manager, 'gcs_pickle_io_manager': gcs_pickle_io_manager,
              'gcs': gcs_resource, 'gcs_filemanager': gcs_file_manager,
              "output_notebook_io_manager": dm.local_output_notebook_io_manager}


class PipelineConfiguration:
    """
    Use this class to get the YAML configuration to specific ETL/PIPELINE, It has a PRESET.
    Each preset can have several MODE. Use MODE to define the resources used by the preset.
    """

    def __init__(self, name: str, config_folder: str = 'config_pipelines', resource: dict = None):
        self.path_config = os.path.join(Path(__file__).parent.parent, 'pipelines', config_folder)
        self.name = name
        if resource is not None:
            self.additional_resources = {**resource, **IO_MANAGER}
        else:
            self.additional_resources = {**IO_MANAGER}

    def get_io_managers(self):
        """Helper function to get io_manager available"""
        return self.additional_resources

    def get_preset(self, name_yaml: str):
        """Get the preset given by the name and the path of YAML file"""
        config_files_path = os.path.join(self.path_config, name_yaml)
        return PresetDefinition.from_files(name=self.name, config_files=[config_files_path], mode='none').run_config
