# phDagCommand/ph_data_clean
Python 实现的数据清洗，并根据 Source 和 Company 选择清洗算法和清洗结构，以此同源数据的 Schema 统一

## 测试方法
### linux or mac 测试方法
```androiddatabinding
python phcli clean '{"data": "{\"0#省\":\"安徽省\",\"1#城市\":\"蚌埠市\",\"2#年\":\"2019\",\"3#季度\":\"1\",\"4#月\":\"1\",\"5#医院编码\":\"230461\",\"6#ATC码\":\"B01AC04\",\"7#药品名称\":\"氯吡格雷\",\"8#商品名\":\"泰嘉\",\"9#包装\":\"H\",\"10#规格\":\"75 MG\",\"11#包装数量\":\"7.0\",\"12#金额（元）\":\"337848.0\",\"13#数量（支/片）\":\"39200.0\",\"14#剂型\":\"TAB\",\"15#途径\":\"OR\",\"16#生产企业\":\"深圳信立泰药业有限公司\",\"_tag\":\"phf\\u001Fauto robot\\u001F190313安进1901检索.xlsx\\u001F1月数据\\u001F1591669293056\"}","metadata": "{\"assetId\":\"5edef206fbfcbe3e147561f3\",\"tag\":\"phf\\u001Fauto robot\\u001F190313安进1901检索.xlsx\\u001F1月数据\\u001F1591669293056\",\"providers\":[\"Amgen\",\"CPA&GYC\"],\"geoCover\":[],\"dataCover\":[\"201901\"],\"label\":[\"原始数据\"],\"fileName\":\"190313安进1901检索.xlsx\",\"molecules\":[],\"markets\":[],\"sheetName\":\"1月数据\",\"length\":8568.0}"}'
```

### windows 测试方法
```androiddatabinding
python phcli clean {\"data\": \"{\\\"0#省\\\":\\\"安徽省\\\",\\\"1#城市\\\":\\\"蚌埠市\\\",\\\"2#年\\\":\\\"2019\\\",\\\"3#季度\\\":\\\"1\\\",\\\"4#月\\\":\\\"1\\\",\\\"5#医院编码\\\":\\\"230461\\\",\\\"6#ATC码\\\":\\\"B01AC04\\\",\\\"7#药品名称\\\":\\\"氯吡格雷\\\",\\\"8#商品名\\\":\\\"泰嘉\\\",\\\"9#包装\\\":\\\"H\\\",\\\"10#规格\\\":\\\"75 MG\\\",\\\"11#包装数量\\\":\\\"7.0\\\",\\\"12#金额（元）\\\":\\\"337848.0\\\",\\\"13#数量（支/片）\\\":\\\"39200.0\\\",\\\"14#剂型\\\":\\\"TAB\\\",\\\"15#途径\\\":\\\"OR\\\",\\\"16#生产企业\\\":\\\"深圳信立泰药业有限公司\\\",\\\"_tag\\\":\\\"phf\\\u001Fauto robot\\\u001F190313安进1901检索.xlsx\\\u001F1月数据\\\u001F1591669293056\\\"}\",\"metadata\": \"{\\\"assetId\\\":\\\"5edef206fbfcbe3e147561f3\\\",\\\"tag\\\":\\\"phf\\\u001Fauto robot\\\u001F190313安进1901检索.xlsx\\\u001F1月数据\\\u001F1591669293056\\\",\\\"providers\\\":[\\\"Amgen\\\",\\\"CPA&GYC\\\"],\\\"geoCover\\\":[],\\\"dataCover\\\":[\\\"201901\\\"],\\\"label\\\":[\\\"原始数据\\\"],\\\"fileName\\\":\\\"190313安进1901检索.xlsx\\\",\\\"molecules\\\":[],\\\"markets\\\":[],\\\"sheetName\\\":\\\"1月数据\\\",\\\"length\\\":8568.0}}
```

###python phcli clean 
```
{\"data\": {\\\"0#省\\\":\\\"安徽省\\\",\\\"1#城市\\\":\\\"蚌埠市\\\",\\\"2#年\\\":\\\"2019\\\",\\\"3#季度\\\":\\\"1\\\",\\\"4#月\\\":\\\"1\\\",\\\"5#医院编码\\\":\\\"230461\\\",\\\"6#ATC码\\\":\\\"B01AC04\\\",\\\"7#药品名称\\\":\\\"氯吡格雷\\\",\\\"8#商品名\\\":\\\"泰嘉\\\",\\\"9#包装\\\":\\\"H\\\",\\\"10#规格\\\":\\\"75 MG\\\",\\\"11#包装数量\\\":\\\"7.0\\\",\\\"12#金额（元）\\\":\\\"337848.0\\\",\\\"13#数量（支/片）\\\":\\\"39200.0\\\",\\\"14#剂型\\\":\\\"TAB\\\",\\\"15#途径\\\":\\\"OR\\\",\\\"16#生产企业\\\":\\\"深圳信立泰药业有限公司\\\",\\\"_tag\\\":\\\"phf\\\\u001Fauto robot\\\\u001F190313安进1901检索.xlsx\\\\u001F1月数据\\\\u001F1591669293056\\\"},\"metadata\": {\\\"assetId\\\":\\\"5edef206fbfcbe3e147561f3\\\",\\\"tag\\\":\\\"phf\\\\u001Fauto robot\\\\u001F190313安进1901检索.xlsx\\\\u001F1月数据\\\\u001F1591669293056\\\",\\\"providers\\\":[\\\"Amgen\\\",\\\"CPA&GYC\\\"],\\\"geoCover\\\":[],\\\"dataCover\\\":[\\\"201901\\\"],\\\"label\\\":[\\\"原始数据\\\"],\\\"fileName\\\":\\\"190313安进1901检索.xlsx\\\",\\\"molecules\\\":[],\\\"markets\\\":[],\\\"sheetName\\\":\\\"1月数据\\\",\\\"length\\\":8568.0}}
```
