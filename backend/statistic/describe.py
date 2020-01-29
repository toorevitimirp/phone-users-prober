import pandas as pd
def describe(clean_data):
    descriptions = clean_data.describe()
    descriptions_dic = {}
    # for row in descriptions.itertuples():
    #     print(row)
    # for index, row in descriptions.iteritems():
    #     print(type(row))
    for column in descriptions.columns:
        description = {}
        i = 0
        maps = {1:"mean",2:"std",3:"min",4:"25%",5:"50%",6:"75%",7:"max"}
        # print(descriptions[column])
        for row in descriptions[column]:
            if i:
                description[maps[i]] = row
            i += 1
        descriptions_dic[column] = description
    return descriptions_dic
