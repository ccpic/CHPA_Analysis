from re import template
import pandas as pd
from sqlalchemy import create_engine
from cls.data_cls import ChpaAnalyzer
from cls.ppt_cls import ChpaPPT
from pptx.util import Inches, Pt, Cm
import matplotlib.pyplot as plt
from cls.chart_cls import PlotBubble, PlotWaterfall

if __name__ == "__main__":
    engine = create_engine("mssql+pymssql://(local)/CHPA_1806")
    table_name = "data"

    condition = "[TC II] = 'C09 RENIN-ANGIOTEN SYST AGENT|作用于肾素-血管紧张素系统的药物'"
    if condition is None:
        sql = f"SELECT * FROM {table_name} WHERE UNIT = 'Value' AND PERIOD = 'MAT'"
    else:
        sql = f"SELECT * FROM {table_name}  WHERE UNIT = 'Value' AND PERIOD = 'MAT' AND {condition}"

    df = pd.read_sql(sql=sql, con=engine)
    df["MOLECULE"] = df["MOLECULE"].str.split("|").str[0]
    df["CORPORATION"] = df["CORPORATION"].str.split("|").str[0]

    c = ChpaAnalyzer(data=df, name="CV领域")

    # df_kpi = c.get_kpi("CORPORATION", is_formatted=True)

    p = ChpaPPT(analyzer=c, template_path="template.pptx", save_path="corp.pptx")

    # p.add_img_slide()
    # p.add_table(df_kpi.head(10), font_size=Pt(9))

    corp_kpi = c.get_kpi("CORPORATION", is_formatted=False)

    # f = plt.figure(
    #     width=14,
    #     height=7,
    #     FigureClass=PlotBubble,
    #     gs=None,
    #     fmt=None,
    #     savepath=c.save_path,
    #     data=df_kpi.loc[:, ["MAT金额", "净增长", "MAT金额"]],
    #     fontsize=10,
    #     style={"xlabel": "MAT金额", "ylabel": "MAT金额净增长"},
    # )

    # p.add_img_slide()
    # p.add_image(f.plot(x_fmt="{:,.0f}", y_fmt="{:+,.0f}", y_avg=0), height=Cm(13))
    # p.save()

    for idx in corp_kpi.head(1).index:
        product_kpi = c.get_kpi(
            "PRODUCT", query_str=f"CORPORATION == '{idx}'", is_formatted=False
        )
        product_kpi["净增长绝对值"] = product_kpi["净增长"].abs()
        product_kpi.sort_values(by="净增长绝对值", ascending=False, inplace=True)
        title = f"{idx}净增长贡献"

        value_pre = c.get_pivot(
            "DATE", query_str=f"CORPORATION == '{idx}' and DATE == '2020-12-01'"
        ).sum().values[0]
        
        f = plt.figure(
            width=7,
            height=7,
            FigureClass=PlotWaterfall,
            gs=None,
            fmt=["{:,.0f}"],
            savepath=c.save_path,
            data=product_kpi.loc[:, ["净增长"]],
            fontsize=10,
            style={"title": title, "xlabel_rotation": 90, "remove_yticks": True},
        )

        f.plot(pre=[("2020", value_pre)], net_index="2021")
