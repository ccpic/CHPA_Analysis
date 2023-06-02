from CHPA2 import CHPA, convert_std_volume, extract_strength
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"

D_RENAME = {
    "A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)": "磺脲类",
    "A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药": "二甲双胍",
    "A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)": "α糖苷酶抑制剂",
    "A10M GLINIDE ANTIDIABETICS|格列奈类降糖药": "格列奈类",
    "A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药": "TZD & PPAR全激动剂",
    "A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂": "DPP4",
    "A10S GLP-1 AGONIST A-DIABS|GLP-1激动剂(胰高血糖素样肽-1激动剂类降糖药)(A10B9)": "GLP-1",
    "A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂": "SGLT2",
    "A10X OTHER DRUGS FOR DIABETES|用于糖尿病的其他药物": "GKA",
}

condition_niad = "[TC III] in ('A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)', \
    'A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药', \
    'A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)', \
    'A10M GLINIDE ANTIDIABETICS|格列奈类降糖药', \
    'A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药', \
    'A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂', \
    'A10S GLP-1 AGONIST A-DIABS|GLP-1激动剂(胰高血糖素样肽-1激动剂类降糖药)(A10B9)', \
    'A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂') or MOLECULE='DORZAGLIATIN|多格列艾汀'"

condition_oad = "[TC III] in ('A10H SULPHONYLUREA A-DIABS|磺脲类降糖药(A10B1)', \
    'A10J BIGUANIDE ANTIDIABETICS|双胍类降糖药', \
    'A10L A-GLUCOSIDASE INH A-DIAB|α-葡糖苷酶抑制剂(A10B5)', \
    'A10M GLINIDE ANTIDIABETICS|格列奈类降糖药', \
    'A10K GLITAZONE ANTIDIABETICS|格列酮类降糖药', \
    'A10N DPP-IV INHIBITOR A-DIABS|DPP-IV（二肽基肽酶IV）抑制剂', \
    'A10P SGLT2 INHIBITOR A-DIABS|钠-葡萄糖协同转运蛋白2抑制剂') or MOLECULE='DORZAGLIATIN|多格列艾汀'"

sql = "SELECT * FROM " + table_name + " WHERE " + condition_niad
df = pd.read_sql(sql=sql, con=engine)


df["MOLECULE"] = df["MOLECULE"].str.split("|").str[1]
df["PRODUCT"] = df["PRODUCT"].apply(lambda x: x[:-3].strip() + " (" + x[-3:] + ")")
df["TC III"] = df["TC III"].map(D_RENAME)
df["STRENGTH"] = df["PACKAGE"].apply(extract_strength)


# 折算标准片数
mask = df["UNIT"] == "Volume (Counting Unit)"
df_std_volume = df.loc[mask, :]
df_std_volume["UNIT"] = "Volume (Std Counting Unit)"
df = pd.concat([df, df_std_volume])

convert_std_volume(df, "MOLECULE", "阿卡波糖", "50MG", 1 / 6)
convert_std_volume(df, "MOLECULE", "阿卡波糖", "100MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "艾塞那肽", "0.3MG", 30)
convert_std_volume(df, "MOLECULE", "艾塞那肽", "0.6MG", 30)
convert_std_volume(df, "MOLECULE", "艾塞那肽", "2MG", 30)
convert_std_volume(df, "MOLECULE", "贝那那肽", "4.2MG", 7)
convert_std_volume(df, "MOLECULE", "吡格列酮", "15MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "吡格列酮二甲双胍", "515MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "杜拉鲁肽", "0.75MG", 7)
convert_std_volume(df, "MOLECULE", "杜拉鲁肽", "1.5MG", 7)
convert_std_volume(df, "MOLECULE", "二甲双胍", "0.25G", 1 / 4)
convert_std_volume(df, "MOLECULE", "二甲双胍", "0.5G", 1 / 2)
convert_std_volume(df, "MOLECULE", "二甲双胍", "250MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "二甲双胍", "500MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "二甲双胍", "850MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "二甲双胍格列本脲", "251MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "二甲双胍格列本脲", "252MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "二甲双胍格列吡嗪", "252MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "二甲双胍格列吡嗪", "300MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "二甲双胍格列吡嗪", "502MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "二甲双胍格列齐特", "290MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "二甲双胍格列齐特", "40MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "二甲双胍维格列汀", "900MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "伏格列波糖", "0.1MG", 1 / 6)
convert_std_volume(df, "MOLECULE", "伏格列波糖", "0.2MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "伏格列波糖", "0.3MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "伏格列波糖", "200Y", 1 / 3)
convert_std_volume(df, "MOLECULE", "格列本脲", "2.5MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "格列吡嗪", "2.5MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "格列吡嗪", "5MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "格列喹酮", "30MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "格列美脲", "1MG", 1 / 6)
convert_std_volume(df, "MOLECULE", "格列美脲", "2MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "格列齐特", "30MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "格列齐特", "40MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "卡格列净", "100MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "利拉鲁肽", "18MG", 15)
convert_std_volume(df, "MOLECULE", "利西拉肽", "150Y", 14)
convert_std_volume(df, "MOLECULE", "利西拉肽", "300Y", 14)
convert_std_volume(df, "MOLECULE", "罗格列酮", "1MG", 1 / 4)
convert_std_volume(df, "MOLECULE", "罗格列酮", "2MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "米格列醇", "50MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "米格列奈", "5MG", 1 / 6)
convert_std_volume(df, "MOLECULE", "米格列醇", "10MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "那格列奈", "30MG", 1 / 12)
convert_std_volume(df, "MOLECULE", "那格列奈", "60MG", 1 / 6)
convert_std_volume(df, "MOLECULE", "那格列奈", "120MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "瑞格列奈", "0.5MG", 1 / 12)
convert_std_volume(df, "MOLECULE", "瑞格列奈", "1MG", 1 / 6)
convert_std_volume(df, "MOLECULE", "瑞格列奈", "2MG", 1 / 3)
convert_std_volume(df, "MOLECULE", "瑞格列奈", "500Y", 1 / 12)
convert_std_volume(df, "MOLECULE", "瑞格列奈二甲双胍", "502MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "沙格列汀", "2.5MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "沙格列汀二甲双胍", "1002MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "沙格列汀二甲双胍", "1005MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "索马鲁肽", "2.01MG", 28)
convert_std_volume(df, "MOLECULE", "索马鲁肽", "4.02MG", 56)
convert_std_volume(df, "MOLECULE", "维格列汀", "50MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "西格列他钠", "16MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "西格列汀二甲双胍", "500MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "西格列汀二甲双胍", "850MG", 1 / 2)
convert_std_volume(df, "MOLECULE", "多格列艾汀", "75MG", 1 / 2)
convert_std_volume(df, "PACKAGE", "FU LAI HE TAB FLM CTD 30", np.nan, 1 / 2)
convert_std_volume(df, "PACKAGE", "QI ZHI PING TAB 36", np.nan, 1 / 4)

# df_index = pd.read_excel("非胰岛素降糖药PTD计算系数.xlsx", engine="openpyxl")
# print(df_index)

# # 折算标准片数
# mask = df["UNIT"] == "Volume (Counting Unit)"
# df_std_volume = df.loc[mask, :]
# df_std_volume["UNIT"] = "PTD"
# df = pd.concat([df, df_std_volume])

# for index, value in df_index.iterrows():
#     mask = (df["PACKAGE"] == value[6]) & (df["UNIT"] == "PTD")
#     df.loc[mask, "AMOUNT"] = df.loc[mask, "AMOUNT"] / value[8]


r = CHPA(df, name="NIAD(非胰岛素降糖药)市场", date_column="DATE", period_interval=3)

# r.plot_overall_performance(index="TC III", unit_change="百万")
# r.plot_overall_performance(
#     index="TC III", unit="Volume (Std Counting Unit)", unit_change="百万"
# )
# r.plot_overall_performance(index="TC III", period="QTR", unit_change="百万")
# r.plot_overall_performance(
#     index="TC III", period="QTR", unit="Volume (Std Counting Unit)", unit_change="百万"
# )

# r.plottable_latest(index="TC III", unit="Value")
# r.plottable_latest(index="TC III", unit="Volume (Std Counting Unit)")

# r.plot_size_diff(index="MOLECULE", unit="Value", unit_change="百万")
# r.plot_size_diff(
#     index="MOLECULE", unit="Volume (Std Counting Unit)", unit_change="百万", label_topy=5,
# )

r.plottable_latest(index="MOLECULE", unit="Value", hue="TC III")
r.plottable_latest(index="MOLECULE", unit="Volume (Std Counting Unit)", hue="TC III")


# r.plot_size_diff(index="PRODUCT", unit="Value", unit_change="百万")
# r.plot_size_diff(
#     index="PRODUCT", unit="Volume (Std Counting Unit)", unit_change="百万", label_topy=5,
# )

r.plottable_latest(index="PRODUCT", unit="Value", hue="CORPORATION")
r.plottable_latest(
    index="PRODUCT", unit="Volume (Std Counting Unit)", hue="CORPORATION"
)
