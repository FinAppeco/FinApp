from typing import Dict, List, NamedTuple, Optional, Mapping, Any
import os
import yaml
import copy

from glob import glob
import dagster._check as check
from dagster._utils.merger import deep_merge_dicts


def load_yaml_from_path(path: str) -> object:
    check.str_param(path, "path")
    with open(path, "r", encoding="utf8") as ff:
        return yaml.safe_load(ff)


def merge_yamls(file_list):
    """Combine a list of YAML files into a dictionary.
    Args:
        file_list (List[str]): List of YAML filenames
    Returns:
        dict: Merged dictionary from combined YAMLs
    Raises:
        yaml.YAMLError: When one of the YAML documents is invalid and has a parse error.
    """
    check.list_param(file_list, "file_list", of_type=str)

    merged = {}

    for yaml_file in file_list:
        yaml_dict = load_yaml_from_path(yaml_file) or {}

        check.invariant(
            isinstance(yaml_dict, dict),
            (
                "Expected YAML from file {yaml_file} to parse to dictionary, "
                'instead got: "{yaml_dict}"'
            ).format(yaml_file=yaml_file, yaml_dict=yaml_dict),
        )
        merged = deep_merge_dicts(merged, yaml_dict)

    return merged


def deep_merge_dicts(onto_dict: dict, from_dict: Mapping) -> dict:
    """
    Returns a recursive union of two input dictionaries:
    * The returned dictionary has an entry for any key that's in either of the inputs.
    * For any key whose value is a dictionary in both of the inputs, the returned value will
      be the result of deep-merging the two input sub-dictionaries.
    If from_dict and onto_dict have different values for the same key, and the values are not both
    dictionaries, the returned dictionary contains the value from from_dict.
    """
    onto_dict = copy.deepcopy(onto_dict)
    check.dict_param(from_dict, "from_dict")
    check.dict_param(onto_dict, "onto_dict")

    for from_key, from_value in from_dict.items():
        if from_key not in onto_dict:
            onto_dict[from_key] = from_value
        else:
            onto_value = onto_dict[from_key]

            if isinstance(from_value, dict) and isinstance(onto_value, dict):
                onto_dict[from_key] = _deep_merge_dicts(onto_value, from_value)
            else:
                onto_dict[from_key] = from_value  # smash

    return onto_dict


def config_from_files(config_files: List[str]) -> Dict[str, Any]:
    """Constructs run config from YAML files.
    Args:
        config_files (List[str]): List of paths or glob patterns for yaml files
            to load and parse as the run config.
    Returns:
        Dict[str, Any]: A run config dictionary constructed from provided YAML files.
    Raises:
        FileNotFoundError: When a config file produces no results
        DagsterInvariantViolationError: When one of the YAML files is invalid and has a parse
            error.
    """
    config_files = check.opt_list_param(config_files, "config_files")

    filenames = []
    for file_glob in config_files or []:
        globbed_files = glob(file_glob)
        if not globbed_files:
            raise ValueError(
                'File or glob pattern "{file_glob}" for "config_files" '
                "produced no results.".format(file_glob=file_glob)
            )

        filenames += [os.path.realpath(globbed_file) for globbed_file in globbed_files]

    try:
        run_config = merge_yamls(filenames)
    except yaml.YAMLError as err:
        raise ValueError(
            f"Encountered error attempting to parse yaml. Parsing files {filenames} "
            f"loaded by file/patterns {config_files}."
        ) from err

    return run_config


class PresetDefinition(
    NamedTuple(
        "_PresetDefinition",
        [
            ("name", str),
            ("run_config", Optional[Dict[str, object]]),
        ],
    )
):
    """Defines a preset configuration in which a pipeline can execute.
    Presets can be used in Dagit to load predefined configurations into the tool.
    Presets may also be used from the Python API (in a script, or in test) as follows:
    .. code-block:: python
        execute_pipeline(pipeline_def, preset='example_preset')
    Presets may also be used with the command line tools:
    .. code-block:: shell
        $ dagster pipeline execute example_pipeline --preset example_preset
    Args:
        name (str): The name of this preset. Must be unique in the presets defined on a given
            pipeline.
        run_config (Optional[dict]): A dict representing the config to set with the preset.
            This is equivalent to the ``run_config`` argument to :py:func:`execute_pipeline`.
    """

    def __new__(
            cls,
            name: str,
            run_config: Optional[Dict[str, object]] = None,
    ):

        return super(PresetDefinition, cls).__new__(
            cls,
            name=name,
            run_config=run_config
        )

    @staticmethod
    def from_files(name, config_files=None):
        """Static constructor for presets from YAML files.
        Args:
            name (str): The name of this preset. Must be unique in the presets defined on a given
                pipeline.
            config_files (Optional[List[str]]): List of paths or glob patterns for yaml files
                to load and parse as the run config for this preset.
        Returns:
            PresetDefinition: A PresetDefinition constructed from the provided YAML files.
        Raises:
            DagsterInvariantViolationError: When one of the YAML files is invalid and has a parse
                error.
        """
        check.str_param(name, "name")
        config_files = check.opt_list_param(config_files, "config_files")

        merged = config_from_files(config_files)

        return PresetDefinition(name, merged)

    def get_environment_yaml(self):
        """Get the environment dict set on a preset as YAML.
        Returns:
            str: The environment dict as YAML.
        """
        return yaml.dump(self.run_config or {}, default_flow_style=False)

    def with_additional_config(self, run_config):
        """Return a new PresetDefinition with additional config merged in to the existing config."""

        check.opt_nullable_dict_param(run_config, "run_config")
        if run_config is None:
            return self
        else:
            initial_config = self.run_config or {}
            return PresetDefinition(
                name=self.name,
                run_config=deep_merge_dicts(initial_config, run_config),
            )
