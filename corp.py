from sqlalchemy import create_engine
import pandas as pd
from typing import Callable

D_SORTER = {}


class CorpAnalyzer(pd.DataFrame):
    @property
    def _constructor(self):
        return CorpAnalyzer._internal_constructor(self.__class__)

    class _internal_constructor(object):
        def __init__(self, cls):
            self.cls = cls

        def __call__(self, *args, **kwargs):
            kwargs["name"] = None
            kwargs["date_column"] = None
            kwargs["value_column"] = None
            return self.cls(*args, **kwargs)

        def _from_axes(self, *args, **kwargs):
            return self.cls._from_axes(*args, **kwargs)

    def __init__(
        self,
        data: pd.DataFrame,
        name: str,
        date_column: str = "DATE",
        value_column: str = "AMOUNT",
        savepath: str = "./plots/",
        index=None,
        columns=None,
        dtype=None,
        copy=True,
    ):
        """初始化对象

        Parameters
        ----------
        data : pd.DataFrame
            一个pandas df数据
        name : str
            数据名，用于一些output存储的命名以及绘图指标的标题
        date_column : str, optional
            指定日期列，作为大部分数据透视时的行, by default "DATE"
        value_column : str, optional
            指定数值列，作为大部分数据透视时的值, by default "AMOUNT"
        savepath : str, optional
            绘图等output方法存储的位置, by default "./plots/"
        其他参数为继承自pandas dataframe，不用输入
        """
        super(CorpAnalyzer, self).__init__(
            data=data, index=index, columns=columns, dtype=dtype, copy=copy
        )
        self.data = data
        self.name = name
        self.date_column = date_column
        self.value_column = value_column
        self.savepath = savepath

    # 透视
    def get_pivot(
        self,
        index: str = None,
        columns: str = None,
        values: str = None,
        aggfunc: Callable = sum,  # 默认求和
        query_str: str = "ilevel_0 in ilevel_0",  # 默认query语句能返回df总体
        perc: bool = False,
        sort_values: bool = True,
        dropna: bool = True,
        fillna: bool = True,
        **kwargs,
    ) -> pd.DataFrame:
        """返回数据透视的结果

        Parameters
        ----------
        index : str, optional
            数据透视表的行, by default None
        columns : str, optional
            数据透视表的列, by default None
        values : str, optional
            数据透视表的值, by default None
        aggfunc : Callable, optional
            数据透视表的汇总方式, by default sum
        query_str: str, optional
            筛选的数据范围，类似sql写法, by default "ilevel_0 in ilevel_0"
        per: bool, optional
            是否转换为行汇总的百分比, by default False
        sort_values : bool, optional
            是否排序，如是按照行/汇总总和大小排序, by default True
        dropna : bool, optional
            是否去除空值，如是将把全部为空整行/列去除, by default True
        fillna : bool, optional
            是否替换空值，如是将空值替换为0, by default True

        Returns
        -------
        pd.DataFrame
            一个透视后的pandas df
        """

        kwargs = kwargs.copy()

        pivoted = pd.pivot_table(
            self.query(query_str),
            values=values,
            index=index,
            columns=columns,
            aggfunc=aggfunc,
        )
        # pivot table对象转为默认df
        pivoted = pd.DataFrame(pivoted.to_records())
        try:
            pivoted.set_index(index, inplace=True)
        except KeyError:  # 当index=None时，捕捉错误并set_index("index"字符串)
            pivoted.set_index("index", inplace=True)

        if sort_values is True:
            s = pivoted.sum(axis=1).sort_values(ascending=False)
            pivoted = pivoted.loc[s.index, :]  # 行按照汇总总和大小排序
            s = pivoted.sum(axis=0).sort_values(ascending=False)
            pivoted = pivoted.loc[:, s.index]  # 列按照汇总总和大小排序

        if columns in D_SORTER:
            pivoted = pivoted.reindex(columns=D_SORTER[columns])

        if index in D_SORTER:
            pivoted = pivoted.reindex(D_SORTER[index])  # 对于部分变量有固定排序

        # 删除NA或替换NA为0
        if dropna is True:
            pivoted = pivoted.dropna(how="all")
            pivoted = pivoted.dropna(axis=1, how="all")
        else:
            if fillna is True:
                pivoted = pivoted.fillna(0)

        if perc is True:
            pivoted = pivoted.div(pivoted.sum(axis=1), axis=0)  # 计算行汇总的百分比

        return pivoted



if __name__ == "__main__":
    engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
    table_name = "data"

    condition = "[TC II] = 'C09 RENIN-ANGIOTEN SYST AGENT|作用于肾素-血管紧张素系统的药物'"
    if condition is None:
        sql = f"SELECT * FROM {table_name} WHERE UNIT = 'Value' AND PERIOD = 'MAT'"
    else:
        sql = f"SELECT * FROM {table_name}  WHERE UNIT = 'Value' AND PERIOD = 'MAT' AND {condition}"

    df = pd.read_sql(sql=sql, con=engine)

    c = CorpAnalyzer(data=df, name="CV领域")

    index = "DATE"
    pivoted = c.get_pivot(index=index, columns="CORPORATION", values="AMOUNT")

    pivoted = pivoted.sort_values(by=pivoted.index[-1], ascending=False, axis=1)
    print(pivoted.iloc[-1, :].index)
