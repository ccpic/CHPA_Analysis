from regex import P
from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"


d_rename = {
    ("MOLECULE", "氯沙坦钾"): "氯沙坦",
    ("MOLECULE", "氯沙坦钾氢氯噻嗪"): "氯沙坦氢氯噻嗪",
    ("MOLECULE", "奥美沙坦酯氢氯噻嗪"): "奥美沙坦氢氯噻嗪",
    ("MOLECULE", "培哚普利叔丁胺"): "培哚普利",
    ("MOLECULE", "贝那普利,氨氯地平"): "贝那普利氨氯地平",
    ("MOLECULE", "氨氯地平贝那普利(II)"): "贝那普利氨氯地平",
    ("MOLECULE", "氨氯地平贝那普利"): "贝那普利氨氯地平",
    ("MOLECULE", "美阿沙坦钾片"): "美阿沙坦",
    ("MOLECULE", "硝苯地平(II)"): "硝苯地平缓释片",
    ("MOLECULE", "硝苯地平控释片"): "硝苯地平缓释片",
}

d_ptd = {
    "氯沙坦": ("MOLECULE", "100MG", 2),
    "氯沙坦": ("MOLECULE", "100MG", 2),
    "厄贝沙坦": ("MOLECULE", "75MG", 0.5),
    "替米沙坦": ("MOLECULE", "20MG", 0.25),
    "替米沙坦": ("MOLECULE", "40MG", 0.5),
    "坎地沙坦": ("MOLECULE", "4MG", 0.5),
    "缬沙坦": ("MOLECULE", "40MG", 0.5),
    "缬沙坦": ("MOLECULE", "160MG", 2),
    "培哚普利": ("MOLECULE", "8MG", 2),
    "贝那普利": ("MOLECULE", "5MG", 0.5),
    "卡托普利": ("MOLECULE", "12.5MG", 0.25),
    "卡托普利": ("MOLECULE", "25MG", 0.5),
    "依那普利": ("MOLECULE", "5MG", 0.5),
    "雷米普利": ("MOLECULE", "2.5MG", 0.5),
    "沙库巴曲缬沙坦": ("MOLECULE", "100MG", 0.5),
    "沙库巴曲缬沙坦": ("MOLECULE", "50MG", 0.25),
    "美阿沙坦": ("MOLECULE", "80MG", 2),
    "硝苯地平": ("MOLECULE", "10MG", 1 / 3),
    "硝苯地平": ("MOLECULE", "20MG", 2 / 3),
    "非洛地平": ("MOLECULE", "2.5MG", 0.5),
    "马尼地平": ("MOLECULE", "5MG", 0.5),
    "贝尼地平": ("MOLECULE", "2MG", 0.25),
    "贝尼地平": ("MOLECULE", "4MG", 0.5),
    "美托洛尔缓释片": ("MOLECULE", "95MG", 2),
    "美托洛尔": ("MOLECULE", "25MG", 1 / 6),
    "美托洛尔": ("MOLECULE", "50MG", 1 / 3),
    "艾司洛尔": ("MOLECULE", "100MG", 0.5),
    "阿替洛尔": ("MOLECULE", "25MG", 0.25),
    "普萘洛尔": ("MOLECULE", "10MG", 0.25),
    "索他洛尔": ("MOLECULE", "40MG", 0.5),
    "拉贝洛尔": ("MOLECULE", "100MG", 0.5),
    "雷贝拉唑": ("MOLECULE", "2MG", 2),
    "艾司奥美拉唑": ("MOLECULE", "40MG", 2),
    "奥美拉唑": ("MOLECULE", "40MG", 2),
    "奥美拉唑": ("MOLECULE", "10MG", 0.5),
    "兰索拉唑": ("MOLECULE", "30MG", 2),
    "匹伐他汀": ("MOLECULE", "1MG", 0.5),
    "阿托伐他汀": ("MOLECULE", "10MG", 0.5),
    "阿托伐他汀": ("MOLECULE", "40MG", 2),
    "瑞舒伐他汀": ("MOLECULE", "5MG", 0.5),
    "瑞舒伐他汀": ("MOLECULE", "20MG", 2),
    "辛伐他汀": ("MOLECULE", "5MG", 0.25),
    "辛伐他汀": ("MOLECULE", "10MG", 0.5),
    "辛伐他汀": ("MOLECULE", "40MG", 2),
    "氟伐他汀": ("MOLECULE", "20MG", 0.5),
    "氟伐他汀": ("MOLECULE", "80MG", 2),
    "普伐他汀": ("MOLECULE", "10MG", 0.5),
    "普伐他汀": ("MOLECULE", "40MG", 2),
    "洛伐他汀": ("MOLECULE", "10MG", 0.5),
}

l_vbp = [
    "厄贝沙坦",
    "坎地沙坦",
    "奥美沙坦",
    "替米沙坦",
    "氯沙坦",
    "缬沙坦",
    "乐卡地平",
    "氨氯地平",
    "美托洛尔",
    "比索洛尔",
    "雷贝拉唑",
    "艾司奥美拉唑",
    "奥美拉唑",
    "泮托拉唑",
    "辛伐他汀",
    "匹伐他汀",
    "阿托伐他汀",
    "瑞舒伐他汀",
    "缬沙坦氨氯地平",
]


def fetch_data(condition: str, focus: list = None) -> pd.DataFrame:
    sql = "SELECT * FROM " + table_name + " WHERE " + condition
    df = pd.read_sql(sql=sql, con=engine)

    df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
    df["PRODUCT"] = (
        df["PRODUCT"]
        .str.split("|")
        .str[0]
        # + "（"
        # + df["PRODUCT"].str.split("|").str[1].str[-3:]
        # + "）"
    )
    df["PRODUCT_CORP"] = (
        df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
        + "\n"
        + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
    )

    # 清洗数据命名
    for k, v in d_rename.items():
        mask = df[k[0]] == k[1]
        df.loc[mask, k[0]] = v

    # 拜新同分子的问题
    mask = df["PRODUCT"] == "拜新同"
    df.loc[mask, "MOLECULE"] = "硝苯地平缓释片"

    # 倍他乐克ZOK分子的问题
    mask = df["PRODUCT"] == "倍他乐克ZOK"
    df.loc[mask, "MOLECULE"] = "美托洛尔缓释片"

    # 转换标准片数
    mask = df["UNIT"] == "Volume (Counting Unit)"
    df_std_volume = df.loc[mask, :]
    df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
    df = pd.concat([df, df_std_volume])

    for k, v in d_ptd.items():
        convert_std_volume(df, v[0], k, v[1], v[2])

    # 标记非关注品种为其他
    if len(focus) > 0:
        mask = (df["MOLECULE"].isin(focus)) | (df["MOLECULE"].isin(l_vbp))
        df.loc[~mask, "MOLECULE"] = "其他非集采品种"

    # 标记vbp品种
    mask = df["MOLECULE"].isin(l_vbp)
    df.loc[mask, "MOLECULE"] = "集采品种"

    return df


if __name__ == "__main__":

    d_market = {
        "ARB市场": (
            "[TC III] in ('C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药')",
            ["阿利沙坦"],
        ),
        "CCB市场": (
            "[TC III] in ('C08A CALCIUM ANTAGONISTS PLAIN|钙离子拮抗剂，单一用药') \
            AND [MOLECULE] not in ('维拉帕米|VERAPAMIL','地尔硫卓|DILTIAZEM') \
            AND [FORMULATION] like 'ORAL%'",
            ["硝苯地平缓释片", "左旋氨氯地平", "非洛地平", "贝尼地平"],
        ),
        "BB市场": (
            "[TC III] in ('C07A BETA BLOCKING AGENT PLN|β受体阻断剂，单用') AND [FORMULATION] like 'ORAL%'",
            ["阿罗洛尔"],
        ),
        "PPI市场": (
            "[TC IV] in ('A02B2 PROTON PUMP INHIBITORS|质子泵抑制剂(PPI)') AND [FORMULATION] like 'ORAL%'",
            ["艾普拉唑"],
        ),
        "他汀市场": (
            "[TC IV] in ('C10A1 STATINS (HMG-COA RED)|他汀类(HMG-COA（羟-甲戊二酰辅酶A）还原酶抑制剂)')",
            ["氟伐他汀", "普伐他汀"],
        ),
        "降LDL-C药物市场": (
            "[TC IV] in ('C10A1 STATINS (HMG-COA RED)|他汀类(HMG-COA（羟-甲戊二酰辅酶A）还原酶抑制剂)', \
            'C10A4 PCSK9 INHIBITORS|PCSK9抑制剂')  \
            OR MOLECULE in ('依折麦布|EZETIMIBE','依折麦布|HYBUTIMIBE','依折麦布辛伐他汀|EZETIMIBE+SIMVASTATIN') ",
            ["依折麦布"],
        ),
        "A+C FDC市场":(
            "MOLECULE in ('培哚普利氨氯地平片(III)|AMLODIPINE+PERINDOPRIL', \
            '氨氯地平贝那普利(II)|AMLODIPINE+BENAZEPRIL', \
            '氨氯地平贝那普利|AMLODIPINE+BENAZEPRIL', \
            '缬沙坦氨氯地平|AMLODIPINE+VALSARTAN', \
            '奥美沙坦酯氨氯地平片|AMLODIPINE+OLMESARTAN MEDOXOMIL')",
            ["贝那普利氨氯地平"]
        )
    }

    for k, v in d_market.items():
        df = fetch_data(v[0], v[1])

        r = chpa(df, name=k)

        for unit in [
            "Value",
            "Volume (Std Counting Unit)",
        ]:
            r.plot_overall_performance(
                dimension="MOLECULE",
                unit=unit,
                sorter=v[1] + ["其他非集采品种", "集采品种"],
                width=15,
                height=6,
            )
