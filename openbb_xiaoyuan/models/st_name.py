"""XiaoYuan ST Name Model."""

from typing import Any, Dict, List, Optional

import pandas as pd

from jinniuai_data_store.reader import get_jindata_reader
from openbb_core.provider.abstract.fetcher import Fetcher

from openbb_xiaoyuan.standard_models.st_name import StNameQueryParams, StNameData

reader = get_jindata_reader()


class XiaoYuanStNameQueryParams(StNameQueryParams):
    """XiaoYuan ST Name Query."""

    ...


class XiaoYuanStNameData(StNameData):
    """XiaoYuan ST Name Data."""

    __alias_dict__ = {"is_st": "是否为ST或退市股票"}


class XiaoYuanStNameFetcher(
    Fetcher[
        XiaoYuanStNameQueryParams,
        List[XiaoYuanStNameData],
    ]
):
    """Transform the query, extract and transform the data from the XiaoYuan Finance endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> XiaoYuanStNameQueryParams:
        """Transform the query parameters."""

        return XiaoYuanStNameQueryParams(**params)

    @staticmethod
    def extract_data(
        # pylint: disable=unused-argument
        query: XiaoYuanStNameQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[dict]:
        """Extract the data from the XiaoYuan Finance endpoints."""

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
        df = df.sort_values(by="timestamp", ascending=False)
        data = df.to_dict(orient="records")
        return data

    @staticmethod
    def transform_data(
        # pylint: disable=unused-argument
        query: XiaoYuanStNameQueryParams,
        data: List[dict],
        **kwargs: Any,
    ) -> List[XiaoYuanStNameData]:
        """Transform the data."""

        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient="records")
        return [XiaoYuanStNameData.model_validate(d) for d in data]