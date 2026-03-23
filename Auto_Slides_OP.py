from os import path
import sys

sys.path.append(path.abspath("D:\\PyProjects\\chart_class"))

from utils.ppt import PPT

dict_layout = {
    # 骨松治疗市场
    "骨松治疗市场": 2,
    "骨松治疗市场dual": 3,
    "骨松治疗市场销售额": 3,
    "骨松治疗市场PTD": 3,
    "骨松治疗市场销售额气泡图-净增长": 3,
    "骨松治疗市场PTD气泡图-净增长": 3,
    "骨松治疗市场销售额气泡图-增长率": 4,
    "骨松治疗市场PTD气泡图-增长率": 4,
    # 特立帕肽市场
    "特立帕肽市场": 5,
    "特立帕肽市场dual": 6,
    # "特立帕肽市场销售额": 6,
    # "特立帕肽市场PTD": 7,
    # "特立帕肽市场销售额气泡图-净增长": 6,
    # "特立帕肽市场PTD气泡图-净增长": 7,
    # "特立帕肽市场销售额气泡图-增长率": 8,
    # "特立帕肽市场PTD气泡图-增长率": 9,
}


if __name__ == "__main__":

    # ！！注意修改最新报告日期
    QTR = "25Q3"
    MON = "2025-09"

    # 欣复泰
    brand = "欣复泰"

    # 创建ppt
    p = PPT(f"IQVIA CHPA最新表现Key Slides_template_{brand}.pptx")

    for mkt in [
        "骨松治疗市场",
        "特立帕肽市场",
    ]:

        # 分隔页-市场定义
        c = p.add_content_slide(layout_style=dict_layout[f"{mkt}"])
        c.set_title(mkt)

        if mkt == "骨松治疗市场":
            # 第一页，治疗大类滚动年趋势双图
            c = p.add_content_slide(layout_style=dict_layout[f"{mkt}dual"])
            c.add_image(
                f"plots\\{mkt}分治疗大类滚动年趋势.png",
                width=c.body.width * 0.95,
                height=None,
                loc=c.body.center,
            )

            # 第2-3页，治疗大类金额/PTD滚动年趋势单图
            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    f"plots\\{mkt}分治疗大类{unit_type}滚动年趋势.png",
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )

            # 第4-5页，治疗大类金额/PTD季度趋势单图
            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    f"plots\\{mkt}分治疗大类{unit_type}季度趋势.png",
                    width=c.body.width * 0.85,
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
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}"]
                    )
                    c.add_image(
                        (
                            f"plots\\{mkt}{MON}滚动年TOP20{metric}{unit_type}明细.png"
                            if metric == "产品"
                            else f"plots\\{mkt}{MON}滚动年{metric}{unit_type}明细.png"
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
                        f"plots\\{mkt}TOP10{metric}滚动年{unit_type}趋势.png",
                        width=c.body.width * 0.85,
                        height=None,
                        loc=c.body.center,
                    )

                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}"]
                    )
                    c.add_image(
                        f"plots\\{mkt}历年{metric}{unit_type}排名.png",
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )
        else:
            c = p.add_content_slide(layout_style=dict_layout[f"{mkt}dual"])
            c.add_image(
                f"plots\\{mkt}分产品包装滚动年趋势.png",
                width=c.body.width * 0.95,
                height=None,
                loc=c.body.center,
            )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}dual"])
                c.add_image(
                    f"plots\\{mkt}分产品包装{unit_type}滚动年趋势.png",
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}dual"])
                c.add_image(
                    f"plots\\{mkt}分产品包装{unit_type}季度趋势.png",
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(
                    layout_style=dict_layout[f"{mkt}dual"]
                )
                c.add_image(
                    f"plots\\{mkt}{MON}滚动年产品包装{unit_type}明细.png",
                    width=c.body.width * 0.95,
                    height=None,
                    loc=c.body.center,
                )

    # 结尾页
    c = p.add_content_slide()
    c.set_title("Thank You")

    p.save(save_path=f"IQVIA CHPA最新表现Key Slides_{QTR}_{brand}.pptx")
