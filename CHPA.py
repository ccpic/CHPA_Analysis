# -*- coding: UTF-8 -*-
import numpy as np
import math
import pandas as pd
import calendar
import datetime
import time
import re
import sqlalchemy.types as t
from sqlalchemy import create_engine
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex
from matplotlib.colors import LinearSegmentedColormap
from pandas.plotting import register_matplotlib_converters
from adjustText import adjust_text
import matplotlib.dates as mdates

register_matplotlib_converters()

pd.set_option("display.max_columns", 5000)
pd.set_option("display.width", 5000)
mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["font.serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams.update({"font.size": 16})
mpl.rcParams["hatch.linewidth"] = 0.5
mpl.rcParams["hatch.color"] = "grey"


myfont = fm.FontProperties(fname="C:/Windows/Fonts/msyh.ttc")

d_layout = {
    1: [1, 1],
    2: [1, 2],
    3: [1, 3],
    4: [2, 2],
    5: [2, 3],
    6: [2, 3],
    7: [2, 4],
    8: [2, 4],
    9: [3, 3],
}

d_tier = {
    "北京": "一线",
    "天津": "二线",
    "沈阳": "二线",
    "哈尔滨": "二线",
    "济南": "二线",
    "石家庄": "三线",
    "青岛": "二线",
    "长春": "三线",
    "大连": "三线",
    "上海": "一线",
    "杭州": "二线",
    "南京": "二线",
    "苏州": "二线",
    "宁波": "二线",
    "温州": "三线",
    "无锡": "二线",
    "常州": "三线",
    "合肥": "二线",
    "广州": "一线",
    "褔厦泉": "三线",
    "武汉": "二线",
    "郑州": "二线",
    "珠三角": "二线",
    "长沙": "二线",
    "深圳": "二线",
    "南宁": "三线",
    "南昌": "三线",
    "昆明": "三线",
    "乌鲁木齐": "三线",
    "太原": "三线",
    "兰州": "三线",
    "呼和浩特": "三线",
    "重庆": "二线",
    "成都": "二线",
    "西安": "二线",
    "贵阳": "三线",
}

d_region1 = {
    "北京": "北区",
    "上海": "东区",
    "广州": "南区",
    "褔厦泉": "南区",
    "重庆": "中区",
    "天津": "北区",
    "武汉": "中区",
    "杭州": "中区",
    "南京": "东区",
    "沈阳": "北区",
    "成都": "中区",
    "哈尔滨": "北区",
    "郑州": "北区",
    "珠三角": "南区",
    "济南": "东区",
    "西安": "中区",
    "石家庄": "北区",
    "青岛": "东区",
    "长春": "北区",
    "苏州": "东区",
    "长沙": "中区",
    "深圳": "南区",
    "宁波": "中区",
    "昆明": "中区",
    "乌鲁木齐": "中区",
    "温州": "中区",
    "太原": "北区",
    "大连": "北区",
    "南宁": "南区",
    "无锡": "东区",
    "南昌": "南区",
    "贵阳": "中区",
    "常州": "东区",
    "兰州": "中区",
    "呼和浩特": "北区",
    "合肥": "东区",
}

d_region2 = {
    "北京": "北京-1",
    "天津": "华北",
    "沈阳": "北京-2",
    "哈尔滨": "北京-1",
    "济南": "华北",
    "石家庄": "华北",
    "青岛": "华北",
    "长春": "其他",
    "大连": "北京-2",
    "上海": "上海",
    "杭州": "浙江",
    "南京": "苏皖",
    "苏州": "苏皖",
    "宁波": "浙江",
    "温州": "浙江",
    "无锡": "苏皖",
    "常州": "苏皖",
    "合肥": "苏皖",
    "广州": "广州",
    "褔厦泉": "闽赣",
    "武汉": "中区",
    "郑州": "中区",
    "珠三角": "广州",
    "长沙": "中区",
    "深圳": "深圳",
    "南宁": "深圳",
    "南昌": "闽赣",
    "昆明": "西区",
    "乌鲁木齐": "中区",
    "太原": "其他",
    "兰州": "其他",
    "呼和浩特": "其他",
    "重庆": "西区",
    "成都": "西区",
    "西安": "西区",
    "贵阳": "西区",
}

color_dict = {
    "阿齐沙坦":"saddlebrown",
    'β受体阻断剂':"teal",
    "MRA":"olivedrab",
    'RAAS平片(ARB+ACEI)':"crimson",
    "螺内酯":"navy",
    "非奈利酮":"crimson",
    "恒格列净": "darkgreen",
    "伊伐布雷定": "navy",
    "美托洛尔": "navy",
    "艾司洛尔": "crimson",
    "比索洛尔": "darkorange",
    "阿罗洛尔": "darkgreen",
    "拉贝洛尔": "olivedrab",
    "DA FEN GAI (SZA)": "darkgreen",
    "二甲双胍": "navy",
    "DPP4": "crimson",
    "SGLT2": "darkorange",
    "GLP-1": "darkgreen",
    "α糖苷酶抑制剂": "olivedrab",
    "磺脲类": "purple",
    "格列奈类": "violet",
    "TZD": "saddlebrown",
    "TZD & PPAR全激动剂": "saddlebrown",
    "V03B 中药和中成药": "darkorange",
    "依折麦布": "crimson",
    "艾普拉唑": "crimson",
    "硝苯地平缓释片": "crimson",
    "集采品种": "grey",
    "其他非集采品种": "purple",
    "美阿沙坦": "gold",
    "马来酸依那普利叶酸片（AU3）": "grey",
    "诺欣妥（NVU）": "violet",
    "ENTRESTO (NVR)": "violet",
    "缬克（JC4）": "purple",
    "兰沙（BW.）": "darkgreen",
    "沙库巴曲缬沙坦": "violet",
    "ARNI": "violet",
    "西格列汀": "navy",
    "沙格列汀": "teal",
    "维格列汀": "crimson",
    "利格列汀": "darkorange",
    "阿格列汀": "darkgreen",
    "阿卡波糖片剂": "navy",
    "阿卡波糖咀嚼片": "deepskyblue",
    "伏格列波糖": "teal",
    "米格列醇": "crimson",
    "卡格列净": "navy",
    "恩格列净": "crimson",
    "达格列净": "teal",
    "埃格列净": "darkorange",
    # "比索洛尔": "navy",
    "美托洛尔缓释剂型": "crimson",
    "美托洛尔缓释片": "crimson",
    "美托洛尔常释剂型": "teal",
    # "阿罗洛尔": "darkorange",
    "地舒单抗": "deepskyblue",
    "带量品种": "crimson",
    "非带量品种": "teal",
    "美阿沙坦钾片": "pink",
    "VBP品种": "crimson",
    "非VBP品种": "teal",
    "拜阿司匹灵": "navy",
    "BAYASPIRIN (BAY)": "navy",
    "波立维": "crimson",
    "PLAVIX (SG9)": "crimson",
    "ELCITONIN (ASC)": "gold",
    "ALENDRONATE SODIUM (S1H)": "saddlebrown",
    "Others": "grey",
    "泰嘉": "darkgreen",
    "TALCOM (SI6)": "teal",
    "CLOPIDOGREL BISULF (HDO)": "pink",
    "SHUAI XIN/SHUAI TAI (LUU)": "darkgreen",
    "YOU LI WEI (NJ2)": "gold",
    "PLAGRIL (DRL)": "deepskyblue",
    "泰仪": "olivedrab",
    "帅信": "darkgreen",
    "SHUAI XIN (LUU)": "darkgreen",
    "SHUAI TAI (LUU)": "olivedrab",
    "帅泰": "olivedrab",
    "帅信/帅泰": "saddlebrown",
    "硫酸氢氯吡格雷片": "saddlebrown",
    "倍林达": "darkorange",
    "BRILINTA (AZN)": "darkorange",
    "阿司匹林": "navy",
    "氯吡格雷": "teal",
    "吲哚布芬": "crimson",
    "替格瑞洛": "darkorange",
    "倍利舒": "purple",
    "美洛林": "deepskyblue",
    "国产阿司匹林": "grey",
    "华东区": "navy",
    "华西区": "crimson",
    "华南区": "teal",
    "华北区": "darkgreen",
    "华中区": "darkorange",
    "一线城市": "navy",
    "二线城市": "crimson",
    "三线城市": "teal",
    "四线城市": "darkgreen",
    "五线城市": "darkorange",
    "25MG10片装": "darkgreen",
    "25MG20片装": "olivedrab",
    "75MG7片装": "darkorange",
    "10MG": "slateblue",
    "15MG": "rebeccapurple",
    "20MG": "indigo",
    "吸入性糖皮质激素(ICS)": "navy",
    "短效β2受体激动剂(SABA)": "crimson",
    "长效β2受体激动剂(LABA)": "tomato",
    "抗白三烯类药物(LTRA)": "teal",
    "黄嘌呤类": "darkorange",
    "长效抗胆碱剂(LAMA)": "darkgreen",
    "短效抗胆碱剂(SAMA)": "olivedrab",
    "LABA+ICS固定复方制剂": "purple",
    "SAMA+SABA固定复方制剂": "deepskyblue",
    "非类固醇类呼吸道消炎药": "saddlebrown",
    "其他": "grey",
    "其他品种": "grey",
    "氨氯地平": "teal",
    "硝苯地平": "crimson",
    "左旋氨氯地平": "darkorange",
    "非洛地平": "navy",
    "贝尼地平": "darkgreen",
    "布地奈德": "navy",
    "丙酸倍氯米松": "crimson",
    "丙酸氟替卡松": "darkorange",
    "环索奈德": "darkgreen",
    "异丙肾上腺素": "grey",
    "特布他林": "navy",
    "沙丁胺醇": "crimson",
    "丙卡特罗": "navy",
    "福莫特罗": "crimson",
    "班布特罗": "darkorange",
    "妥洛特罗": "teal",
    "环仑特罗": "darkgreen",
    "茚达特罗": "purple",
    "孟鲁司特": "navy",
    "普仑司特": "crimson",
    "多索茶碱": "navy",
    "茶碱": "crimson",
    "二羟丙茶碱": "tomato",
    "氨茶碱": "darkorange",
    "复方胆氨": "darkgreen",
    "二羟丙茶碱氯化钠": "teal",
    "复方妥英麻黄茶碱": "olivedrab",
    "复方茶碱麻黄碱": "purple",
    "茶碱,盐酸甲麻黄碱,暴马子浸膏": "saddlebrown",
    "ARB": "teal",
    "ACEI": "crimson",
    "CCB": "navy",
    "Beta Blocker": "olivedrab",
    "Diuretics": "darkgreen",
    "RAAS FDC": "darkorange",
    "厄贝沙坦": "navy",
    "缬沙坦": "crimson",
    "缬沙坦氢氯噻嗪": "pink",
    "缬沙坦,氨氯地平": "maroon",
    "缬沙坦氨氯地平": "maroon",
    "贝那普利,氨氯地平": "salmon",
    "贝那普利氨氯地平": "salmon",
    "厄贝沙坦,氢氯噻嗪": "royalblue",
    "厄贝沙坦氢氯噻嗪": "royalblue",
    "氯沙坦氢氯噻嗪": "gold",
    "氯沙坦": "darkorange",
    "氯沙坦钾": "darkorange",
    "替米沙坦": "darkgreen",
    "奥美沙坦": "deepskyblue",
    "奥美沙坦（BW.）": "deepskyblue",
    "坎地沙坦": "olivedrab",
    "阿利沙坦": "teal",
    "代文": "navy",
    "代文（NVR）": "navy",
    "代文（NVU）": "navy",
    "DIOVAN (NVR)": "navy",
    "洛汀新": "olivedrab",
    "洛汀新（NBJ）": "olivedrab",
    "洛汀新（NVU）": "olivedrab",
    "LOTENSIN (NBJ)": "olivedrab",
    "科素亚": "darkorange",
    "科素亚（MHU）": "darkorange",
    "科素亚（MSG）": "darkorange",
    "COZAAR (ORG)": "darkorange",
    "安博维": "crimson",
    "安博维（SG9）": "crimson",
    "安博维（SA9）": "crimson",
    "APROVEL (SG9)": "crimson",
    "安博诺（SA9）": "pink",
    "COAPROVEL (SG9)": "pink",
    "VALSARTAN (QJX)": "pink",
    "雅施达": "saddlebrown",
    "雅施达（TSV）": "saddlebrown",
    "雅施达（SVU）": "saddlebrown",
    "百安新": "darkgreen",
    "百安新（YAZ）": "darkgreen",
    "BAI AN XIN (GRU)": "darkgreen",
    "倍博特（NVU）": "maroon",
    "EXFORGE (NVR)": "maroon",
    "倍博特": "maroon",
    "傲坦": "deepskyblue",
    "美卡素": "purple",
    "美卡素（B.I）": "purple",
    "必洛斯": "darkgreen",
    "信立坦": "teal",
    "信立坦（SI6）": "teal",
    "XIN LI TAN (SI6)": "teal",
    "倍悦": "purple",
    "倍悦（ZJ5）": "purple",
    "BEI YUE (ZJ5)": "purple",
    "复傲坦（DCG）": "deepskyblue",
    "缓宁": "gold",
    "安来": "gold",
    "安来（ZJ5）": "gold",
    "AN LAI (ZJ5)": "gold",
    "搏力高": "mediumslateblue",
    "搏力高（ZYG）": "mediumslateblue",
    "平欣": "mediumslateblue",
    "XIE AN ZHI (ZHU)": "mediumslateblue",
    "依苏": "coral",
    "YI SU (JJJ)": "coral",
    "YI YE (AU3)": "coral",
    "科苏": "darkgreen",
    "穗悦": "olivedrab",
    "XIE KE (JC4)": "navy",
    "AMLODIPINE BESYLAT (S5O)": "olivedrab",
    "迪之雅": "olive",
    "伊达力": "olive",
    "伊达力（ZUP）": "olive",
    "伊达力（ZHI）": "olive",
    "YI DA LI (ZUP)": "olive",
    "兰沙": "c",
    "LAN SHA (BW.)": "c",
    "倍怡": "pink",
    "倍怡（ZJ5）": "pink",
    "BEI YI (ZJ5)": "pink",
    "吉加": "orchid",
    "吉加（JSH）": "orchid",
    "吉加（H9R）": "orchid",
    "JI JIA (JSH)": "orchid",
    "卡托普利片": "grey",
    "华法林": "darkorange",
    "利伐沙班": "rebeccapurple",
    "阿哌沙班": "darkgreen",
    "依度沙班": "deepskyblue",
    "达比加群酯": "dodgerblue",
    "肝素": "crimson",
    "比伐芦定": "teal",
    "万脉舒（H2C）": "navy",
    "克赛（AVS）": "crimson",
    "立迈青（AHK）": "darkorange",
    "泰加宁（SI6）": "teal",
    "希弗全（A1L）": "darkgreen",
    "尤尼舒（J/G）": "olivedrab",
    "速避凝（A3N）": "purple",
    "赛博利（S1E）": "gold",
    "注射用那屈肝素钙（DG+）": "deepskyblue",
    "赛倍畅（JJY）": "saddlebrown",
    "齐征（QLU）": "pink",
    "普洛静（GTW）": "pink",
    "法安明（PHA）": "rebeccapurple",
    "那屈肝素钙注射液（JJY）": "saddlebrown",
    "泰加宁": "teal",
    "泽朗": "crimson",
    "泰加宁\n深圳信立泰药业股份有限公司": "teal",
    "泽朗\n江苏豪森药业集团有限公司": "crimson",
    "比伐芦定\n海南双成药业股份有限公司": "darkorange",
    "比伐芦定\n齐鲁制药集团": "deepskyblue",
    "阿托伐他汀": "navy",
    "瑞舒伐他汀": "crimson",
    "匹伐他汀": "teal",
    "氟伐他汀": "darkgreen",
    "普伐他汀": "olivedrab",
    "辛伐他汀": "darkorange",
    "洛伐他汀": "saddlebrown",
    "立普妥": "navy",
    "可定": "crimson",
    "阿乐": "darkorange",
    "尤佳": "teal",
    "瑞旨": "darkgreen",
    "京诺": "olivedrab",
    "托妥": "purple",
    "赛博利": "gold",
    "优力平": "gold",
    "注射用那屈肝素钙": "deepskyblue",
    "齐征": "pink",
    "立普妥（PFZ）": "navy",
    "立普妥（VI/）": "navy",
    "信立明（SI6）": "teal",
    "信立明": "teal",
    "可定（AZN）": "crimson",
    "可定（A5Z）": "crimson",
    "阿乐（SDS）": "darkorange",
    "尤佳（TOF）": "darkgreen",
    "瑞旨（S6B）": "olivedrab",
    "瑞旨（S7O）": "olivedrab",
    "托妥（NJ2）": "purple",
    "京诺（ZXJ）": "pink",
    "阿托伐他汀钙分散片（G6B）": "gold",
    "冠爽（BJP）": "crimson",
    "冠爽（SHN）": "crimson",
    "阿托伐他汀（ZLU）": "deepskyblue",
    "美百乐镇（DSC）": "coral",
    "美百乐镇（DCG）": "coral",
    "富利他之（ZHI）": "rebeccapurple",
    "邦之（JBI）": "saddlebrown",
    "邦之（SFO）": "saddlebrown",
    "舒降之（MHU）": "dodgerblue",
    "来适可XL（NVR）": "orchid",
    "来适可XL（NVU）": "orchid",
    "辛可（GXN）": "olive",
    "优力平（ZLU）": "saddlebrown",
    "阿托伐他汀（GI2）": "olive",
    "阿托伐他汀（FXG）": "olive",
    "瑞舒伐他汀钙片（ZHI）": "orchid",
    "瑞舒伐他汀（C2T）": "dodgerblue",
    "瑞舒伐他汀（NJ2）": "dodgerblue",
    "瑞舒伐他汀（LEK）": "olive",
    "瑞舒伐他汀（NVU）": "olive",
    "阿托伐他汀（HNQ）": "deepskyblue",
    "阿托伐他汀（QIL）": "deepskyblue",
    "阿托伐他汀（FJ.）": "pink",
    "京必舒新（ZXJ）": "darkorange",
    "冠爽": "navy",
    "邦之": "crimson",
    "力清之": "darkorange",
    "京可新": "darkgreen",
    "匹伐他汀钙片": "olivedrab",
    "京可新（ZXJ）": "darkgreen",
    "力清之（KW.）": "darkorange",
    "匹伐他汀（JN.）": "dodgerblue",
    "匹伐他汀钙片（S1Q）": "navy",
    "匹伐他汀钙片（SI6）": "olivedrab",
    "G03J0\n选择性雌激素\n受体调节剂": "navy",
    "SERM": "navy",
    "H04A0\n降钙素": "crimson",
    "降钙素": "crimson",
    "H04E0\n甲状旁腺激素\n及类似物": "darkorange",
    "PTH": "darkorange",
    "M05B3\n治疗骨质疏松\n和骨钙失调\n的二膦酸盐类": "darkgreen",
    "双膦酸盐类": "darkgreen",
    "唑来膦酸": "navy",
    "唑来膦酸（SHR）": "pink",
    "唑来膦酸（YAZ）": "darkorange",
    "达芬盖（SZA）": "dodgerblue",
    "伊疏（S.I）": "saddlebrown",
    "普罗力（AAI）": "pink",
    "普罗力": "pink",
    "PROLIA (AAI)": "pink",
    "唑来膦酸注射液": "navy",
    "鲑鱼降钙素": "crimson",
    "鲑降钙素": "crimson",
    "阿仑膦酸钠": "darkorange",
    "阿仑膦酸钠,维生素D3": "darkgreen",
    "阿仑膦酸钠维生素D3": "darkgreen",
    "依降钙素": "olivedrab",
    "利塞膦酸钠": "purple",
    "特立帕肽": "pink",
    "雷洛昔芬": "gold",
    "依替膦酸二钠": "teal",
    "密固达": "navy",
    "密固达（NVR）": "navy",
    "密固达（NVU）": "navy",
    "ACLASTA (NVR)": "navy",
    "欣复泰": "teal",
    "欣复泰（XIL）": "teal",
    "XIN FU TAI (XIL)": "teal",
    "RISEDRONATE SODIUM (YKJ)": "coral",
    "依固": "crimson",
    "依固（CTA）": "crimson",
    "依固（C2T）": "crimson",
    "YI GU (CTA)": "crimson",
    "密盖息": "darkorange",
    "密盖息（NVR）": "darkorange",
    "密盖息（NVU）": "darkorange",
    "MIACALCIC (NVR)": "darkorange",
    "福美加": "darkgreen",
    "福美加（MSD）": "darkgreen",
    "福美加（MSG）": "darkgreen",
    "FOSAMAX PLUS (ORG)": "darkgreen",
    "福善美": "olivedrab",
    "福善美（MSD）": "olivedrab",
    "福善美（MSG）": "olivedrab",
    "FOSAMAX (ORG)": "olivedrab",
    "金尔力": "purple",
    "金尔力（B-Y）": "purple",
    "JIN ER LI (B-Y)": "purple",
    "斯迪诺": "saddlebrown",
    "SI DI NUO (S-Y)": "saddlebrown",
    "利塞膦酸钠片": "gold",
    "利塞膦酸钠片（YKJ）": "gold",
    "KE MI GU (SK4)": "gold",
    "益盖宁": "teal",
    "斯迪诺（S-Y）": "teal",
    "斯迪诺（LU6）": "teal",
    "复泰奥": "deepskyblue",
    "复泰奥（LYG）": "deepskyblue",
    "FORSTEO (LLY)": "deepskyblue",
    "珍固": "crimson",
    "珍固（S60）": "crimson",
    "ZHEN GU (S60)": "crimson",
    "益盖宁（ASC）": "pink",
    "唑来膦酸注射液（SK4）": "saddlebrown",
    "唑来膦酸注射液（KEU）": "saddlebrown",
    "丙戊酸钠": "navy",
    "左乙拉西坦": "crimson",
    "奥卡西平": "darkorange",
    "硫酸镁": "darkgreen",
    "普瑞巴林": "olivedrab",
    "拉莫三嗪": "purple",
    "苯巴比妥": "pink",
    "加巴喷丁": "gold",
    "托吡酯": "teal",
    "氯硝西泮": "deepskyblue",
    "开浦兰（UCB）": "navy",
    "左乙拉西坦片（CQU）": "crimson",
    "左乙拉西坦片（ZXJ）": "darkorange",
    "左乙拉西坦（SI6）": "teal",
    "左乙拉西坦（ZJO）": "darkgreen",
    "依那普利": "saddlebrown",
    "依那普利（JJJ）": "saddlebrown",
    "依那普利（YAZ）": "saddlebrown",
    "依那普利拉": "olivedrab",
    "卡托普利": "darkorange",
    "咪达普利": "coral",
    "喹那普利": "saddlebrown",
    "培哚普利": "purple",
    "福辛普利": "teal",
    "贝那普利": "coral",
    "赖诺普利": "pink",
    "雷米普利": "deepskyblue",
    "傲坦（DSC）": "navy",
    "傲坦（DCG）": "navy",
    "OLMETEC PLUS (DSC)": "navy",
    "兰沙（B4W）": "crimson",
    "希佳（NJ2）": "darkorange",
    "希佳（C2T）": "darkorange",
    "奥美沙坦酯片（S6N）": "darkgreen",
    "天泉乐宁（FTQ）": "olivedrab",
    "奥美沙坦（FTQ）": "deepskyblue",
    "奥美沙坦（GY0）": "saddlebrown",
    "欧美利（GY0）": "saddlebrown",
    "奥美沙坦（SI6）": "teal",
    "信达悦（SI6）": "teal",
    "250MG": "navy",
    "500MG": "crimson",
    "恩存": "deepskyblue",
    "EN CUN (S1H)": "deepskyblue",
    "托平（ZHT）": "deepskyblue",
    "TUO PING (ZHT)": "deepskyblue",
    "诺欣妥": "crimson",
    "口服片剂": "navy",
    "口服溶液": "deepskyblue",
    "注射剂": "crimson",
    "A+C": "navy",
    "A+D": "darkorange",
    "B03A 补血药，铁剂": "navy",
    "B03C 红细胞生成素": "crimson",
    "B03D HIF-PH抑制剂": "teal",
    "中标仿制": "crimson",
    "未中标原研": "navy",
    "未中标仿制": "dodgerblue",
}

color_list = [
    "teal",
    "crimson",
    "navy",
    "tomato",
    "darkorange",
    "darkgreen",
    "olivedrab",
    "purple",
    "deepskyblue",
    "saddlebrown",
    "grey",
    "cornflowerblue",
    "magenta",
    "teal",
    "crimson",
    "navy",
    "tomato",
    "darkorange",
    "darkgreen",
    "olivedrab",
    "purple",
    "deepskyblue",
    "saddlebrown",
    "grey",
    "cornflowerblue",
    "magenta",
]
iter_colors = iter(color_list)
d_rename = {
    "CLASS": "治疗大类",
    "硫酸氢氯吡格雷片": "帅信/帅泰",
    "TC III": "治疗大类",
    "TC IV": "治疗大类",
    "FDC CLASS": "复方制剂类别",
    "MOLECULE": "通用名",
    "PRODUCT": "产品",
    "PRODUCT_CORP": "产品",
    "PACKAGE": "包装",
    "STRENGTH": "剂量规格",
    "FORMULATION": "剂型",
    "CITY": "城市",
    "VBP": "是否VBP",
    "VBP_STATUS": "VBP中标情况",
    "TIER": "城市层级",
    "REGION1": "大区",
    "REGION2": "区域",
    "MAT": "滚动年",
    "MQT": "滚动季",
    "QTR": "季度",
    "MTH": "单月",
    "MON": "单月",
    "Value": "销售额",
    "Volume": "销售量",
    "Volume (Counting Unit)": "销售量（片数）",
    "Volume (Std Counting Unit)": "销售量（标准片数）",
    "PTD": "PTD（病人治疗天数）",
    # 'C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药': 'ACEI',
    # 'C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药': 'ARB',
    "代文|DIOVAN             NVR": "代文",
    "洛汀新|LOTENSIN           NBJ": "洛汀新",
    "科素亚|COZAAR             MHU": "科素亚",
    "安博维|APROVEL            SG9": "安博维",
    "雅施达|ACERTIL            TSV": "雅施达",
    "傲坦|OLMETEC            DSC": "傲坦",
    "美卡素|MICARDIS           B.I": "美卡素",
    "必洛斯|BLOPRESS           T/T": "必洛斯",
    "信立坦|XIN LI TAN         SI6": "信立坦",
    # '缓宁|HUAN NING          SHR': '缓宁',
    # '倍怡|BEI YI             ZJ5': '倍怡',
    # '迪之雅|DI ZHI YA          SWY': '迪之雅',
    # '兰沙|LAN SHA            B4W': '兰沙',
    # '依苏|YI SU              J1J': '依苏',
    # '平欣|PING XIN           S6B': '平欣',
    # '吉加|JI JIA             JSH': '吉加',
    # '氯沙坦钾|LOSARTAN': '氯沙坦',
    # '厄贝沙坦|IRBESARTAN': '厄贝沙坦',
    # '福辛普利|FOSINOPRIL': '福辛普利',
    # '赖诺普利|LISINOPRIL': '赖诺普利',
    # '依那普利|ENALAPRIL': '依那普利',
    "贝那普利|BENAZEPRIL": "贝那普利",
    "培哚普利叔丁胺|PERINDOPRIL": "培哚普利",
    "培哚普利|PERINDOPRIL": "培哚普利",
    "厄贝沙坦|IRBESARTAN": "厄贝沙坦",
    "氯沙坦钾|LOSARTAN": "氯沙坦",
    "替米沙坦|TELMISARTAN": "替米沙坦",
    "奥美沙坦|OLMESARTAN MEDOXOMIL": "奥美沙坦",
    "缬沙坦|VALSARTAN": "缬沙坦",
    "缬沙坦胶囊|VALSARTAN": "缬沙坦",
    "阿利沙坦|ALLISARTAN ISOPROXIL": "阿利沙坦",
    "坎地沙坦|CANDESARTAN CILEXETIL": "坎地沙坦",
    "C03A DIURETICS|利尿剂": "Diuretics",
    "C07A BETA BLOCKING AGENT PLN|β受体阻断剂，单用": "Beta Blocker",
    "C08A CALCIUM ANTAGONISTS PLAIN|钙离子拮抗剂，单一用药": "CCB",
    "C08B CALCIUM ANTAGONISTS COMBS|钙离子拮抗剂，联合用药": "CCB",
    "C09A ACE INHIBITORS PLAIN|血管紧张素转换酶抑制剂，单一用药": "ACEI",
    "C09B ACE INHIBITORS COMBS|血管紧张素转换酶抑制剂，联合用药": "RAAS FDC",
    "C09C ANGIOTENS-II ANTAG, PLAIN|血管紧张素II拮抗剂，单一用药": "ARB",
    "C09D ANGIOTEN-II ANTAG, COMB|血管紧张素II拮抗剂，联合用药": "RAAS FDC",
    "C09X OTH RENIN-ANGIOTEN AGENT|其他血管紧张素调节剂": "RAAS FDC",
}


def change_unit(unit, text_sign, df):
    if unit == "M":
        df = df / 1000000
        if text_sign == "额":
            unit_label = "（百万元）"
        else:
            unit_label = "（百万）"
    elif unit == "k":
        df = df / 1000
        if text_sign == "额":
            unit_label = "（千元）"
        else:
            unit_label = "（千）"
    elif unit == "%":
        unit_label = "份额"
    elif unit == "+%":
        unit_label = "增长率"
    else:
        unit_label = ""
    return unit_label, df


class chpa(pd.DataFrame):
    # This class variable tells Pandas the name of the attributes
    # that are to be ported over to derivative DataFrames.  There
    # is a method named `__finalize__` that grabs these attributes
    # and assigns them to newly created `SomeData`
    _metadata = ["name"]

    @property
    def _constructor(self):
        """This is the key to letting Pandas know how to keep
        derivative `SomeData` the same type as yours.  It should
        be enough to return the name of the Class.  However, in
        some cases, `__finalize__` is not called and `my_attr` is
        not carried over.  We can fix that by constructing a callable
        that makes sure to call `__finlaize__` every time."""

        def _c(*args, **kwargs):
            return chpa(*args, **kwargs).__finalize__(self)

        return _c

    def __init__(self, *args, **kwargs):
        # grab the keyword argument that is supposed to be my_attr
        self.name = kwargs.pop("name", None)
        super().__init__(*args, **kwargs)

    def latest_date(self):
        return self["DATE"].max()

    # def latest_ya_date(self):
    #     return self.latest_date() - pd.DateOffset(years=1)

    def filtered(self, filter, filter_value, unit, period):
        if filter is not None and filter_value is not None:
            mask = (
                (self[filter].isin(filter_value))
                & (self["UNIT"] == unit)
                & (self["PERIOD"] == period)
            )
        else:
            mask = (self["UNIT"] == unit) & (self["PERIOD"] == period)
        return self.loc[mask]

    def pivot_by_group(self, filter, filter_value, index, dimension, unit, period):
        affix = d_rename[period] + d_rename[unit]

        table = pd.pivot_table(
            self.filtered(filter, filter_value, unit, period),
            values="AMOUNT",
            index=index,
            columns=dimension,
            aggfunc=np.sum,
        )

        df = pd.DataFrame()
        df[self.name] = table.sum(axis=1)  # 定义市场总体销售额
        if dimension is not None:
            df = pd.concat([df, table], axis=1)  # 加上分维度销售额
        df.columns = df.columns + affix

        return df

    def matrix_by_timeseries(
        self,
        filter,
        filter_value,
        dimension,
        return_type,
        unit,
        period,
        has_total=False,
        index=None,
    ):
        affix = d_rename[period] + d_rename[unit]

        if index is not None:
            df = self.pivot_by_group(
                filter, filter_value, [index, "DATE"], dimension, unit, period
            )
            df = df.sort_index(axis=1, level=2, ascending=False).sort_index(
                axis=1, level=[0, 1], sort_remaining=False
            )
            df = df.reset_index()

            df_combined = pd.DataFrame()
            for i, idx in enumerate(df[index].unique()):
                df2 = df[df[index] == idx]
                df2.set_index("DATE", inplace=True)
                df2.columns = df2.columns.str[: -len(affix)]
                df2.columns.values[0] = index

                if return_type == "增长率":
                    df2 = df2.pct_change(periods=4)
                elif return_type == "净增长":
                    df2 = df2.diff(periods=4)
                elif return_type == "份额":
                    for col in df2.columns:
                        if col != self.name and col != index:
                            df2[col] = df2[col].div(df2[self.name], axis=0)
                    df2[self.name] = 1
                df2.dropna(how="all", inplace=True)
                df2.replace([np.inf, -np.inf], np.nan, inplace=True)

                if has_total is False:
                    df2.drop(self.name, axis=1, inplace=True)

                if i == 0:
                    df_combined = df2
                else:
                    df_combined = pd.concat([df_combined, df2])

            df_combined.columns.values[0] = index

            return df_combined
        else:
            df = self.pivot_by_group(
                filter, filter_value, "DATE", dimension, unit, period
            )
            df.columns = df.columns.str[: -len(affix)]

            if return_type == "增长率":
                df = df.pct_change(periods=4)
            elif return_type == "净增长":
                df = df.diff(periods=4)
            elif return_type == "份额":
                for col in df.columns:
                    if col != self.name and col != index:
                        df[col] = df[col].div(df[self.name], axis=0)
                df[self.name] = 1
            df.dropna(how="all", inplace=True)

            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            if has_total is False:
                df.drop(self.name, axis=1, inplace=True)

            return df

    def matrix_by_group(self, index, dimension, date, unit, period):
        affix = d_rename[period] + d_rename[unit]

        df = self.pivot_by_group("DATE", date, index, dimension, unit, period)
        df_ya = self.pivot_by_group(
            "DATE", [date[0] - pd.DateOffset(years=1)], index, dimension, unit, period
        )

        df_diff = df - df_ya  # 同比净增长
        df_diff.columns = df_diff.columns + "净增长"

        df_gr = df / df_ya - 1  # 同比增长率
        df_gr.columns = df_gr.columns + "增长率"
        df_gr.replace([np.inf, -np.inf], np.nan, inplace=True)
        df_combined = pd.concat([df, df_diff, df_gr], axis=1)

        if dimension is not None:
            df_ei = pd.DataFrame()
            for element in self[dimension].unique():
                print(df_gr[element + affix + "增长率"], df_gr[self.name + affix + "增长率"])
                df_ei[element + affix + "EI"] = (
                    (df_gr[element + affix + "增长率"] + 1)
                    / (df_gr[self.name + affix + "增长率"] + 1)
                    * 100
                )  # 同比EI
            df_combined = pd.concat([df_combined, df_ei], axis=1)

        return df_combined

    def plot_stackedbar(
        self,
        df,
        df_share,
        column,
        title,
        ytitle,
        threshold=False,
        threshold_color=None,
        yunit="M",
        yfmt="{:.0f}",
        show_grid=True,
        width=18,
        height=7,
    ):

        unit_label = change_unit(unit=yunit, text_sign=ytitle[-1], df=df)[0]
        df = change_unit(unit=yunit, text_sign=ytitle[-1], df=df)[1]

        fig, ax = plt.subplots()
        fig.set_size_inches(width, height)
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda y, _: yfmt.format(y))
        )  # 主坐标轴Y轴格式
        print(df)
        for index in df.index:
            bottom = 0
            for i, col in enumerate(df):
                if col in color_dict.keys():
                    color = color_dict[col]
                else:
                    color = color_list[i]
                hatch = ""
                if col == column:
                    hatch = "+++"
                if (
                    col == column
                    and threshold is not None
                    and df_share.loc[index, col] < threshold
                ):
                    color = threshold_color

                ax.bar(
                    index,
                    df.loc[index, col],
                    width=60,
                    color=color,
                    bottom=bottom,
                    hatch=hatch,
                )
                if df_share.loc[index, col] > 0.02:
                    plt.text(
                        index,
                        bottom + df.loc[index, col] / 2,
                        "{:.0%}".format(df_share.loc[index, col]),
                        color="white",
                        va="center",
                        ha="center",
                        fontsize=14,
                    )
                bottom += df.loc[index, col]

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(
            df.columns,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            frameon=False,
            prop={"family": "SimHei"},
        )

        # x轴文字方向
        ax.set_xticks(df.index)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment="center")

        # 轴标题
        plt.title(title, fontproperties=myfont)
        # ax.set_xlabel(xtitle, fontproperties=myfont, fontsize=12)
        ax.set_ylabel(ytitle + unit_label, fontproperties=myfont, fontsize=12)

        # 自定义主要网格
        if show_grid is True:
            plt.grid(which="major", linestyle=":", linewidth="1", color="grey")

        # 保存
        plt.savefig(
            "./plots/" + title + ".png",
            format="png",
            bbox_inches="tight",
            transparent=True,
            dpi=600,
        )
        print("./plots/" + title + ".png saved...")

    def plot_stackedbar_line(
        self,
        df_bar,
        df_line,
        hline_label,
        hline_value,
        title,
        xtitle,
        y1title,
        y2title,
        y1unit="M",
        y2fmt="{:+.1%}",
        y2lim=None,
    ):

        unit_label = change_unit(unit=y1unit, text_sign=y1title[-1], df=df_bar)[0]
        df_bar = change_unit(unit=y1unit, text_sign=y1title[-1], df=df_bar)[1]

        fig, ax = plt.subplots()
        fig.set_size_inches(14, 7)
        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda y, _: "{:,.0f}".format(y))
        )  # 主坐标轴Y轴格式

        df_bar.plot(
            kind="bar",
            stacked=True,
            title=title,
            color=["teal", "crimson"],
            ax=ax,
            grid=False,
        )  # 主坐标轴柱状图

        ax2 = ax.twinx()  # 副坐标轴共享x轴
        ax2.yaxis.set_major_formatter(
            FuncFormatter(lambda y, _: y2fmt.format(y))
        )  # 副坐标轴Y轴格式
        # ax2.axhline(0, linestyle='--', linewidth=1, color='r')
        ax2.axhline(hline_value, linestyle="--", linewidth=1, color="r")
        plt.text(
            ax.get_xlim()[1],
            hline_value,
            hline_label + "\n" + y2fmt.format(hline_value),
            ha="left",
            va="center",
            color="r",
            multialignment="center",
            fontproperties=myfont,
            fontsize=8,
        )

        df_line.plot(
            kind="line",
            color="darkorange",
            ax=ax2,
            linewidth=2,
            marker="o",
            markersize=5,
            markerfacecolor="white",
        )  # 次坐标轴线图

        # 组合图例
        bars, labels = ax.get_legend_handles_labels()
        line, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(bars + line, labels + labels2, loc="upper right", fontsize=10)
        ax.get_legend().remove()

        # 轴标题
        ax.set_xlabel(xtitle, fontproperties=myfont, fontsize=12)
        ax.set_ylabel(y1title + unit_label, fontproperties=myfont, fontsize=12)
        ax2.set_ylabel(y2title, fontproperties=myfont, fontsize=12)

        # 设置y轴此坐标轴上下限
        if y2lim is not None:
            ax2.set_ylim(ymin=y2lim[0], ymax=y2lim[1])

        # 自定义主要网格
        plt.grid(which="major", linestyle=":", linewidth="1", color="grey")

        # 保存
        plt.savefig(
            "./plots/" + title + ".png",
            format="png",
            bbox_inches="tight",
            transparent=True,
            dpi=600,
        )
        print("./plots/" + title + ".png saved...")

        # 关闭图像对象释放内存
        plt.clf()
        plt.cla()
        plt.close()

    def plot_bubble(
        self,
        x,
        y,
        z,
        labels,
        title,
        xtitle,
        ytitle,
        xfmt="{:.0%}",
        yfmt="{:+.0%}",
        yavgline=False,
        yavg=None,
        ylabel="",
        xavgline=False,
        xavg=None,
        xlabel="",
        ylim=None,
        xlim=None,
        yunit=None,
        xunit=None,
        showLabel=True,
        labelLimit=15,
    ):

        y_unit_label = change_unit(unit=yunit, text_sign=ytitle[-1], df=y)[0]
        y = change_unit(unit=yunit, text_sign=ytitle[-1], df=y)[1]
        x_unit_label = change_unit(unit=xunit, text_sign=xtitle[-1], df=x)[0]
        x = change_unit(unit=xunit, text_sign=xtitle[-1], df=x)[1]

        fig, ax = plt.subplots()
        fig.set_size_inches(14, 7)

        if ylim is not None:
            ax.set_ylim(ymin=ylim[0], ymax=ylim[1])
        if xlim is not None:
            ax.set_xlim(xmin=xlim[0], xmax=xlim[1])

        cmap = mpl.colors.ListedColormap(np.random.rand(256, 3))
        colors = iter(cmap(np.linspace(0, 1, len(y))))

        for i in range(len(x)):
            ax.scatter(
                x[i], y[i], z[i], color=next(colors), alpha=0.6, edgecolors="black"
            )
        if yavgline == True:
            ax.axhline(yavg, linestyle="--", linewidth=1, color="r")
        if xavgline == True:
            ax.axvline(xavg, linestyle="--", linewidth=1, color="r")
        # ax.scatter(x, y, s=z, c=color, alpha=0.6, edgecolors="grey")
        # ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')

        ax.xaxis.set_major_formatter(FuncFormatter(lambda y, _: xfmt.format(y)))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: yfmt.format(y)))

        np.random.seed(0)
        # for i, txt in enumerate(labels):
        #     text = plt.text(x[i],y[i], txt+"\n"+ '('+ str("{:.1%}".format(x[i])) +', ' + str("{:.1%}".format(y[i])) + ')', ha='center', va='center')
        if showLabel is True:
            texts = [
                plt.text(
                    x[i],
                    y[i],
                    labels[i],
                    ha="center",
                    va="center",
                    multialignment="center",
                    fontproperties=myfont,
                    fontsize=10,
                )
                for i in range(len(labels[:labelLimit]))
            ]
            adjust_text(
                texts, force_text=0.1, arrowprops=dict(arrowstyle="->", color="black")
            )

        if yavgline == True:
            plt.text(
                ax.get_xlim()[1],
                yavg,
                ylabel,
                ha="left",
                va="center",
                color="r",
                multialignment="center",
                fontproperties=myfont,
                fontsize=10,
            )
        if xavgline == True:
            plt.text(
                xavg,
                ax.get_ylim()[1],
                xlabel,
                ha="left",
                va="top",
                color="r",
                multialignment="center",
                fontproperties=myfont,
                fontsize=10,
            )

        plt.title(title, fontproperties=myfont)
        plt.xlabel(xtitle + x_unit_label, fontproperties=myfont, fontsize=12)
        plt.ylabel(ytitle + y_unit_label, fontproperties=myfont, fontsize=12)

        # Save
        plt.savefig(
            "./plots/" + title + ".png",
            format="png",
            bbox_inches="tight",
            transparent=True,
            dpi=200,
        )
        print("./plots/" + title + ".png saved...")

        # Close
        plt.clf()
        plt.cla()
        plt.close()

    def plot_line(
        self,
        df,
        column,
        title,
        ytitle,
        ylim=None,
        yfmt="{:.1%}",
        ignore_list=None,
    ):
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 7))
        ax = plt.subplot(1, 1, 1)

        count = 0
        for i, col in enumerate(df):
            markerstyle = "o"
            if col == column:
                markerstyle = "D"
            linewidth = 1
            if col == column:
                linewidth = 2
            if col in color_dict.keys():
                color = color_dict[col]
            else:
                color = color_list[i]
            if ignore_list is None:
                ax.plot(
                    df.index,
                    df[col],
                    color=color,
                    linewidth=linewidth,
                    label=col,
                    marker=markerstyle,
                    markersize=5,
                    markerfacecolor="white",
                    markeredgecolor=color,
                )
                endpoint = -1
                while np.isnan(df.values[endpoint][count]) or df.values[endpoint][
                    count
                ] == float("inf"):
                    endpoint = endpoint - 1
                    if abs(endpoint) == len(df.index):
                        break
                if abs(endpoint) < len(df.index):
                    # if df1.values[endpoint][count] <= 3:
                    plt.text(
                        df.index[endpoint] + pd.DateOffset(days=10),
                        df.values[endpoint][count],
                        yfmt.format(df.values[endpoint][count]),
                        ha="left",
                        va="center",
                        fontsize=12,
                        color=color,
                    )

                startpoint = 0
                while np.isnan(df.values[startpoint][count]) or df.values[startpoint][
                    count
                ] == float("inf"):
                    startpoint = startpoint + 1
                    if startpoint == len(df.index):
                        break

                if startpoint < len(df.index):
                    plt.text(
                        df.index[startpoint] - pd.DateOffset(days=10),
                        df.values[startpoint][count],
                        yfmt.format(df.values[startpoint][count]),
                        ha="right",
                        va="center",
                        fontsize=12,
                        color=color,
                    )

            else:
                if col not in ignore_list:
                    ax.plot(
                        df.index,
                        df[col],
                        color=color,
                        linewidth=linewidth,
                        label=col,
                        marker=markerstyle,
                        markersize=5,
                        markerfacecolor="white",
                        markeredgecolor=color,
                    )

                    endpoint = -1
                    while np.isnan(df.values[endpoint][count]) or df.values[endpoint][
                        count
                    ] == float("inf"):
                        endpoint = endpoint - 1
                        if abs(endpoint) == len(df.index):
                            break
                    if abs(endpoint) < len(df.index):
                        # if df1.values[endpoint][count] <= 3:
                        plt.text(
                            df.index[endpoint],
                            df.values[endpoint][count],
                            yfmt.format(df.values[endpoint][count]),
                            ha="left",
                            va="center",
                            fontsize=10,
                            color=color,
                        )

                    startpoint = 0
                    while np.isnan(df.values[startpoint][count]) or df.values[
                        startpoint
                    ][count] == float("inf"):
                        startpoint = startpoint + 1
                        if startpoint == len(df.index):
                            break

                    if startpoint < len(df.index):
                        plt.text(
                            df.index[startpoint],
                            df.values[startpoint][count],
                            yfmt.format(df.values[startpoint][count]),
                            ha="right",
                            va="center",
                            fontsize=10,
                            color=color,
                        )
            count += 1

        df.index = df.index.strftime("%Y-%m")
        ax.set_xticks(df.index)
        ax.set_xticklabels(df.index)
        ax.grid(which="both", linestyle=":", linewidth="0.5", color="grey")
        if ylim is not None:
            ax.set_ylim(ylim[0], ylim[1])
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: yfmt.format(y)))

        # plt.tick_params(
        #     axis='x',  # changes apply to the x-axis
        #     which='both',  # both major and minor ticks are affected
        #     bottom='off',  # ticks along the bottom edge are off
        #     top='off',  # ticks along the top edge are off
        #     labelbottom='on')
        plt.setp(
            ax.get_xticklabels(), rotation=90, horizontalalignment="center", fontsize=12
        )

        # ax.legend(df1, loc='center right', prop=myfont, frameon=False)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(
            df.columns,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            labelspacing=1,
            frameon=False,
            prop={"family": "SimHei", "size": 12},
        )

        plt.suptitle(title, fontproperties=myfont, fontsize=20)
        fig.text(
            0.05,
            0.5,
            ytitle,
            va="center",
            rotation="vertical",
            fontproperties=myfont,
            fontsize=16,
        )

        plt.savefig(
            "./plots/" + title + ".png",
            format="png",
            transparent=True,
            bbox_inches="tight",
            dpi=400,
        )

    def plot_line_twin(
        self,
        df1,
        df2,
        column,
        title,
        xtitle1,
        xtitle2,
        ytitle,
        ylim1=None,
        ylim2=None,
        yfmt1="{:.1%}",
        yfmt2="{:+.1%}",
        ignore_list=None,
    ):
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(19, 6))
        ax1 = plt.subplot(1, 2, 1)

        count = 0
        for i, col in enumerate(df1):
            markerstyle = "o"
            if col == column:
                markerstyle = "D"
            linewidth = 1
            if col == column:
                linewidth = 2
            if col in color_dict.keys():
                color = color_dict[col]
            else:
                color = color_list[i]
            if ignore_list is None:
                ax1.plot(
                    df1.index,
                    df1[col],
                    color=color,
                    linewidth=linewidth,
                    label=col,
                    marker=markerstyle,
                    markersize=5,
                    markerfacecolor="white",
                    markeredgecolor=color,
                )
                endpoint = -1
                while np.isnan(df1.values[endpoint][count]) or df1.values[endpoint][
                    count
                ] == float("inf"):
                    endpoint = endpoint - 1
                    if abs(endpoint) == len(df1.index):
                        break
                if abs(endpoint) < len(df1.index):
                    # if df1.values[endpoint][count] <= 3:
                    plt.text(
                        df1.index[endpoint] + pd.DateOffset(days=10),
                        df1.values[endpoint][count],
                        yfmt1.format(df1.values[endpoint][count]),
                        ha="left",
                        va="center",
                        fontsize=12,
                        color=color,
                    )

                startpoint = 0
                while np.isnan(df1.values[startpoint][count]) or df1.values[startpoint][
                    count
                ] == float("inf"):
                    startpoint = startpoint + 1
                    if startpoint == len(df1.index):
                        break

                if startpoint < len(df1.index):
                    plt.text(
                        df1.index[startpoint] - pd.DateOffset(days=10),
                        df1.values[startpoint][count],
                        yfmt1.format(df1.values[startpoint][count]),
                        ha="right",
                        va="center",
                        fontsize=12,
                        color=color,
                    )

            else:
                if col not in ignore_list:
                    ax1.plot(
                        df1.index,
                        df1[col],
                        color=color,
                        linewidth=linewidth,
                        label=col,
                        marker=markerstyle,
                        markersize=5,
                        markerfacecolor="white",
                        markeredgecolor=color,
                    )

                    endpoint = -1
                    while np.isnan(df1.values[endpoint][count]) or df1.values[endpoint][
                        count
                    ] == float("inf"):
                        endpoint = endpoint - 1
                        if abs(endpoint) == len(df1.index):
                            break
                    if abs(endpoint) < len(df1.index):
                        # if df1.values[endpoint][count] <= 3:
                        plt.text(
                            df1.index[endpoint],
                            df1.values[endpoint][count],
                            yfmt1.format(df1.values[endpoint][count]),
                            ha="left",
                            va="center",
                            fontsize=10,
                            color=color,
                        )

                    startpoint = 0
                    while np.isnan(df1.values[startpoint][count]) or df1.values[
                        startpoint
                    ][count] == float("inf"):
                        startpoint = startpoint + 1
                        if startpoint == len(df1.index):
                            break

                    if startpoint < len(df1.index):
                        plt.text(
                            df1.index[startpoint],
                            df1.values[startpoint][count],
                            yfmt1.format(df1.values[startpoint][count]),
                            ha="right",
                            va="center",
                            fontsize=10,
                            color=color,
                        )
            count += 1

        df1.index = df1.index.strftime("%Y-%m")
        ax1.set_xticks(df1.index)
        ax1.set_xticklabels(df1.index)
        ax1.grid(which="both", linestyle=":", linewidth="0.5", color="grey")
        if ylim1 is not None:
            ax1.set_ylim(ylim1[0], ylim1[1])
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: yfmt1.format(y)))
        ax1.set_title(xtitle1, fontproperties=myfont)

        # plt.tick_params(
        #     axis='x',  # changes apply to the x-ax1is
        #     which='both',  # both major and minor ticks are affected
        #     bottom='off',  # ticks along the bottom edge are off
        #     top='off',  # ticks along the top edge are off
        #     labelbottom='on')
        plt.setp(
            ax1.get_xticklabels(),
            rotation=90,
            horizontalalignment="center",
            fontsize=12,
        )

        # ax1.legend(df1, loc='center right', prop=myfont, frameon=False)
        box = ax1.get_position()
        ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax1.legend(
            df1.columns,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            labelspacing=1,
            frameon=False,
            prop={"family": "SimHei", "size": 12},
        )

        ax2 = plt.subplot(1, 2, 2)

        count = 0
        for i, col in enumerate(df2):
            markerstyle = "o"
            if col == column:
                markerstyle = "D"
            linewidth = 1
            if col == column:
                linewidth = 2
            if col in color_dict.keys():
                color = color_dict[col]
            else:
                color = color_list[i]
            if ignore_list is None:
                ax2.plot(
                    df2.index,
                    df2[col],
                    color=color,
                    linewidth=linewidth,
                    label=col,
                    marker=markerstyle,
                    markersize=5,
                    markerfacecolor="white",
                    markeredgecolor=color,
                )
                endpoint = -1
                while np.isnan(df2.values[endpoint][count]) or df2.values[endpoint][
                    count
                ] == float("inf"):
                    endpoint = endpoint - 1
                    if abs(endpoint) == len(df2.index):
                        break
                if abs(endpoint) < len(df2.index):
                    # if df2.values[endpoint][count] <= 3:
                    plt.text(
                        df2.index[endpoint] + pd.DateOffset(days=10),
                        df2.values[endpoint][count],
                        yfmt2.format(df2.values[endpoint][count]),
                        ha="left",
                        va="center",
                        fontsize=12,
                        color=color,
                    )

                startpoint = 0
                while np.isnan(df2.values[startpoint][count]) or df2.values[startpoint][
                    count
                ] == float("inf"):
                    startpoint = startpoint + 1
                    if startpoint == len(df2.index):
                        break

                if startpoint < len(df2.index):
                    plt.text(
                        df2.index[startpoint] - pd.DateOffset(days=10),
                        df2.values[startpoint][count],
                        yfmt2.format(df2.values[startpoint][count]),
                        ha="right",
                        va="center",
                        fontsize=12,
                        color=color,
                    )

            else:
                if col not in ignore_list:
                    ax2.plot(
                        df2.index,
                        df2[col],
                        color=color,
                        linewidth=linewidth,
                        label=col,
                        marker=markerstyle,
                        markersize=5,
                        markerfacecolor="white",
                        markeredgecolor=color,
                    )

                    endpoint = -1
                    while np.isnan(df2.values[endpoint][count]) or df2.values[endpoint][
                        count
                    ] == float("inf"):
                        endpoint = endpoint - 1
                        if abs(endpoint) == len(df2.index):
                            break
                    if abs(endpoint) < len(df2.index):
                        # if df2.values[endpoint][count] <= 3:
                        plt.text(
                            df2.index[endpoint],
                            df2.values[endpoint][count],
                            yfmt2.format(df2.values[endpoint][count]),
                            ha="left",
                            va="center",
                            fontsize=10,
                            color=color,
                        )

                    startpoint = 0
                    while np.isnan(df2.values[startpoint][count]) or df2.values[
                        startpoint
                    ][count] == float("inf"):
                        startpoint = startpoint + 1
                        if startpoint == len(df2.index):
                            break

                    if startpoint < len(df2.index):
                        plt.text(
                            df2.index[startpoint],
                            df2.values[startpoint][count],
                            yfmt2.format(df2.values[startpoint][count]),
                            ha="right",
                            va="center",
                            fontsize=10,
                            color=color,
                        )
            count += 1

        df2.index = df2.index.strftime("%Y-%m")
        ax2.set_xticks(df2.index)
        ax2.set_xticklabels(df2.index)
        ax2.grid(which="both", linestyle=":", linewidth="0.5", color="grey")
        if ylim2 is not None:
            ax2.set_ylim(ylim2[0], ylim2[1])
        ax2.yaxis.set_visible(True)
        ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: yfmt2.format(y)))
        ax2.set_title(xtitle2, fontproperties=myfont)

        # plt.tick_params(
        #     axis='x',  # changes apply to the x-ax2is
        #     which='both',  # both major and minor ticks are affected
        #     bottom='off',  # ticks along the bottom edge are off
        #     top='off',  # ticks along the top edge are off
        #     labelbottom='on')
        plt.setp(
            ax2.get_xticklabels(),
            rotation=90,
            horizontalalignment="center",
            fontsize=12,
        )

        # ax2.legend(df2, loc='center right', prop=myfont, frameon=False)
        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax2.legend(
            df2.columns,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            labelspacing=1,
            frameon=False,
            prop={"family": "SimHei", "size": 12},
        )

        plt.suptitle(title, fontproperties=myfont, fontsize=20)
        # fig.text(0.5, 0.05, xtitle2, ha='center', fontproperties=myfont, fontsize=16)
        fig.text(
            0.05,
            0.5,
            ytitle,
            va="center",
            rotation="vertical",
            fontproperties=myfont,
            fontsize=16,
        )

        plt.savefig(
            "./plots/" + title + ".png",
            format="png",
            transparent=True,
            bbox_inches="tight",
            dpi=600,
        )

    def plot_line_grid(
        self,
        df,
        index,
        index_list,
        column,
        title,
        xtitle,
        ytitle,
        ylim=[0, 1],
        yfmt="{:.1%}",
        ignore_list=None,
    ):
        layout = d_layout[len(index_list)]
        fig, axes = plt.subplots(
            nrows=layout[0], ncols=layout[1], sharex=True, figsize=(14, 7)
        )

        for i, idx in enumerate(index_list):

            df2 = df[df[index] == idx]
            df2.drop(index, axis=1, inplace=True)

            ax = plt.subplot(layout[0], layout[1], i + 1)

            count = 0
            for col in df2:
                markerstyle = "o"
                if col == column:
                    markerstyle = "D"
                linewidth = 1
                if col == column:
                    linewidth = 2
                if col in color_dict.keys():
                    color = color_dict[col]
                else:
                    color = color_list[i]
                if ignore_list is None:
                    ax.plot(
                        df2.index,
                        df2[col],
                        color=color,
                        linewidth=linewidth,
                        label=col,
                        marker=markerstyle,
                        markersize=5,
                        markerfacecolor="white",
                        markeredgecolor=color,
                    )
                    endpoint = -1
                    while np.isnan(df2.values[endpoint][count]) or df2.values[endpoint][
                        count
                    ] == float("inf"):
                        endpoint = endpoint - 1
                        if abs(endpoint) == len(df2.index):
                            break
                    if abs(endpoint) < len(df2.index):
                        # if df2.values[endpoint][count] <= 3:
                        plt.text(
                            df2.index[endpoint] + pd.DateOffset(days=10),
                            df2.values[endpoint][count],
                            yfmt.format(df2.values[endpoint][count]),
                            ha="left",
                            va="center",
                            fontsize=12,
                            color=color,
                        )

                    startpoint = 0
                    while np.isnan(df2.values[startpoint][count]) or df2.values[
                        startpoint
                    ][count] == float("inf"):
                        startpoint = startpoint + 1
                        if startpoint == len(df2.index):
                            break

                    if startpoint < len(df2.index):
                        plt.text(
                            df2.index[startpoint] - pd.DateOffset(days=10),
                            df2.values[startpoint][count],
                            yfmt.format(df2.values[startpoint][count]),
                            ha="right",
                            va="center",
                            fontsize=12,
                            color=color,
                        )

                else:
                    if col not in ignore_list:
                        ax.plot(
                            df2.index,
                            df2[col],
                            color=color,
                            linewidth=linewidth,
                            label=col,
                            marker=markerstyle,
                            markersize=5,
                            markerfacecolor="white",
                            markeredgecolor=color,
                        )

                        endpoint = -1
                        while np.isnan(df2.values[endpoint][count]) or df2.values[
                            endpoint
                        ][count] == float("inf"):
                            endpoint = endpoint - 1
                            if abs(endpoint) == len(df2.index):
                                break
                        if abs(endpoint) < len(df2.index):
                            # if df2.values[endpoint][count] <= 3:
                            plt.text(
                                df2.index[endpoint],
                                df2.values[endpoint][count],
                                yfmt.format(df2.values[endpoint][count]),
                                ha="left",
                                va="center",
                                fontsize=10,
                                color=color,
                            )

                        startpoint = 0
                        while np.isnan(df2.values[startpoint][count]) or df2.values[
                            startpoint
                        ][count] == float("inf"):
                            startpoint = startpoint + 1
                            if startpoint == len(df2.index):
                                break

                        if startpoint < len(df2.index):
                            plt.text(
                                df2.index[startpoint],
                                df2.values[startpoint][count],
                                yfmt.format(df2.values[startpoint][count]),
                                ha="right",
                                va="center",
                                fontsize=10,
                                color=color,
                            )
                count += 1

            ax.grid(which="both", linestyle=":", linewidth="0.5", color="grey")
            ax.set_ylim(ylim[0], ylim[1])
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: yfmt.format(y)))
            ax.set_title(idx, fontproperties=myfont)
            ax.label_outer()

            plt.tick_params(
                axis="x",  # changes apply to the x-axis
                which="both",  # both major and minor ticks are affected
                bottom="off",  # ticks along the bottom edge are off
                top="off",  # ticks along the top edge are off
                labelbottom="on",
            )
            plt.setp(
                ax.get_xticklabels(),
                rotation=90,
                horizontalalignment="center",
                fontsize=12,
            )

        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc="center right", prop=myfont, frameon=False)
        plt.suptitle(title, fontproperties=myfont, fontsize=20)
        fig.text(0.5, 0.05, xtitle, ha="center", fontproperties=myfont, fontsize=16)
        fig.text(
            0.05,
            0.5,
            ytitle,
            va="center",
            rotation="vertical",
            fontproperties=myfont,
            fontsize=16,
        )

        plt.subplots_adjust(
            right=0.85,
        )

        if len(index_list) in [5, 7]:
            fig.delaxes(axes.flat[-1])

        plt.savefig(
            "./plots/" + title + "_" + "_".join(index_list) + ".png",
            format="png",
            transparent=True,
            bbox_inches="tight",
            dpi=600,
        )

    def plot_barh(
        self,
        df,
        stacked=True,
        width=15,
        height=9,
        xfmt="{:.0f}",
        yfmt="{:.0%}",
        labelfmt="{:.0%}",
        title=None,
        xtitle=None,
        ytitle=None,
        ymin=None,
        ymax=None,
        haslegend=True,
    ):

        colors = []
        for item in df.columns.tolist():
            print(item)
            colors.append(color_dict[item])
        ax = df.plot(
            kind="barh",
            stacked=stacked,
            figsize=(width, height),
            alpha=0.8,
            edgecolor="black",
            color=colors,
        )
        plt.title(title, fontproperties=myfont, fontsize=18)
        plt.xlabel(xtitle, fontproperties=myfont)
        plt.ylabel(ytitle, fontproperties=myfont)
        plt.axvline(x=0, linewidth=2, color="r")

        if haslegend == True:
            plt.legend(
                loc="center left", bbox_to_anchor=(1.0, 0.5), prop=myfont, fontsize=12
            )
        else:
            plt.legend(prop=myfont)

        # plt.setp(ax.get_xticklabels(), rotation=0, horizontalalignment='center')
        #
        # ax.xaxis.set_major_formatter(FuncFormatter(lambda y, _: xfmt.format(y)))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: yfmt.format(y)))
        # ax.set_ylim([ymin, ymax])

        # Add value label
        labels = []
        for j in df.columns:
            for i in df.index:
                label = str(df.loc[i][j])
                labels.append(label)

        patches = ax.patches

        for label, rect in zip(labels, patches):
            height = rect.get_height()
            if height > 0.015:
                x = rect.get_x()
                y = rect.get_y()
                width = rect.get_width()
                if abs(width) < 3000000:
                    color = "black"
                else:
                    color = "white"
                ax.text(
                    x + width / 2.0,
                    y + height / 2.0,
                    labelfmt.format(float(label)),
                    ha="center",
                    va="center",
                    color=color,
                    fontproperties=myfont,
                    fontsize=10,
                )

        # Save the figure
        plt.savefig(
            "./plots/" + title.replace("\n", "") + ".png",
            format="png",
            bbox_inches="tight",
            transparent=True,
            dpi=600,
        )

        # Close
        plt.clf()
        plt.cla()
        plt.close()

    def plot_pie(self, sizelist, labellist, column, title):

        # sns.set_style("white")

        # Prepare the white center circle for Donat shape
        my_circle = plt.Circle((0, 0), 0.7, color="white")

        sizelist = sizelist.transform(lambda x: x / x.sum())
        print(sizelist)
        sizelist_mask = []
        for size in sizelist:
            sizelist_mask.append(abs(size))

        # Draw the pie chart
        wedges, texts, autotexts = plt.pie(
            sizelist_mask,
            labels=labellist,
            autopct="%1.1f%%",
            pctdistance=0.85,
            wedgeprops={"linewidth": 3, "edgecolor": "white"},
            textprops={"family": "Simhei"},
        )

        for i, pie_wedge in enumerate(wedges):
            pie_wedge.set_facecolor(color_dict[pie_wedge.get_label()])

            if column is not None:
                if pie_wedge.get_label() == column:
                    pie_wedge.set_hatch("//")
            if sizelist[i] < 0:
                pie_wedge.set_facecolor("white")

        for i, autotext in enumerate(autotexts):
            autotext.set_color("white")
            autotext.set_fontsize(10)
            autotext.set_text("{:.1%}".format(sizelist[i]))
            if sizelist[i] < 0:
                autotext.set_color("r")

        # Add title at the center
        plt.text(
            0,
            0,
            title,
            horizontalalignment="center",
            verticalalignment="center",
            size=20,
            fontproperties=myfont,
        )

        # Combine circle part and pie part
        fig = plt.gcf()
        fig.set_size_inches(6, 6)
        fig.gca().add_artist(my_circle)

        # Save
        plt.savefig(
            "./plots/" + title.replace("\n", "") + ".png",
            format="png",
            transparent=True,
            bbox_inches="tight",
            dpi=600,
        )
        print(title)

        # Close
        plt.clf()
        plt.cla()
        plt.close()

    def plot_share(
        self,
        dimension,
        column,
        return_type,
        unit="Value",
        period="MAT",
        series_limit=10,
    ):
        affix = d_rename[period] + d_rename[unit]
        df = self.matrix_by_group(
            index=dimension,
            dimension=None,
            date=[self.latest_date()],
            unit=unit,
            period=period,
        )
        df.sort_values(by=self.name + affix, ascending=False, inplace=True)

        if df.shape[0] > series_limit:
            df2 = df.iloc[:series_limit, :]
            others = df.iloc[series_limit:, :].sum()
            others.name = "其他"
            df2 = df2.append(others)

            if column is not None:
                print(column in df2.index.values)
                if column not in df2.index.values:
                    df2 = df2.append(df.loc[column, :])
                    df2.loc["其他", :] = df2.loc["其他", :].subtract(df2.loc[column, :])
        else:
            df2 = df

        if return_type == "份额":
            df2 = df2[self.name + affix]
        elif return_type == "净增长贡献":
            df2 = df2.loc[:, [self.name + affix, self.name + affix + "净增长"]]
            df2 = df2.loc[:, self.name + affix + "净增长"]

        title1 = self.name + "\n" + affix + "\n" + return_type
        title2 = self.name + affix + return_type
        xtitle = affix + return_type
        if df2.sum() > 0:
            self.plot_pie(
                sizelist=df2, labellist=df2.index, column=column, title=title1
            )
        else:
            self.plot_barh(
                df=df2.to_frame().T,
                stacked=False,
                width=9,
                height=9,
                labelfmt="{:,.0f}",
                title=title2,
                xtitle=xtitle,
                ytitle="",
                haslegend=False,
            )
        return df2

    def plot_stackedbar_plus(
        self, df, df_share, df_gr, column, title, ytitle, yunit="M", width=14, height=6
    ):
        unit_label = change_unit(unit=yunit, text_sign=ytitle[-1], df=df)[0]
        df = change_unit(unit=yunit, text_sign=ytitle[-1], df=df)[1]

        fig, ax = plt.subplots()
        fig.set_size_inches(width, height)
        df.index = df.index.strftime("%Y-%m")
        df_share.index = df_share.index.strftime("%Y-%m")
        df_gr.index = df_gr.index.strftime("%Y-%m")
        print(df, df_share, df_gr)

        for index in df.index:
            bottom = 0
            for i, col in enumerate(df):
                if col in color_dict.keys():
                    color = color_dict[col]
                else:
                    color = color_list[i]
                ax.bar(
                    index,
                    df.loc[index, col],
                    width=0.5,
                    color=color,
                    bottom=bottom,
                    label=col,
                )
                if df_share.loc[index, col] > 0.001:
                    plt.text(
                        index,
                        bottom + df.loc[index, col] / 2,
                        "{:,.0f}".format(df.loc[index, col])
                        + "("
                        + "{:.1%}".format(df_share.loc[index, col])
                        + ")",
                        color="white",
                        va="center",
                        ha="center",
                        fontsize=12,
                    )
                bottom += df.loc[index, col]

        hindex = 1.03
        plt.bar(
            df.index,
            df.sum(axis=1) * hindex,
            width=0.6,
            linewidth=1,
            linestyle="--",
            facecolor=(1, 0, 0, 0.0),
            edgecolor=(0, 0, 0, 1),
        )
        for index in df.index:
            plt.text(
                index,
                df.loc[index, :].sum() * (hindex + 0.02),
                "{:,.0f}".format(df.loc[index, :].sum()),
                ha="center",
                fontsize=14,
            )

        bottom1 = 0
        bottom2 = 0
        bottom3 = 0
        bottom4 = 0
        bbox_props = None
        for i, column in enumerate(df_gr):
            if math.isnan(df_gr.iloc[1, i]) is False:
                ax.annotate(
                    "{:+.1%}".format(df_gr.iloc[1, i]),
                    xy=(
                        0.5,
                        (bottom1 + bottom2 + df.iloc[0, i] / 2 + df.iloc[1, i] / 2) / 2,
                    ),
                    ha="center",
                    va="center",
                    color=color_dict[column],
                    fontsize=14,
                    bbox=bbox_props,
                )
            if math.isnan(df_gr.iloc[2, i]) is False:
                ax.annotate(
                    "{:+.1%}".format(df_gr.iloc[2, i]),
                    xy=(
                        1.5,
                        (bottom2 + bottom3 + df.iloc[1, i] / 2 + df.iloc[2, i] / 2) / 2,
                    ),
                    ha="center",
                    va="center",
                    color=color_dict[column],
                    fontsize=14,
                    bbox=bbox_props,
                )
            if math.isnan(df_gr.iloc[3, i]) is False:
                ax.annotate(
                    "{:+.1%}".format(df_gr.iloc[3, i]),
                    xy=(
                        2.5,
                        (bottom3 + bottom4 + df.iloc[2, i] / 2 + df.iloc[3, i] / 2) / 2,
                    ),
                    ha="center",
                    va="center",
                    color=color_dict[column],
                    fontsize=14,
                    bbox=bbox_props,
                )
            bottom1 += df.iloc[0, i]
            bottom2 += df.iloc[1, i]
            bottom3 += df.iloc[2, i]
            bottom4 += df.iloc[3, i]

        gr1 = df.iloc[1, :].sum() / df.iloc[0, :].sum() - 1
        gr2 = df.iloc[2, :].sum() / df.iloc[1, :].sum() - 1
        gr3 = df.iloc[3, :].sum() / df.iloc[2, :].sum() - 1
        ax.annotate(
            "{:+.1%}".format(gr1),
            xy=(0.5, (df.iloc[0, :].sum() + df.iloc[1, :].sum()) / 2 * (hindex + 0.02)),
            ha="center",
            va="center",
            color="black",
            fontsize=14,
            bbox=bbox_props,
        )
        ax.annotate(
            "{:+.1%}".format(gr2),
            xy=(1.5, (df.iloc[1, :].sum() + df.iloc[2, :].sum()) / 2 * (hindex + 0.02)),
            ha="center",
            va="center",
            color="black",
            fontsize=14,
            bbox=bbox_props,
        )
        ax.annotate(
            "{:+.1%}".format(gr3),
            xy=(2.5, (df.iloc[2, :].sum() + df.iloc[3, :].sum()) / 2 * (hindex + 0.02)),
            ha="center",
            va="center",
            color="black",
            fontsize=14,
            bbox=bbox_props,
        )

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(
            zip(
                labels[::-1],
                handles[::-1],
            )
        )  # 和下放调用.values()/.keys()配合去除重复的图例，顺便倒序让图例与图表保持一致
        ax.legend(
            by_label.values(),
            by_label.keys(),
            loc="center left",
            ncol=1,
            bbox_to_anchor=(1, 0.5),
            labelspacing=1,
            frameon=False,
            prop={"family": "SimHei", "size": 12},
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.title(title, fontproperties=myfont, fontsize=18)
        plt.ylabel(ytitle + unit_label, fontproperties=myfont)

        # Save
        plt.savefig(
            "./plots/" + title + ".png",
            format="png",
            transparent=True,
            bbox_inches="tight",
            dpi=600,
        )

        # Close
        plt.clf()
        plt.cla()
        plt.close()

    def agg_table(self, index, dimension, column, unit="Value", period="MAT"):
        affix = d_rename[period] + d_rename[unit]
        df = self.matrix_by_group(
            index=index,
            dimension=dimension,
            date=[self.latest_date()],
            period=period,
            unit=unit,
        )
        df.sort_values(by=self.name + affix, ascending=False, inplace=True)  # 按当前销售规模排序

        df_new = pd.DataFrame()
        df_new[self.name + affix] = df[self.name + affix]
        df_new[column + affix] = df[column + affix]
        df_new[column + "份额"] = df[column + affix] / df[self.name + affix]
        df_new[column + "份额变化"] = (df[column + affix] / df[self.name + affix]) - (
            (df[column + affix] - df[column + affix + "净增长"])
            / (df[self.name + affix] - df[self.name + affix + "净增长"])
        )
        for suffix in ["净增长", "增长率", "EI"]:
            df_new[column + affix + suffix] = df[column + affix + suffix]
        return df_new

    def plot_overall_performance(
        self,
        dimension,
        cycle="Annual",
        column=None,
        filter=None,
        filter_value=None,
        unit="Value",
        period="MAT",
        yunit="M",
        sorter=None,
        width=14,
        height=6,
    ):
        df = self.matrix_by_timeseries(
            filter=filter,
            filter_value=filter_value,
            index=None,
            dimension=dimension,
            return_type="绝对值",
            has_total=False,
            unit=unit,
            period=period,
        )
        df_share = self.matrix_by_timeseries(
            filter=filter,
            filter_value=filter_value,
            index=None,
            dimension=dimension,
            return_type="份额",
            has_total=False,
            unit=unit,
            period=period,
        )
        df_gr = self.matrix_by_timeseries(
            filter=filter,
            filter_value=filter_value,
            index=None,
            dimension=dimension,
            return_type="增长率",
            has_total=False,
            unit=unit,
            period=period,
        )

        suffix = ""
        df.to_excel(f"data_anemia_{unit}.xlsx")
        if cycle == "Annual":
            df = df.iloc[[-13, -9, -5, -1], :]
            df_share = df_share.iloc[[-13, -9, -5, -1], :]
            df_gr = df_gr.iloc[[-13, -9, -5, -1], :]
            suffix = "年度趋势"
        elif cycle == "Quarterly":
            # df = df.iloc[-13:, :]
            # df_share = df_share.iloc[-13:, :]
            # df_gr = df_gr.iloc[-13:, :]
            suffix = "季度趋势"

        if sorter is not None:
            df = df.reindex(sorter, axis=1)
            df_share = df_share.reindex(sorter, axis=1)
            df_gr = df_gr.reindex(sorter, axis=1)
        else:
            df.sort_values(axis=1, by=df.index[-1], ascending=False, inplace=True)
            df_share = df_share.reindex(df.columns, axis=1)
            df_gr = df_gr.reindex(df.columns, axis=1)

        title = self.name + "分" + d_rename[dimension] + d_rename[unit] + suffix
        ytitle = d_rename[unit]
        if cycle == "Annual":
            self.plot_stackedbar_plus(
                df=df,
                df_share=df_share,
                df_gr=df_gr,
                column=column,
                title=title,
                ytitle=ytitle,
                yunit=yunit,
                width=width,
                height=height,
            )
        else:
            self.plot_stackedbar(
                df=df,
                df_share=df_share,
                column=column,
                title=title,
                ytitle=ytitle,
                yunit=yunit,
                width=width,
                height=height,
            )

    def plot_map(self, dimension, column, unit="Value", period="MAT"):

        d_latlon = {
            "海门": [121.15, 31.89],
            "鄂尔多斯": [109.781327, 39.608266],
            "招远": [120.38, 37.35],
            "舟山": [122.207216, 29.985295],
            "齐齐哈尔": [123.97, 47.33],
            "盐城": [120.13, 33.38],
            "赤峰": [118.87, 42.28],
            "青岛": [120.33, 36.07],
            "乳山": [121.52, 36.89],
            "金昌": [102.188043, 38.520089],
            "泉州": [118.58, 24.93],
            "莱西": [120.53, 36.86],
            "日照": [119.46, 35.42],
            "胶南": [119.97, 35.88],
            "南通": [121.05, 32.08],
            "拉萨": [91.11, 29.97],
            "云浮": [112.02, 22.93],
            "梅州": [116.1, 24.55],
            "文登": [122.05, 37.2],
            "上海": [121.48, 31.22],
            "攀枝花": [101.718637, 26.582347],
            "威海": [122.1, 37.5],
            "承德": [117.93, 40.97],
            "厦门": [118.1, 24.46],
            "汕尾": [115.375279, 22.786211],
            "潮州": [116.63, 23.68],
            "丹东": [124.37, 40.13],
            "太仓": [121.1, 31.45],
            "曲靖": [103.79, 25.51],
            "烟台": [121.39, 37.52],
            "福州": [119.3, 26.08],
            "瓦房店": [121.979603, 39.627114],
            "即墨": [120.45, 36.38],
            "抚顺": [123.97, 41.97],
            "玉溪": [102.52, 24.35],
            "张家口": [114.87, 40.82],
            "阳泉": [113.57, 37.85],
            "莱州": [119.942327, 37.177017],
            "湖州": [120.1, 30.86],
            "汕头": [116.69, 23.39],
            "昆山": [120.95, 31.39],
            "宁波": [121.56, 29.86],
            "湛江": [110.359377, 21.270708],
            "揭阳": [116.35, 23.55],
            "荣成": [122.41, 37.16],
            "连云港": [119.16, 34.59],
            "葫芦岛": [120.836932, 40.711052],
            "常熟": [120.74, 31.64],
            "东莞": [113.75, 23.04],
            "河源": [114.68, 23.73],
            "淮安": [119.15, 33.5],
            "泰州": [119.9, 32.49],
            "南宁": [108.33, 22.84],
            "营口": [122.18, 40.65],
            "惠州": [114.4, 23.09],
            "江阴": [120.26, 31.91],
            "蓬莱": [120.75, 37.8],
            "韶关": [113.62, 24.84],
            "嘉峪关": [98.289152, 39.77313],
            "广州": [113.23, 23.16],
            "延安": [109.47, 36.6],
            "太原": [112.53, 37.87],
            "清远": [113.01, 23.7],
            "中山": [113.38, 22.52],
            "昆明": [102.73, 25.04],
            "寿光": [118.73, 36.86],
            "盘锦": [122.070714, 41.119997],
            "长治": [113.08, 36.18],
            "深圳": [114.07, 22.62],
            "珠海": [113.52, 22.3],
            "宿迁": [118.3, 33.96],
            "咸阳": [108.72, 34.36],
            "铜川": [109.11, 35.09],
            "平度": [119.97, 36.77],
            "佛山": [113.11, 23.05],
            "海口": [110.35, 20.02],
            "江门": [113.06, 22.61],
            "章丘": [117.53, 36.72],
            "肇庆": [112.44, 23.05],
            "大连": [121.62, 38.92],
            "临汾": [111.5, 36.08],
            "吴江": [120.63, 31.16],
            "石嘴山": [106.39, 39.04],
            "沈阳": [123.38, 41.8],
            "苏州": [120.62, 31.32],
            "茂名": [110.88, 21.68],
            "嘉兴": [120.76, 30.77],
            "长春": [125.35, 43.88],
            "胶州": [120.03336, 36.264622],
            "银川": [106.27, 38.47],
            "张家港": [120.555821, 31.875428],
            "三门峡": [111.19, 34.76],
            "锦州": [121.15, 41.13],
            "南昌": [115.89, 28.68],
            "柳州": [109.4, 24.33],
            "三亚": [109.511909, 18.252847],
            "自贡": [104.778442, 29.33903],
            "吉林": [126.57, 43.87],
            "阳江": [111.95, 21.85],
            "泸州": [105.39, 28.91],
            "西宁": [101.74, 36.56],
            "宜宾": [104.56, 29.77],
            "呼和浩特": [111.65, 40.82],
            "成都": [104.06, 30.67],
            "大同": [113.3, 40.12],
            "镇江": [119.44, 32.2],
            "桂林": [110.28, 25.29],
            "张家界": [110.479191, 29.117096],
            "宜兴": [119.82, 31.36],
            "北海": [109.12, 21.49],
            "西安": [108.95, 34.27],
            "金坛": [119.56, 31.74],
            "东营": [118.49, 37.46],
            "牡丹江": [129.58, 44.6],
            "遵义": [106.9, 27.7],
            "绍兴": [120.58, 30.01],
            "扬州": [119.42, 32.39],
            "常州": [119.95, 31.79],
            "潍坊": [119.1, 36.62],
            "重庆": [106.54, 29.59],
            "台州": [121.420757, 28.656386],
            "南京": [118.78, 32.04],
            "滨州": [118.03, 37.36],
            "贵阳": [106.71, 26.57],
            "无锡": [120.29, 31.59],
            "本溪": [123.73, 41.3],
            "克拉玛依": [84.77, 45.59],
            "渭南": [109.5, 34.52],
            "马鞍山": [118.48, 31.56],
            "宝鸡": [107.15, 34.38],
            "焦作": [113.21, 35.24],
            "句容": [119.16, 31.95],
            "北京": [116.46, 39.92],
            "徐州": [117.2, 34.26],
            "衡水": [115.72, 37.72],
            "包头": [110, 40.58],
            "绵阳": [104.73, 31.48],
            "乌鲁木齐": [87.68, 43.77],
            "枣庄": [117.57, 34.86],
            "杭州": [120.19, 30.26],
            "淄博": [118.05, 36.78],
            "鞍山": [122.85, 41.12],
            "溧阳": [119.48, 31.43],
            "库尔勒": [86.06, 41.68],
            "安阳": [114.35, 36.1],
            "开封": [114.35, 34.79],
            "济南": [117, 36.65],
            "德阳": [104.37, 31.13],
            "温州": [120.65, 28.01],
            "九江": [115.97, 29.71],
            "邯郸": [114.47, 36.6],
            "临安": [119.72, 30.23],
            "兰州": [103.73, 36.03],
            "沧州": [116.83, 38.33],
            "临沂": [118.35, 35.05],
            "南充": [106.110698, 30.837793],
            "天津": [117.2, 39.13],
            "富阳": [119.95, 30.07],
            "泰安": [117.13, 36.18],
            "诸暨": [120.23, 29.71],
            "郑州": [113.65, 34.76],
            "哈尔滨": [126.63, 45.75],
            "聊城": [115.97, 36.45],
            "芜湖": [118.38, 31.33],
            "唐山": [118.02, 39.63],
            "平顶山": [113.29, 33.75],
            "邢台": [114.48, 37.05],
            "德州": [116.29, 37.45],
            "济宁": [116.59, 35.38],
            "荆州": [112.239741, 30.335165],
            "宜昌": [111.3, 30.7],
            "义乌": [120.06, 29.32],
            "丽水": [119.92, 28.45],
            "洛阳": [112.44, 34.7],
            "秦皇岛": [119.57, 39.95],
            "株洲": [113.16, 27.83],
            "石家庄": [114.48, 38.03],
            "莱芜": [117.67, 36.19],
            "常德": [111.69, 29.05],
            "保定": [115.48, 38.85],
            "湘潭": [112.91, 27.87],
            "金华": [119.64, 29.12],
            "岳阳": [113.09, 29.37],
            "长沙": [113, 28.21],
            "衢州": [118.88, 28.97],
            "廊坊": [116.7, 39.53],
            "菏泽": [115.480656, 35.23375],
            "合肥": [117.27, 31.86],
            "武汉": [114.31, 30.52],
            "大庆": [125.03, 46.58],
        }
        affix = d_rename[period] + d_rename[unit]
        df = self.matrix_by_group(
            index="CITY", dimension="PRODUCT", date=[self.latest_date()]
        )
        df = df[column + affix] / df[self.name + affix]
        df.index = df.index + "市"
        s = pd.Series(
            [
                df.loc["福厦泉市"],
                df.loc["福厦泉市"],
                df.loc["福厦泉市"],
                df.loc["珠三角市"],
                df.loc["珠三角市"],
                df.loc["珠三角市"],
            ],
            index=["福州市", "厦门市", "泉州市", "佛山市", "东莞市", "中山市"],
        )

        df = df.append(s)

        fig, ax = plt.subplots(figsize=(9, 8))
        plt.title("title", fontproperties=myfont, fontsize=16, y=0.9)
        m = Basemap(
            llcrnrlon=77,
            llcrnrlat=14,
            urcrnrlon=140,
            urcrnrlat=51,
            projection="lcc",
            lat_1=33,
            lat_2=45,
            lon_0=100,
        )
        m.readshapefile("CHN_adm_shp/CHN_adm1", "states", drawbounds=True)
        m.readshapefile("CHN_adm_shp/CHN_adm2", "counties", drawbounds=False)
        m.readshapefile("TWN_adm_shp/TWN_adm0", "taiwan", drawbounds=True)  # 增加台湾

        countynames = []
        for shapedict in m.counties_info:
            countyname = shapedict["NL_NAME_2"]
            p = countyname.split("|")
            if len(p) > 1:
                s = p[1]
            else:
                s = p[0]
            # 直辖市命名问题
            if s in ["北京", "上海", "天津", "重庆"]:
                s = s + "市"
            # 撤并的县市
            if s == "巢湖市":
                s = "合肥市"
            if s == "天门市":
                s = "武汉市"
            if s == "潜江市":
                s = "武汉市"
            if s == "仙桃市":
                s = "武汉市"
            if s == "济源市":
                s = "焦作市"
            # 部分省直辖区域无法归类，归于最近的城市
            if s == "海南":
                s = "海口市"
            if s == "神农架林区":
                s = "恩施土家族苗族自治州"
            # 繁体字导致的错误
            if s == "益陽市":
                s = "益阳市"
            if s == "邵陽市":
                s = "邵阳市"
            if s == "衡陽市":
                s = "衡阳市"
            if s == "岳陽市":
                s = "岳阳市"
            if s == "張家界市":
                s = "张家界市"
            if s == "長沙市":
                s = "长沙市"
            if s == "懷化市":
                s = "怀化市"
            if s == "婁底市":
                s = "娄底市"
            # 撤县并市
            if s == "运城县":
                s = "运城市"
            # 用字不同
            if s == "巴音郭愣蒙古自治州":
                s = "巴彦卓尔蒙古自治州"
            # 少'市'字
            if s == "滨州":
                s = "滨州市"
            countynames.append(s)
        countynames_nodup = list(set(countynames))  # 去除重复

        df = df.reindex(countynames_nodup)

        if df.min() < 0:
            colors = {}
            cmap1 = LinearSegmentedColormap.from_list(
                "mycmap", ["red", "white"]
            )  # 定义负值colormap,红白渐变
            vmax1 = 0
            vmin1 = df.min()
            norm1 = mpl.colors.Normalize(vmin=vmin1, vmax=vmax1)
            cmap2 = LinearSegmentedColormap.from_list(
                "mycmap", ["white", "green"]
            )  # 定义正值colormap,白绿渐变
            vmax2 = df.max()
            vmin2 = 0
            norm2 = mpl.colors.Normalize(vmin=vmin2, vmax=vmax2)

            # 每个值根据正负和正态分布中的给定颜色
            for index, value in df.iteritems():
                if value < 0:
                    colors[index] = cmap1(np.sqrt((value - vmin1) / (vmax1 - vmin1)))[
                        :3
                    ]
                else:
                    colors[index] = cmap2(np.sqrt((value - vmin2) / (vmax2 - vmin2)))[
                        :3
                    ]

            # 生产渐变色legend colorbar
            cax1 = fig.add_axes([0.18, 0.15, 0.36, 0.01])
            cax2 = fig.add_axes([0.54, 0.15, 0.36, 0.01])
            fmt = FuncFormatter(lambda y, _: "{:.0%}".format(y))
            cb1 = mpl.colorbar.ColorbarBase(
                cax1,
                cmap=cmap1,
                norm=norm1,
                spacing="proportional",
                orientation="horizontal",
                format=fmt,
            )
            cb2 = mpl.colorbar.ColorbarBase(
                cax2,
                cmap=cmap2,
                norm=norm2,
                spacing="proportional",
                orientation="horizontal",
                format=fmt,
            )
            # cb1.set_label('label', x=1, fontproperties=myfont, fontsize=10)
            # cb2.set_label('（%）', x=1, fontproperties=myfont, fontsize=10)
            cb1.ax.tick_params(labelsize=10)
            cb2.ax.tick_params(labelsize=10)
        else:
            colors = {}
            cmap = LinearSegmentedColormap.from_list(
                "mycmap", ["white", "orange", "green"]
            )  # 定义正值colormap,白绿渐变
            vmax = df.max()
            vmin = df.min()
            norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

            # 每个值根据正负和正态分布中的给定颜色
            for index, value in df.iteritems():
                colors[index] = cmap(np.sqrt((value - vmin) / (vmax - vmin)))[:3]

            # 生产渐变色legend colorbar
            cax = fig.add_axes([0.18, 0.15, 0.72, 0.01])
            fmt = FuncFormatter(lambda y, _: "{:.0%}".format(y))
            cb = mpl.colorbar.ColorbarBase(
                cax,
                cmap=cmap,
                norm=norm,
                spacing="proportional",
                orientation="horizontal",
                format=fmt,
            )
            # cb.set_label('（%）', x=1, fontproperties=myfont, fontsize=10)
            cb.ax.tick_params(labelsize=10)
            cb.ax.tick_params(labelsize=10)

        # 每个区域绘图
        for nshape, seg in enumerate(m.counties):
            facecolor = "white"
            edgecolor = "white"
            if np.isnan(df[countynames[nshape]]) == False:
                facecolor = rgb2hex(colors[countynames[nshape]])
                edgecolor = facecolor
            #     # x, y = np.array(seg).mean(axis=0)
            #     # plt.text(x, y, '{:.1%}'.format(df[countynames[nshape]]), ha="center", fontsize=10)
            #     edgecolor='black'
            poly = Polygon(seg, facecolor=facecolor, edgecolor=facecolor)
            ax.add_patch(poly)

        # 去除图片边框re
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)

        # 保存图片，去掉边缘白色区域，透明
        plt.savefig(
            "./plots/" + "title" + ".png",
            format="png",
            bbox_inches="tight",
            transparent=True,
            dpi=600,
        )
        print("title" + " finished plot")

        return df

    def plot_share_gr_trend(
        self,
        dimension,
        column,
        filter=None,
        filter_value=None,
        unit="Value",
        period="MAT",
        yfmt1="{:.1%}",
        yfmt2="{:+.1%}",
        ylim1=None,
        ylim2=None,
        series_limit=10,
    ):
        affix = d_rename[period] + d_rename[unit]
        df_share = self.matrix_by_timeseries(
            filter=filter,
            filter_value=filter_value,
            index=None,
            dimension=dimension,
            return_type="份额",
            has_total=False,
            unit=unit,
            period=period,
        )
        df_gr = self.matrix_by_timeseries(
            filter=filter,
            filter_value=filter_value,
            index=None,
            dimension=dimension,
            return_type="增长率",
            has_total=False,
            unit=unit,
            period=period,
        )
        df_share.sort_values(
            by=df_share.index[-1], axis=1, ascending=False, inplace=True
        )
        if df_share.shape[1] > series_limit:
            set_limit = True
            df_share2 = df_share.iloc[:, :series_limit]
            if column is not None:
                found = df_share2.columns.str.contains(column)
                if sum(found) == 0:
                    df_share2.loc[:, column] = df_share.loc[:, column]
        else:
            set_limit = False
            df_share2 = df_share
        df_gr2 = df_gr.loc[:, df_share2.columns]

        if set_limit is True:
            title = self.name + "Top" + d_rename[dimension] + affix + "份额和增长率趋势"
        else:
            title = self.name + "各" + d_rename[dimension] + affix + "份额和增长率趋势"
        xtitle1 = affix + "份额趋势"
        xtitle2 = affix + "增长率趋势"
        ytitle = ""
        print(df_share2, df_gr2)
        self.plot_line_twin(
            df1=df_share2,
            df2=df_gr2,
            column=column,
            title=title,
            xtitle1=xtitle1,
            xtitle2=xtitle2,
            ytitle=ytitle,
            yfmt1=yfmt1,
            yfmt2=yfmt2,
            ylim1=ylim1,
            ylim2=ylim2,
        )

        return df_share, df_gr

    def plot_share_trend(
        self,
        dimension,
        column,
        filter=None,
        filter_value=None,
        unit="Value",
        period="MAT",
        yfmt="{:.1%}",
        ylim=None,
        series_limit=10,
        show_list=None,
        ignore_list=None,
    ):
        affix = d_rename[period] + d_rename[unit]
        df_share = self.matrix_by_timeseries(
            filter=filter,
            filter_value=filter_value,
            index=None,
            dimension=dimension,
            return_type="份额",
            has_total=False,
            unit=unit,
            period=period,
        )

        df_share.sort_values(
            by=df_share.index[-1], axis=1, ascending=False, inplace=True
        )

        if show_list is not None:
            df_share = df_share.loc[:, show_list]
        else:
            if ignore_list is not None:
                for ele in ignore_list:
                    try:
                        df_share.drop(ele, axis=1, inplace=True)
                    except KeyError:
                        continue

        if df_share.shape[1] > series_limit:
            set_limit = True
            df_share2 = df_share.iloc[:, :series_limit]
            if column is not None:
                found = df_share2.columns.str.contains(column)
                if sum(found) == 0:
                    df_share2.loc[:, column] = df_share.loc[:, column]
        else:
            set_limit = False
            df_share2 = df_share

        df_share2.sort_values(
            by=df_share2.index[-1], axis=1, ascending=False, inplace=True
        )

        if set_limit is True or show_list is not None:
            title = self.name + "Top" + d_rename[dimension] + affix + "份额趋势"
        else:
            title = self.name + "各" + d_rename[dimension] + affix + "份额趋势"
        ytitle = ""
        print(df_share2)
        self.plot_line(
            df=df_share2,
            column=column,
            title=title,
            ytitle=ytitle,
            yfmt=yfmt,
            ylim=ylim,
        )

        return df_share

    def plot_grid_share_trend(
        self,
        grid_index,
        dimension,
        column,
        filter=None,
        filter_value=None,
        unit="Value",
        period="MAT",
        sort_method="Value",
        sorter=None,
        ignore_list=None,
    ):
        affix = d_rename[period] + d_rename[unit]
        df = self.matrix_by_timeseries(
            filter=filter,
            filter_value=filter_value,
            index=grid_index,
            dimension=dimension,
            return_type="份额",
            has_total=False,
            unit=unit,
            period=period,
        )

        df_index = self.matrix_by_group(
            grid_index, dimension, [self.latest_date()], unit, period
        )
        if sort_method == "Value":
            df_index.sort_values(by=self.name + affix, ascending=False, inplace=True)
        elif sort_method == "Index":
            df_index.sort_index(inplace=True)
        elif sort_method == "List":
            df_index = df_index.reindex(sorter)

        if ignore_list is not None:
            for ele in ignore_list:
                try:
                    df.drop(ele, axis=1, inplace=True)
                except KeyError:
                    continue

        index_list = df_index.index.tolist()
        title = "各" + d_rename[grid_index] + d_rename[dimension] + affix + "份额趋势"
        xtitle = ""
        ytitle = d_rename[unit] + "份额"
        self.plot_line_grid(
            df=df,
            index=grid_index,
            index_list=index_list,
            column=column,
            title=title,
            xtitle=xtitle,
            ytitle=ytitle,
            ylim=[0, df.iloc[:, 1:].max().max()],
        )

    def plot_group_size_share(
        self,
        index,
        date,
        dimension,
        column,
        unit="Value",
        period="MAT",
        xlim=None,
        ylim=None,
        adjust_scale=1.0,
        series_limit=10,
        showLabel=True,
        labelLimit=15,
    ):
        affix = d_rename[period] + d_rename[unit]
        df = self.matrix_by_group(index, dimension, date, unit, period)

        df.fillna(0, inplace=True)
        x = df[self.name + affix]
        y = df[column + affix] / df[self.name + affix]
        z = df[column + affix] / 5000 * adjust_scale
        labels = x.index

        title = "各" + d_rename[index] + self.name + "潜力 versus " + column + "份额"
        self.plot_bubble(
            x=x,
            y=y,
            z=z,
            labels=labels,
            title=title,
            xtitle=self.name + affix,
            ytitle=column + affix + "份额",
            xunit="M",
            xfmt="{:.0f}",
            yunit="%",
            yfmt="{:.1%}",
            xlim=xlim,
            ylim=ylim,
            showLabel=showLabel,
            labelLimit=labelLimit,
        )

    def plot_group_share_gr(
        self,
        index,
        date,
        dimension,
        column,
        unit="Value",
        period="MAT",
        xlim=None,
        ylim=None,
        adjust_scale=1.0,
        series_limit=10,
        showLabel=True,
        labelLimit=15,
    ):
        affix = d_rename[period] + d_rename[unit]
        df = self.matrix_by_group(index, dimension, date, unit, period)

        df.fillna(0, inplace=True)
        df.sort_values(by=self.name + affix, ascending=False, inplace=True)
        if df.shape[0] > series_limit:
            set_limit = True
            df2 = df.iloc[:series_limit, :]
            if column is not None:
                found = df2.index.str.contains(column)
                if sum(found) == 0:
                    df2 = df2.append(df.loc[column, :])
        else:
            set_limit = False
            df2 = df

        # 计算平均增长率
        yavg = df2[self.name + affix + "净增长"].sum() / df2[self.name + affix].sum()

        x = df2[self.name + affix] / df2[self.name + affix].sum()
        y = df2[self.name + affix + "增长率"]
        z = df2[self.name + affix] / 5000 * adjust_scale
        labels = x.index

        if set_limit is True:
            title = (
                self.name
                + "Top"
                + str(series_limit)
                + d_rename[index]
                + affix
                + "份额 versus 增长率"
            )
        else:
            title = self.name + "各" + d_rename[index] + affix + "份额 versus 增长率"
        self.plot_bubble(
            x=x,
            y=y,
            z=z,
            labels=labels,
            title=title,
            xtitle=self.name + affix,
            ytitle=affix,
            xunit="%",
            xfmt="{:.1%}",
            yunit="+%",
            yfmt="{:+.1%}",
            xlim=xlim,
            ylim=ylim,
            showLabel=showLabel,
            labelLimit=labelLimit,
            yavgline=True,
            yavg=yavg,
        )

    def plot_group_size_diff(
        self,
        index,
        date,
        dimension,
        column,
        unit="Value",
        period="MAT",
        xlim=None,
        ylim=None,
        adjust_scale=1.0,
        series_limit=10,
        showLabel=True,
        labelLimit=15,
    ):
        affix = d_rename[period] + d_rename[unit]
        df = self.matrix_by_group(index, dimension, date, unit, period)

        df.fillna(0, inplace=True)
        df.sort_values(by=self.name + affix, ascending=False, inplace=True)
        if df.shape[0] > series_limit:
            set_limit = True
            df2 = df.iloc[:series_limit, :]
            if column is not None:
                found = df2.index.str.contains(column)
                if sum(found) == 0:
                    df2 = df2.append(df.loc[column, :])
        else:
            set_limit = False
            df2 = df

        x = df2[self.name + affix]
        y = df2[self.name + affix + "净增长"]
        z = df2[self.name + affix] / 5000 * adjust_scale
        labels = x.index

        if set_limit is True:
            title = (
                self.name
                + "Top"
                + str(series_limit)
                + d_rename[index]
                + affix
                + "绝对值 versus 净增长"
            )
        else:
            title = self.name + "各" + d_rename[index] + affix + "绝对值 versus 净增长"
        self.plot_bubble(
            x=x,
            y=y,
            z=z,
            labels=labels,
            title=title,
            xtitle=self.name + affix,
            ytitle=affix + "净增长",
            xunit="M",
            xfmt="{:,.0f}",
            yunit="M",
            yfmt="{:,.0f}",
            xlim=xlim,
            ylim=ylim,
            showLabel=showLabel,
            labelLimit=labelLimit,
            yavgline=True,
            yavg=0,
        )

    def plot_group_share(
        self,
        index,
        date,
        dimension,
        column,
        method,
        threshold=False,
        threshold_color="crimson",
        unit="Value",
        period="MAT",
        sort_method="Value",
        sorter=None,
    ):
        affix = d_rename[period] + d_rename[unit]
        df = self.matrix_by_group(index, dimension, date, unit, period)
        df = df.loc[:, df.columns.str.endswith(affix)]
        df.fillna(0, inplace=True)
        df.sort_values(by=self.name + affix, ascending=False, inplace=True)  # 按当前销售规模排序
        df.columns = df.columns.str[: -len(affix)]

        if sort_method == "Value":
            df.sort_values(
                by=df.first_valid_index(), axis=1, ascending=False, inplace=True
            )  # 按当前销售规模排序
        elif sort_method == "Index":
            df.sort_index(axis=1, inplace=True)
        elif sort_method == "List":
            sorter.insert(0, self.name)
            df = df.reindex(sorter, axis=1)

        if threshold is True and column is not None:
            avg = df[column].sum() / (df.sum(axis=1).sum() / 2)
        else:
            avg = None

        df_share = pd.DataFrame()
        for col in df.columns:
            if col != self.name:
                if method == "share":
                    df_share[col] = df[col].div(df[self.name], axis=0)
                    df[col] = df[col].div(df[self.name], axis=0)
                elif method == "abs":
                    df_share[col] = df[col].div(df[self.name], axis=0)
        df.drop(self.name, axis=1, inplace=True)

        title = "各" + d_rename[index] + self.name + d_rename[dimension] + "份额"
        if method == "share":
            self.plot_stackedbar(
                df=df,
                df_share=df_share,
                column=column,
                threshold=avg,
                threshold_color=threshold_color,
                title=title,
                xtitle="按" + self.name + "最新" + affix + "大小排序",
                ytitle=affix,
                yunit="%",
                yfmt="{:.1%}",
                show_grid=False,
            )
        elif method == "abs":
            self.plot_stackedbar(
                df=df,
                df_share=df_share,
                column=column,
                threshold=avg,
                threshold_color=threshold_color,
                title=title,
                xtitle="按" + self.name + "最新" + affix + "大小排序",
                ytitle=affix,
            )

    def plot_group_size_gr(
        self,
        index,
        date,
        dimension,
        column,
        comparison_method,
        unit="Value",
        period="MAT",
        y2lim=None,
    ):
        affix = d_rename[period] + d_rename[unit]

        df = self.matrix_by_group(index, dimension, date, unit, period)
        print(df)
        if dimension is None:
            title = self.name + affix + "分" + d_rename[index] + "表现"
            df = df.loc[
                :,
                [
                    self.name + affix,
                    self.name + affix + "净增长",
                    self.name + affix + comparison_method,
                ],
            ]
            df[self.name + "上年" + d_rename[unit]] = (
                df[self.name + affix] - df[self.name + affix + "净增长"]
            )
            df.sort_values(
                by=self.name + affix, ascending=False, inplace=True
            )  # 按当前销售规模排序
            avg_comparison_label = "平均" + comparison_method + ":"
            avg_comparison_value = (
                df[self.name + affix].sum()
                / df[self.name + "上年" + d_rename[unit]].sum()
                - 1
            )
            self.plot_stackedbar_line(
                df_bar=df[
                    [self.name + "上年" + d_rename[unit], self.name + affix + "净增长"]
                ],
                df_line=df[self.name + affix + comparison_method],
                hline_label=avg_comparison_label,
                hline_value=avg_comparison_value,
                title=title,
                xtitle="按" + self.name + "最新" + affix + "大小排序",
                y1title=affix,
                y2title=affix + comparison_method,
                y2lim=y2lim,
            )
        else:
            title = column + affix + "分" + d_rename[index] + "表现"
            df = df.loc[
                :,
                [
                    self.name + affix,
                    self.name + affix + "净增长",
                    self.name + affix + comparison_method,
                    column + affix,
                    column + affix + "净增长",
                    column + affix + comparison_method,
                ],
            ]
            df[self.name + "上年" + d_rename[unit]] = (
                df[self.name + affix] - df[self.name + affix + "净增长"]
            )
            df[column + "上年" + d_rename[unit]] = (
                df[column + affix] - df[column + affix + "净增长"]
            )
            df.sort_values(
                by=column + affix, ascending=False, inplace=True
            )  # 按当前销售规模排序
            avg_comparison_label = "平均" + comparison_method + ":"
            if comparison_method == "增长率":
                avg_comparison_value = (
                    df[column + affix].sum() / df[column + "上年" + d_rename[unit]].sum()
                    - 1
                )
                y2fmt = "{:+.1%}"
            elif comparison_method == "EI":
                avg_comparison_value = (
                    (
                        df[column + affix].sum()
                        / df[column + "上年" + d_rename[unit]].sum()
                    )
                    / (
                        df[self.name + affix].sum()
                        / df[self.name + "上年" + d_rename[unit]].sum()
                    )
                    * 100
                )
                y2fmt = "{:,.0f}"
            else:
                avg_comparison_value = 0
                y2fmt = "{:,.0f}"

            self.plot_stackedbar_line(
                df_bar=df[[column + "上年" + d_rename[unit], column + affix + "净增长"]],
                df_line=df[column + affix + comparison_method],
                hline_label=avg_comparison_label,
                hline_value=avg_comparison_value,
                title=title,
                xtitle="按" + self.name + "最新" + affix + "大小排序",
                y1title=affix,
                y2title=affix + comparison_method,
                y2fmt=y2fmt,
                y2lim=y2lim,
            )

        return df


def rand_cmap(
    nlabels, type="bright", first_color_black=True, last_color_black=False, verbose=True
):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np

    if type not in ("bright", "soft"):
        print('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print("Number of labels: " + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == "bright":
        randHSVcolors = [
            (
                np.random.uniform(low=0.0, high=1),
                np.random.uniform(low=0.2, high=1),
                np.random.uniform(low=0.9, high=1),
            )
            for i in range(nlabels)
        ]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(
                colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2])
            )

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list(
            "new_map", randRGBcolors, N=nlabels
        )

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == "soft":
        low = 0.6
        high = 0.95
        randRGBcolors = [
            (
                np.random.uniform(low=low, high=high),
                np.random.uniform(low=low, high=high),
                np.random.uniform(low=low, high=high),
            )
            for i in range(nlabels)
        ]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list(
            "new_map", randRGBcolors, N=nlabels
        )

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt

        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(
            ax,
            cmap=random_colormap,
            norm=norm,
            spacing="proportional",
            ticks=None,
            boundaries=bounds,
            format="%1i",
            orientation="horizontal",
        )

    return random_colormap


def convert_std_volume(df, dimension, target, strength, ratio):
    column_unit = "UNIT"
    column_strength = "STRENGTH"
    unit_std_volume = "Volume (Std Counting Unit)"
    column_value = "AMOUNT"
    mask = (
        (df[dimension] == target)
        & (df[column_strength] == strength)
        & (df[column_unit] == unit_std_volume)
    )
    df.loc[mask, column_value] = (df.loc[mask, column_value]) * ratio
