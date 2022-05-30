import os
from collections import Counter
from venv import logger

import pandas as pd
from dagster.utils import mkdir_p

from finapp.resources.asset_manager import df_asset_manager


def upload_parquet_gcs(context, obj, key, bucket_obj):
    """

    """
    if isinstance(obj, dict):
        obj = pd.DataFrame(obj)
    if isinstance(obj, pd.DataFrame):
        context.log.info(f"rows: {len(obj)}")
        try:
            temp_parquet = os.path.join(os.getcwd(), 'temp_parquet_manager', '/'.join(key.split('/')[:-1]))
            mkdir_p(temp_parquet)
            temp_parquet = os.path.join(temp_parquet, key.split('/')[-1])
            obj.to_parquet(path=temp_parquet, use_deprecated_int96_timestamps=True, engine='pyarrow')
            if os.path.exists(temp_parquet):
                try:
                    bucket_obj.blob(key).upload_from_filename(temp_parquet)
                except Exception as e:
                    raise e
            df_asset_manager(context, obj)
        except ValueError as e:
            columns = Counter(obj.columns).most_common()
            # parquet doesn't allow have duplicated name fields in the same file
            columns_duplicated = [column[0] for column in columns if column[1] > 1]
            msg = str(columns_duplicated) + ' These columns are duplicated. One value is possibly repeated in ' \
                                            'the yaml file. Check the section for the solid "{solid_name}"'.format(
                solid_name=context.solid_def.name)
            logger.error(msg)
            raise ValueError(msg)