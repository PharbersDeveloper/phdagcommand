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
            "candidate": ["省"],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "CITY_NAME",
            "col_desc": "城市名",
            "candidate": ["CITY", "城市"],
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
            "candidate": ["YEAR", "年"],
            "type": "Integer",
            "not_null": True,
        },
        {
            "col_name": "QUARTER",
            "col_desc": "季度",
            "candidate": ["季度"],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "MONTH",
            "col_desc": "月份",
            "candidate": ["MONTH", "月"],
            "type": "Integer",
            "not_null": True,
        },
        {
            "col_name": "HOSP_NAME",
            "col_desc": "医院名",
            "candidate": ["医院名称"],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "HOSP_CODE",
            "col_desc": "医院编码",
            "candidate": ["HOSPITAL_CODE", "医院编码"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "HOSP_LEVEL",
            "col_desc": "医院等级",
            "candidate": ["参考级别"],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "ATC",
            "col_desc": "ATC编码",
            "candidate": [],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "MOLE_NAME",
            "col_desc": "分子名",
            "candidate": ["MOLE_NAME"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PRODUCT_NAME",
            "col_desc": "商品名",
            "candidate": ["PRODUCT_NAME"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "SPEC",
            "col_desc": "规格",
            "candidate": ["PACK_DES", "原PACK_DES"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "DOSAGE",
            "col_desc": "剂型",
            "candidate": ["APP2_COD"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "PACK_QTY",
            "col_desc": "包装数量",
            "candidate": ["PACK_NUMBER", "pack"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "SALES_QTY_GRAIN",
            "col_desc": "粒度销量",
            "candidate": ["STANDARD_UNIT"],
            "type": "String",
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
            "candidate": ["VALUE", "金额（元）"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "DELIVERY_WAY",
            "col_desc": "给药途径",
            "candidate": ["给药途径"],
            "type": "String",
            "not_null": False,
        },
        {
            "col_name": "MANUFACTURER_NAME",
            "col_desc": "生产厂商",
            "candidate": ["CORP_NAME"],
            "type": "String",
            "not_null": True,
        },
        {
            "col_name": "MKT",
            "col_desc": "所属市场",
            "candidate": ["PRODUCT_MKT"],
            "type": "String",
            "not_null": False,
        },
    ]
