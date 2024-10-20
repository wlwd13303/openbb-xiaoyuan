from typing import Any, Dict, List, Optional

import pandas as pd

from jinniuai_data_store.reader import get_jindata_reader
from openbb_core.provider.abstract.fetcher import Fetcher

from openbb_xiaoyuan.standard_models.st_name import StNameQueryParams, StNameData

reader = get_jindata_reader()


class XYStNameQueryParams(StNameQueryParams):
    pass


class XYStNameData(StNameData):
    pass


class XYStNameFetcher(
    Fetcher[
        XYStNameQueryParams,
        List[XYStNameData],
    ]
):
    @staticmethod
    def transform_query(params: Dict[str, Any]) -> XYStNameQueryParams:
        return XYStNameQueryParams(**params)

    @staticmethod
    def extract_data(
        query: XYStNameQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[dict]:
        symbols = query.symbol.split(",")
        start_date = reader.convert_to_db_date_format(query.start_date)
        end_date = reader.convert_to_db_date_format(query.end_date)
        df = reader.get_factors(
            source="6M",
            frequency="1D",
            factor_names=["是否为ST或退市股票"],
            start_date=start_date,
            end_date=end_date,
            symbols=symbols,
        )

        data = df.to_dict(orient="records")
        return data

    @staticmethod
    def transform_data(
        query: XYStNameQueryParams, data: List[dict], **kwargs: Any
    ) -> List[XYStNameData]:
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient="records")
        return [XYStNameData(**d) for d in data]
