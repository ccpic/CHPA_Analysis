from os import path
import sys

sys.path.append(path.abspath("D:\\PyProjects\\chart_class"))

from utils.ppt import PPT

dict_layout = {
    "肾性贫血市场销售额": 3,
    "肾性贫血市场PTD": 4,
    "肾性贫血市场销售额气泡图-净增长": 3,
    "肾性贫血市场PTD气泡图-净增长": 4,
    "肾性贫血市场销售额气泡图-增长率": 5,
    "肾性贫血市场PTD气泡图-增长率": 6,
    "ESA+HIF市场销售额": 8,
    "ESA+HIF市场PTD": 9,
    "ESA+HIF市场销售额气泡图-净增长": 8,
    "ESA+HIF市场PTD气泡图-净增长": 9,
    "ESA+HIF市场销售额气泡图-增长率": 10,
    "ESA+HIF市场PTD气泡图-增长率": 11,
    "HIF-PHI市场销售额": 13,
    "HIF-PHI市场PTD": 14,
    "HIF-PHI市场销售额气泡图-净增长": 13,
    "HIF-PHI市场PTD气泡图-净增长": 14,
    "HIF-PHI市场销售额气泡图-增长率": 15,
    "HIF-PHI市场PTD气泡图-增长率": 16,
}


if __name__ == "__main__":

    # ！！注意修改最新报告日期
    QTR = "25Q3"
    MON = "2025-09"

    # 肾性贫血定义市场
    brand = "恩那罗"
    # 创建ppt
    p = PPT(f"IQVIA CHPA最新表现Key Slides_template_{brand}.pptx")

    for mkt in ["肾性贫血市场", "ESA+HIF市场", "HIF-PHI市场"]:
        if mkt != "HIF-PHI市场":
            c = p.add_content_slide(layout_style=2 if mkt == "肾性贫血市场" else 7)
            c.set_title(mkt)

            c = p.add_content_slide(layout_style=3 if mkt == "肾性贫血市场" else 8)
            c.add_image(
                f"plots\\{mkt}分治疗大类滚动年趋势.png",
                width=c.body.width * 0.95,
                height=None,
                loc=c.body.center,
            )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    f"plots\\{mkt}分治疗大类{unit_type}滚动年趋势.png",
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )

            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    f"plots\\{mkt}分治疗大类{unit_type}季度趋势.png",
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )
        else:
            c = p.add_content_slide(layout_style=12)
            c.set_title(mkt)
            
            c = p.add_content_slide(layout_style=13)
            c.add_image(
                f"plots\\{mkt}分通用名滚动年趋势.png",
                width=c.body.width * 0.95,
                height=None,
                loc=c.body.center,
            )
            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    f"plots\\{mkt}分通用名{unit_type}季度趋势.png",
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )
            
            for unit_type in ["销售额", "PTD"]:
                c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                c.add_image(
                    f"plots\\{mkt}分通用名{unit_type}滚动年趋势.png",
                    width=c.body.width * 0.85,
                    height=None,
                    loc=c.body.center,
                )     
        
        if mkt != "HIF-PHI市场":
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
                            if mkt == "肾性贫血市场" or metric == "产品"
                            else f"plots\\{mkt}{MON}滚动年{metric}{unit_type}明细.png"
                        ),
                        width=c.body.width * 0.95,
                        height=None,
                        loc=c.body.center,
                    )

                if mkt == "肾性贫血市场":
                    top_text = "TOP10"
                else:
                    if metric == "通用名":
                        top_text = ""
                    else:
                        top_text = "TOP10"
                
                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(layout_style=dict_layout[f"{mkt}{unit_type}"])
                    c.add_image(
                        f"plots\\{mkt}{top_text}{metric}滚动年{unit_type}趋势.png",
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
        else:
            for metric in ["通用名", "产品"]:
                for unit_type in ["销售额", "PTD"]:
                    c = p.add_content_slide(
                        layout_style=dict_layout[f"{mkt}{unit_type}"]
                    )
                    c.add_image(
                        image_file=(
                            f"plots\\{mkt}{MON}滚动年{metric}{unit_type}明细.png"
                        ),
                        width=c.body.width * 0.85,
                        height=None,
                        loc=c.body.center,
                    )
    # 结尾页
    c = p.add_content_slide()
    c.set_title("Thank You")

    p.save(save_path=f"IQVIA CHPA最新表现Key Slides_{QTR}_{brand}.pptx")
