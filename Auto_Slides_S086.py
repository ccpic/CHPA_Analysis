from os import path
import sys

sys.path.append(path.abspath("D:\\PyProjects\\chart_class"))

from utils.ppt import PPT
from pptx.util import Cm

dict_layout = {
    # 口服降压药市场
    "口服降压药市场": 2,
    "口服降压药市场dual": 3,
    "口服降压药市场销售额": 3,
    "口服降压药市场PTD": 3,
    "口服降压药市场销售额气泡图-净增长": 3,
    "口服降压药市场PTD气泡图-净增长": 3,
    "口服降压药市场销售额气泡图-增长率": 4,
    "口服降压药市场PTD气泡图-增长率": 4,
    # RAAS+ARNI市场
    "RAAS+ARNI市场": 5,
    "RAAS+ARNI市场dual": 7,
    "RAAS+ARNI市场销售额": 6,
    "RAAS+ARNI市场PTD": 7,
    "RAAS+ARNI市场销售额气泡图-净增长": 6,
    "RAAS+ARNI市场PTD气泡图-净增长": 7,
    "RAAS+ARNI市场销售额气泡图-增长率": 8,
    "RAAS+ARNI市场PTD气泡图-增长率": 9,
    # ARNI市场
    "ARNI市场": 10,
    "ARNI市场dual": 11,
    "ARNI市场销售额": 11,
    # "ARNI市场PTD": 14,
    # "ARNI市场销售额气泡图-净增长": 13,
    # "ARNI市场PTD气泡图-净增长": 14,
    # "ARNI市场销售额气泡图-增长率": 15,
    # "ARNI市场PTD气泡图-增长率": 16,
}


if __name__ == "__main__":

    # ！！注意修改最新报告日期
    QTR = "25Q3"
    MON = "2025-09"

    # S086
    brand = "信超妥"

    # 创建ppt
    p = PPT(f"IQVIA CHPA最新表现Key Slides_template_{brand}.pptx")

    for mkt in [
        "口服降压药市场",
        "RAAS+ARNI市场",  # 含复方
        "ARNI市场",
    ]:

        # 分隔页-市场定义
        c = p.add_content_slide(layout_style=dict_layout[f"{mkt}"])
        c.set_title(mkt)

        if mkt != "ARNI市场":
            # 第一页，治疗大类滚动年趋势双图
            c = p.add_content_slide(layout_style=dict_layout[f"{mkt}dual"])
            c.add_image(
                image_file=(f"plots\\{mkt}分治疗大类滚动年趋势.png"),
                width=c.body.width * 0.95,
                height=None,
                loc=c.body.center,
            )

            # 第2-3页，治疗大类金额/PTD滚动年趋势单图
            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    image_file=(f"plots\\{mkt}分治疗大类{unit_type}滚动年趋势.png"),
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )

            # 第4-5页，治疗大类金额/PTD季度趋势单图
            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    image_file=(f"plots\\{mkt}分治疗大类{unit_type}季度趋势.png"),
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )

            if mkt == "口服降压药市场":
                # 治疗大类明细
                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}"]
                    )
                    c.add_image(
                        image_file=(
                            f"plots\\{mkt}{MON}滚动年治疗大类{unit_type}明细.png"
                        ),
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )
                # 治疗大类历年明细
                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}"]
                    )
                    c.add_image(
                        image_file=(f"plots\\{mkt}历年治疗大类{unit_type}排名.png"),
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )

            if mkt != "ARNI市场":
                # 第6页，分VBP状态滚动年趋势双图
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}dual"])
                c.add_image(
                    image_file=(f"plots\\{mkt}分VBP状态滚动年趋势.png"),
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
                        image_file=(
                            f"plots\\{mkt}{metric}滚动年{unit_type}绝对值 vs. 净增长.png"
                        ),
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )

                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}气泡图-增长率"]
                    )
                    c.add_image(
                        image_file=(
                            f"plots\\{mkt}{metric}滚动年{unit_type}份额 vs. 同比增长率.png"
                        ),
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )

                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}"]
                    )
                    c.add_image(
                        image_file=(
                            f"plots\\{mkt}{MON}滚动年TOP20{metric}{unit_type}明细.png"
                        ),
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )

                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}"]
                    )
                    c.add_image(
                        image_file=(
                            f"plots\\{mkt}TOP10{metric}滚动年{unit_type}趋势.png"
                        ),
                        width=c.body.width * 0.85,
                        height=None,
                        loc=c.body.center,
                    )

                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}"]
                    )
                    c.add_image(
                        image_file=(f"plots\\{mkt}历年{metric}{unit_type}排名.png"),
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )
        else:
            c = p.add_content_slide(layout_style=11)
            c.add_image(
                image_file=(f"plots\\{mkt}销售额滚动年趋势.png"),
                width=c.body.width * 0.4,
                height=None,
                anchor="mid_left",
                loc=c.body.left_mid + (Cm(2), 0),
            )
            c.add_image(
                image_file=(f"plots\\{mkt}PTD滚动年趋势.png"),
                width=c.body.width * 0.4,
                height=None,
                anchor="mid_right",
                loc=c.body.right_mid + (Cm(-2), 0),
            )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=11)
                c.add_image(
                    image_file=f"plots\\ARNI市场{unit_type}季度趋势.png",
                    width=c.body.width * 0.95,
                    height=None,
                    loc=c.body.center,
                )

            for dimension in ["产品", "产品包装"]  :
                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(layout_style=11)
                    c.add_image(
                        image_file=f"plots\\ARNI市场{MON}滚动年{dimension}{unit_type}明细.png",
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )

    # 结尾页
    c = p.add_content_slide()
    c.set_title("Thank You")

    p.save(save_path=f"IQVIA CHPA最新表现Key Slides_{QTR}_{brand}.pptx")
