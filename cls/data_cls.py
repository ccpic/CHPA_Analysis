import pandas as pd
from typing import Callable, Union
from pandas import DatetimeIndex
import math

# 解决pandas print行列不对齐的问题
pd.set_option("display.unicode.ambiguous_as_wide", True)
pd.set_option("display.unicode.east_asian_width", True)

D_SORTER = {
    "DATE": DatetimeIndex(
        [
            "2017-12-01",
            "2018-03-01",
            "2018-06-01",
            "2018-09-01",
            "2018-12-01",
            "2019-03-01",
            "2019-06-01",
            "2019-09-01",
            "2019-12-01",
            "2020-03-01",
            "2020-06-01",
            "2020-09-01",
            "2020-12-01",
            "2021-03-01",
            "2021-06-01",
            "2021-09-01",
            "2021-12-01",
        ]
    )
}


def format_numbers(
    num_str: str,
    format_str: str,
    else_str: Union[str, None] = None,
    ignore_nan=False,
) -> str:
    """一个函数，帮助格式化数值时忽略非数值化的文本及空值

    Parameters
    ----------
    num_str : str
        原始文本，如df的值
    format_str : str
        格式化字符串，如"{:,.0f}"
    else_str : Union[str, None], optional
        忽略的文本, by default None
    ignore_nan : bool, optional
        是否忽略空值, by default False

    Returns
    -------
    str
        格式化后的结果，可以配合pandas的lambda使用
    """
    if ignore_nan and math.isnan(float(num_str)):
        if else_str is not None:
            num_str = else_str
    else:
        try:
            num_str = format_str.format(num_str)
        except ValueError:
            pass
            if else_str is not None:
                num_str = else_str
    return num_str


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    """根据pandas df的列名格式化该列数值，如出现"份额"字样则格式化为百分比

    Parameters
    ----------
    df : pd.DataFrame
        原始df

    Returns
    -------
    pd.DataFrame
        数值格式化后的df
    """
    format_abs = lambda x: format_numbers(x, "{:,.0f}")
    format_diff = lambda x: format_numbers(x, "{:+,.0f}")
    format_share = lambda x: format_numbers(x, "{:.1%}")
    format_gr = lambda x: format_numbers(x, "{:+.1%}")
    format_currency = lambda x: format_numbers(x, "¥{:,.1f}")
    for col in df.columns:
        if any(x in str(col) for x in ["同比增长", "增长率", "CAGR", "同比变化", "份额变化"]):
            df[col] = df[col].map(format_gr)
        elif (
            any(x in str(col) for x in ["份额", "贡献", "达成", "占比", "覆盖率", "DOT %"])
            and str(col) != "份额变化"
        ):
            df[col] = df[col].map(format_share)
        elif any(x in str(col) for x in ["价格", "单价"]):
            df[col] = df[col].map(format_currency)
        elif any(x in str(col) for x in ["净增长"]):
            df[col] = df[col].map(format_diff)
        else:
            df[col] = df[col].map(format_abs)

    return df


class ChpaAnalyzer(pd.DataFrame):
    @property
    def _constructor(self):
        return ChpaAnalyzer._internal_constructor(self.__class__)

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
        save_path: str = "./plots/",
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
        save_path : str, optional
            绘图等output方法存储的位置, by default "./plots/"
        其他参数为继承自pandas dataframe，不用输入
        """
        super(ChpaAnalyzer, self).__init__(
            data=data, index=index, columns=columns, dtype=dtype, copy=copy
        )
        self.data = data
        self.name = name
        self.date_column = date_column
        self.value_column = value_column
        self.save_path = save_path

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

    def get_kpi(self, column: str, is_formatted: bool = False) -> pd.DataFrame:
        """根据分析目标字段返回透视后的kpi表格，包括以分析目标字段breakout出的各个项目的Rank(变化), MAT金额, 净增长, 份额, 份额变化以及EI

        Parameters
        ----------
        column : str
            分析目标字段，如TC, MOLECULE, PRODUCT, CORPORATION等
        is_formatted : bool, by default False
            是否格式化数值

        Returns
        -------
        pd.DataFrame
            返回一个包含结果的pandas dataframe
        """
        pivoted = self.get_pivot(
            index=self.date_column, columns=column, values="AMOUNT"
        )

        pivoted = pivoted.sort_values(by=pivoted.index[-1], ascending=False, axis=1)
        sr_mat = pivoted.iloc[-1, :]
        sr_ya = pivoted.iloc[-5, :]
        rank_diff = sr_ya.rank(ascending=False) - sr_mat.rank(
            ascending=False
        )  # 最新MAT和Year ago的排名变化
        sr_rank = (
            sr_mat.rank(ascending=False).astype(int).astype(str)
            + "("
            + rank_diff.astype(int).map(lambda x: ("+" if x > 0 else "") + str(x))
            + ")"
        )  # 组合排名字符串，排名变化在最新排名后的括号内呈现
        df_kpi = pd.DataFrame(sr_rank, columns=["Rank"])
        df_kpi["MAT金额"] = pivoted.iloc[-1, :]
        df_kpi["净增长"] = df_kpi["MAT金额"].subtract(sr_ya)
        df_kpi["增长率"] = df_kpi["MAT金额"].div(sr_ya) - 1
        df_kpi["份额"] = df_kpi["MAT金额"] / df_kpi["MAT金额"].sum()
        df_kpi["份额变化"] = df_kpi["份额"] - sr_ya / sr_ya.sum()
        df_kpi["EI"] = (
            (df_kpi["增长率"] + 1) / (df_kpi["MAT金额"].sum() / sr_ya.sum()) * 100
        )  # EI代表该项目增速和整体增速的关系，高于100及快于整体平均

        if is_formatted:
            df_kpi = format_df(df_kpi)

        return df_kpi
