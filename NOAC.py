from CHPA import *

engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
table_name = "data"
condition = "[TC IV] = 'B01F0 DIRECT FACTOR XA INHIBS|直接因子XA抑制剂' or MOLECULE in('华法林|WARFARIN','达比加群酯|DABIGATRAN ETEXILATE')"
sql = "SELECT * FROM " + table_name + " WHERE " + condition
df = pd.read_sql(sql=sql, con=engine)

df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
df["PRODUCT"] = df["PRODUCT"].str.split("|").str[0]
df["PRODUCT_CORP"] = (
    df["PRODUCT_CORP"].str.split("（").str[0].str.split("|").str[0]
    + "\n"
    + df["PRODUCT_CORP"].str.split("（").str[1].str.split("|").str[0]
)


r = chpa(df, name="口服抗凝药（VKA+NOAC）市场")

r.plot_overall_performance(
    dimension="MOLECULE",
    sorter=[
        "华法林",
        "阿哌沙班",
        "利伐沙班",
        "依度沙班",
        "达比加群酯",
    ],
)
r.plot_overall_performance(
    dimension="MOLECULE",
    unit="Volume (Counting Unit)",
    sorter=[
        "华法林",
        "阿哌沙班",
        "利伐沙班",
        "依度沙班",
        "达比加群酯",
    ],
)
r.plot_group_share_gr(
    index="PRODUCT_CORP",
    date=[r.latest_date()],
    dimension=None,
    column=None,
    adjust_scale=0.1,
    ylim=[-0.5, 1],
)
r.plot_group_share_gr(
    index="PRODUCT_CORP",
    date=[r.latest_date()],
    dimension=None,
    column=None,
    adjust_scale=0.1,
    unit="Volume (Counting Unit)",
)

# r = chpa(df, name="口服抗凝药市场\n（VKA+NOAC）")
# r.plot_share("MOLECULE", None, "份额")
# r.plot_share("MOLECULE", None, "净增长贡献")

# r.plot_share("MOLECULE", None, "份额", unit="Volume (Counting Unit)")
# r.plot_share("MOLECULE", None, "净增长贡献", unit="Volume (Counting Unit)")

# df = df[df["MOLECULE"] == "利伐沙班"]
# r = chpa(df, name="利伐沙班分剂型")
# r.plot_share("STRENGTH", None, "份额", unit="Volume (Counting Unit)")
# r.plot_share("STRENGTH", None, "净增长贡献", unit="Volume (Counting Unit)")
