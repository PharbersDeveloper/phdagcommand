def mapping():
    return [
        {
            "col_name": "COMPANY",
            "col_desc": "数据公司",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "SOURCE",
            "col_desc": "数据来源",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "TAG",
            "col_desc": "文件标识",
            "candidate": ['_TAG'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PROVINCE_NAME",
            "col_desc": "省份名",
            "candidate": ['省'],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "CITY_NAME",
            "col_desc": "城市名",
            "candidate": ['城市', 'CITY'],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "PREFECTURE_NAME",
            "col_desc": "区县名",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "YEAR",
            "col_desc": "年份",
            "candidate": ['年', 'YEAR'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "QUARTER",
            "col_desc": "季度",
            "candidate": ['季度'],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "MONTH",
            "col_desc": "月份",
            "candidate": ['月', 'MONTH'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "HOSP_NAME",
            "col_desc": "医院名",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "HOSP_CODE",
            "col_desc": "医院编码",
            "candidate": ['医院编码', 'HOSPITAL_CODE'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "HOSP_LEVEL",
            "col_desc": "医院等级",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "ATC",
            "col_desc": "ATC编码",
            "candidate": ['ATC编码'],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "MOLE_NAME",
            "col_desc": "分子名",
            "candidate": ['药品名称', 'MOLE_NAME'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PRODUCT_NAME",
            "col_desc": "商品名",
            "candidate": ['商品名', 'PRODUCT_NAME'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "SPEC",
            "col_desc": "规格",
            "candidate": ['规格', '原PACK_DES'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "DOSAGE",
            "col_desc": "剂型",
            "candidate": ['剂型', 'APP2_COD'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PACK_QTY",
            "col_desc": "包装数量",
            "candidate": ['包装数量', 'pack'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "SALES_QTY_GRAIN",
            "col_desc": "粒度销量",
            "candidate": ['数量（支/片）', 'STANDARD_UNIT'],
            "type": "Double",
            "not_null": True,
        },
        {
            "col_name": "SALES_QTY_BOX",
            "col_desc": "盒装销量",
            "candidate": [],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "SALES_QTY_TAG",
            "col_desc": r"销量标识(GRAIN \ BOX \ FULL)",
            "candidate": [],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "SALES_VALUE",
            "col_desc": "销售额",
            "candidate": ['金额（元）', 'VALUE'],
            "type": "Double",
            "not_null": True,
        },
        {
            "col_name": "DELIVERY_WAY",
            "col_desc": "给药途径",
            "candidate": ['途径', 'APP1_COD'],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "MANUFACTURER_NAME",
            "col_desc": "生产厂商",
            "candidate": ['生产企业', 'CORP_NAME'],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MKT",
            "col_desc": "所属市场",
            "candidate": ['PRODUCT_MKT'],
            "type": "String",
            "not_null": False,
        },
    ]
