from re import template
import pandas as pd
from sqlalchemy import create_engine
from cls.data_cls import ChpaAnalyzer
from cls.ppt_cls import ChpaPPT
from pptx.util import Inches, Pt, Cm
import matplotlib.pyplot as plt
from cls.chart_cls import PlotBubble

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

    df_kpi = c.get_kpi("CORPORATION", is_formatted=True)

    print(df_kpi)

    p = ChpaPPT(analyzer=c, template_path="template.pptx", save_path="corp.pptx")

    p.add_img_slide()
    p.add_table(df_kpi.head(10), font_size=Pt(9))

    df_kpi = c.get_kpi("CORPORATION", is_formatted=False)

    f = plt.figure(
        width=14,
        height=7,
        FigureClass=PlotBubble,
        gs=None,
        fmt=None,
        savepath=c.save_path,
        data=df_kpi.loc[:, ["MAT金额", "净增长", "MAT金额"]],
        fontsize=10,
        style={"xlabel": "MAT金额", "ylabel": "MAT金额净增长"},
    )

    p.add_img_slide()
    p.add_image(f.plot(x_fmt="{:,.0f}", y_fmt="{:+,.0f}", y_avg=0), height=Cm(13))
    p.save()