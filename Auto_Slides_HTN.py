from os import path
import sys

sys.path.append(path.abspath("D:\\PyProjects\\chart_class"))

from utils.ppt import PPT

dict_layout = {
    # RAAS+ARNI市场
    "RAAS+ARNI市场": 2,
    "RAAS+ARNI市场dual": 4,
    "RAAS+ARNI市场销售额": 3,
    "RAAS+ARNI市场PTD": 4,
    "RAAS+ARNI市场销售额气泡图-净增长": 3,
    "RAAS+ARNI市场PTD气泡图-净增长": 4,
    "RAAS+ARNI市场销售额气泡图-增长率": 5,
    "RAAS+ARNI市场PTD气泡图-增长率": 6,
    # RAAS市场
    "RAAS市场": 7,
    "RAAS市场dual": 9,
    "RAAS市场销售额": 8,
    "RAAS市场PTD": 9,
    "RAAS市场销售额气泡图-净增长": 8,
    "RAAS市场PTD气泡图-净增长": 9,
    "RAAS市场销售额气泡图-增长率": 10,
    "RAAS市场PTD气泡图-增长率": 11,
    # RAAS单方+ARNI市场
    "RAAS单方+ARNI市场": 12,
    "RAAS单方+ARNI市场dual": 14,
    "RAAS单方+ARNI市场销售额": 13,
    "RAAS单方+ARNI市场PTD": 14,
    "RAAS单方+ARNI市场销售额气泡图-净增长": 13,
    "RAAS单方+ARNI市场PTD气泡图-净增长": 14,
    "RAAS单方+ARNI市场销售额气泡图-增长率": 15,
    "RAAS单方+ARNI市场PTD气泡图-增长率": 16,
    # RAAS单方市场
    "RAAS单方市场": 17,
    "RAAS单方市场dual": 19,
    "RAAS单方市场销售额": 18,
    "RAAS单方市场PTD": 19,
    "RAAS单方市场销售额气泡图-净增长": 18,
    "RAAS单方市场PTD气泡图-净增长": 19,
    "RAAS单方市场销售额气泡图-增长率": 20,
    "RAAS单方市场PTD气泡图-增长率": 21,
    # ARB单方市场
    "ARB单方市场": 22,
    "ARB单方市场dual": 24,
    "ARB单方市场销售额": 23,
    "ARB单方市场PTD": 24,
    "ARB单方市场销售额气泡图-净增长": 23,
    "ARB单方市场PTD气泡图-净增长": 24,
    "ARB单方市场销售额气泡图-增长率": 25,
    "ARB单方市场PTD气泡图-增长率": 26,
    # RAAS复方市场
    "RAAS复方市场": 27,
    "RAAS复方市场dual": 29,
    "RAAS复方市场销售额": 28,
    "RAAS复方市场PTD": 29,
    "RAAS复方市场销售额气泡图-净增长": 28,
    "RAAS复方市场PTD气泡图-净增长": 29,
    "RAAS复方市场销售额气泡图-增长率": 30,
    "RAAS复方市场PTD气泡图-增长率": 31,
    # A+C复方市场
    "A+C复方市场": 32,
    "A+C复方市场dual": 34,
    "A+C复方市场销售额": 33,
    "A+C复方市场PTD": 34,
    "A+C复方市场销售额气泡图-净增长": 33,
    "A+C复方市场PTD气泡图-净增长": 34,
    "A+C复方市场销售额气泡图-增长率": 35,
    "A+C复方市场PTD气泡图-增长率": 36,
}


if __name__ == "__main__":

    # ！！注意修改最新报告日期
    QTR = "25Q3"
    MON = "2025-09"

    # 信立坦&复立坦定义市场
    brand = "信立坦&复立坦"

    # 创建ppt
    p = PPT(f"IQVIA CHPA最新表现Key Slides_template_{brand}.pptx")

    for mkt in [
        "RAAS+ARNI市场",  # 含复方
        "RAAS市场",  # 含复方
        "RAAS单方+ARNI市场",
        "RAAS单方市场",
        "ARB单方市场",
        "RAAS复方市场",
        "A+C复方市场",
    ]:

        # 分隔页-市场定义
        c = p.add_content_slide(layout_style=dict_layout[f"{mkt}"])
        c.set_title(mkt)

        # 第一页，治疗大类滚动年趋势双图
        c = p.add_content_slide(layout_style=dict_layout[f"{mkt}dual"])
        c.add_image(
            (
                f"plots\\{mkt}分治疗大类滚动年趋势.png"
                if mkt != "ARB单方市场"
                else f"plots\\{mkt}滚动年趋势.png"
            ),
            width=c.body.width * 0.95,
            height=None,
            loc=c.body.center,
        )

        # 第2-3页，治疗大类金额/PTD滚动年趋势单图
        for unit_type in ["销售额", "PTD"]:
            c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
            c.add_image(
                (
                    f"plots\\{mkt}分治疗大类{unit_type}滚动年趋势.png"
                    if mkt != "ARB单方市场"
                    else f"plots\\{mkt}{unit_type}滚动年趋势.png"
                ),
                width=c.body.width * 0.85,
                height=None,
                loc=c.body.center,
            )

        # 第4-5页，治疗大类金额/PTD季度趋势单图
        for unit_type in ["销售额", "PTD"]:
            c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
            c.add_image(
                (
                    f"plots\\{mkt}分治疗大类{unit_type}季度趋势.png"
                    if mkt != "ARB单方市场"
                    else f"plots\\{mkt}{unit_type}季度趋势.png"
                ),
                width=c.body.width * 0.85,
                height=None,
                loc=c.body.center,
            )

        # 第6页，分VBP状态滚动年趋势双图
        c = p.add_content_slide(layout_style=dict_layout[f"{mkt}dual"])
        c.add_image(
            f"plots\\{mkt}分VBP状态滚动年趋势.png",
            width=c.body.width * 0.95,
            height=None,
            loc=c.body.center,
        )

        # 通用名/产品气泡图、排名明细、趋势、
        for metric in ["通用名", "产品"]:
            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(
                    layout_style=dict_layout[f"{mkt}{unit_type}气泡图-净增长"]
                )
                c.add_image(
                    f"plots\\{mkt}{metric}滚动年{unit_type}绝对值 vs. 净增长.png",
                    width=c.body.width * 0.95,
                    height=None,
                    loc=c.body.center,
                )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(
                    layout_style=dict_layout[f"{mkt}{unit_type}气泡图-增长率"]
                )
                c.add_image(
                    f"plots\\{mkt}{metric}滚动年{unit_type}份额 vs. 同比增长率.png",
                    width=c.body.width * 0.95,
                    height=None,
                    loc=c.body.center,
                )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    (
                        f"plots\\{mkt}{MON}滚动年TOP20{metric}{unit_type}明细.png"
                        if (
                            mkt == "RAAS+ARNI市场"
                            or mkt == "RAAS市场"
                            or metric == "产品"
                        )
                        else f"plots\\{mkt}{MON}滚动年{metric}{unit_type}明细.png"
                    ),
                    width=c.body.width * 0.95,
                    height=None,
                    loc=c.body.center,
                )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    (
                        f"plots\\{mkt}{metric}滚动年{unit_type}趋势.png"
                        if (
                            (mkt == "ARB单方市场" or mkt == "A+C复方市场")
                            and metric == "通用名"
                        )
                        else f"plots\\{mkt}TOP10{metric}滚动年{unit_type}趋势.png"
                    ),
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    f"plots\\{mkt}历年{metric}{unit_type}排名.png",
                    width=c.body.width * 0.95,
                    height=None,
                    loc=c.body.center,
                )

    # 结尾页
    c = p.add_content_slide()
    c.set_title("Thank You")

    p.save(save_path=f"IQVIA CHPA最新表现Key Slides_{QTR}_{brand}.pptx")
