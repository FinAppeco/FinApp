from datetime import datetime
from dagster import AssetMaterialization, AssetKey, MetadataValue


def df_asset_manager(context, obj):

            columns_timestamp = list(obj.select_dtypes(include=['datetime64']).columns)
            obj[columns_timestamp] = obj[columns_timestamp].astype(str)
            dict_metadata = obj.head(1).to_dict(orient='records')

            context.log_event(AssetMaterialization(
                asset_key=AssetKey(
                    context.solid_def.name + ' ' + datetime.now().strftime(format='%Y-%m-%d %H:%M')),
                description="Persisted result to storage.",
                metadata={
                    "Solid name": MetadataValue.text(context.solid_def.name),
                    "number of rows": obj.shape[0],
                    "columns": MetadataValue.text(str(list(obj.columns) if len(obj) > 0 else [])),
                    "sample": MetadataValue.json(data={'data': dict_metadata})
                },
                tags={'asset date': datetime.now().strftime(format='%Y-%m-%d/%H:%M')}
            ))