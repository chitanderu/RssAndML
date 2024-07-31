import pandas as pd

# 读取Excel文件
excel_data = pd.read_excel('text.xlsx')

# 遍历所有数据
new_rows = []
drop_indexes=[]
for index, row in excel_data.iterrows():
    # 检查总发行批次是否大于1
    if row['总发行批次'] > 1:
        # 拆分利率、发行期限、累计发行金额等列中的数据
        rates = row['利率'].split(',')
        limits = row['发行期限'].split(',')
        amounts = row['累计发行金额'].split(',')
        # 将拆分后的数据作为新的行添加到数据框中
        for i in range(len(rates)):
            new_row = {
                '总发行批次': 1,
                '地区': row['地区'],
                '年份': row['年份'],
                '利率': rates[i],
                '累计发行金额': amounts[i],
            }
            new_rows.append(new_row)
        drop_indexes.append(index)
# 将拆分后的数据添加到原始数据框中
new_data = pd.concat([excel_data, pd.DataFrame(new_rows)])
new_data = new_data.drop(drop_indexes)

# 显示拆分后的数据
print(new_data.head())
new_data.to_excel('cleandata.xlsx', index=False)