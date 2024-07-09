from CHPA2 import CHPA, extract_strength
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

condition_htn = "[TC IV] in ('C10A1 STATINS (HMG-COA RED)|他汀类(HMG-COA（羟-甲戊二酰辅酶A）还原酶抑制剂)', \
'C10A4 PCSK9 INHIBITORS|PCSK9抑制剂',\
'C10C0 LIP.REG.CO.W.OTH.LIP.REG|多种脂质调节剂联合用药') \
or MOLECULE in ('EZETIMIBE|依折麦布', 'HYBUTIMIBE|海博麦布')"


sql = "SELECT * FROM " + table_name + " WHERE " + condition_htn
df = pd.read_sql(sql=sql, con=engine)

print("Finished importing...")

D_CLASS = {
    "C10A9": "胆固醇吸收抑制剂",
    "C10C0": "他汀+麦布类复方",
    "C10A1": "他汀",
    "C10A4": "PCSK9抑制剂",
}

D_COLOR = {
    "他汀": "navy",
    "胆固醇吸收抑制剂": "crimson",
    "他汀+麦布类复方": "purple",
    "PCSK9抑制剂": "darkorange",
}

df["CLASS"] = df["TC IV"].str[:5].map(D_CLASS).fillna("Others")

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)


D_RENAME = {
    "阿利珠单抗": "阿利西尤单抗",
}
df["MOLECULE"] = df["MOLECULE"].map(D_RENAME).fillna(df["MOLECULE"])

# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "PTD"
df = pd.concat([df, df_std_volume])

df_ptd = pd.read_excel("降LDL-C类PTD.xlsx")
for row in df_ptd.iterrows():
    mask = (
        (df["MOLECULE"] == row[1]["MOLECULE"])
        & (df["PACKAGE"] == row[1]["PACKAGE"])
        & (df["UNIT"] == "PTD")
    )
    df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / row[1]["index"]

print("Finished converting PTD...")


r = CHPA(df, name="降LDL-C用药市场", date_column="DATE", period_interval=3)
# r.data.to_excel("test.xlsx")
r.plot_overall_performance(
    index="CLASS", unit_change="百万", label_threshold=0.01, color_dict=D_COLOR
)
r.plot_overall_performance(
    index="CLASS",
    unit_change="百万",
    label_threshold=0.01,
    color_dict=D_COLOR,
    unit="PTD",
)
r.plot_overall_performance(
    index="CLASS", unit_change="百万", label_threshold=0.01, color_dict=D_COLOR, period="QTR"
)
r.plot_overall_performance(
    index="CLASS",
    unit_change="百万",
    label_threshold=0.01,
    color_dict=D_COLOR,
    unit="PTD",
    period="QTR",
)
r.plottable_latest(
    index="CLASS",
    unit="Value",
    focus=None,
    period="MAT",
    topn=15,
    fontsize=22,
)
r.plottable_latest(
    index="CLASS",
    unit="PTD",
    focus=None,
    period="MAT",
    topn=15,
    fontsize=22,
)

df2 = df[df["CLASS"] == "PCSK9抑制剂"]
r = CHPA(df2, name="PCSK9市场", date_column="DATE", period_interval=3)


r.plot_overall_performance(
    index="MOLECULE", unit_change="百万", label_threshold=0.01, color_dict=D_COLOR
)
r.plot_overall_performance(
    index="MOLECULE",
    unit_change="百万",
    label_threshold=0.01,
    color_dict=D_COLOR,
    unit="PTD",
)


r.plot_overall_performance(
    index="MOLECULE",
    unit_change="百万",
    label_threshold=0.01,
    color_dict=D_COLOR,
    period="QTR",
)
r.plot_overall_performance(
    index="MOLECULE",
    unit_change="百万",
    label_threshold=0.01,
    color_dict=D_COLOR,
    period="QTR",
    unit="PTD",
)

r.plottable_latest(
    index="MOLECULE",
    unit="Value",
    focus=None,
    hue="CORPORATION",
    period="MAT",
    topn=15,
    fontsize=22,
)
r.plottable_latest(
    index="MOLECULE",
    unit="PTD",
    focus=None,
    hue="CORPORATION",
    period="MAT",
    topn=15,
    fontsize=22,
)
