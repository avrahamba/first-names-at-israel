import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def replace_data(count_list):
    for i in range(len(count_list)):
        if count_list[i] == '.':
            count_list[i] = 0
        elif count_list[i] == '..':
            count_list[i] = np.random.randint(1, 5)
        else:
            count_list[i] = int(count_list[i])
    return np.array(count_list)


def process_row(row):
    res = pd.Series(data=replace_data(row[2:]), name=row[0][::-1], index=range(1948, 2022))
    return res


def edit_name(name, sheet):
    return F"{name} ה{['בן', 'בת'][sheet]}"[::-1]


def calc_name(name, sheet_name, data_excel, sum_per_year, normal):
    table = data_excel.iterrows()
    df = pd.DataFrame()
    i = 0
    for row in table:
        i += 1
        if i < 13:
            continue
        row = process_row(row[1])
        if normal:
            row *= (1 / sum_per_year)
            row *= 100
        if not row.name == name[::-1]:
            continue
        row.name = edit_name(name, sheet_name)
        df = pd.DataFrame(row)
        break
    return df


def how_many_at_year(data_excel):
    table = data_excel.iterrows()
    i = 0
    series_list = []
    for row in table:
        i += 1
        if i < 13:
            continue
        series_list.append(process_row(row[1]))
    df = pd.DataFrame(series_list)
    sum_list = []
    for column in df:
        sum_list.append(df[column].sum())
    return pd.Series(sum_list, index=range(1948, 2022))


def show_name_list(name_sheet_list, normal):
    boys_data = pd.read_excel('./data.xlsx', sheet_name=0)
    sum_of_boys = how_many_at_year(boys_data)
    girls_data = pd.read_excel('./data.xlsx', sheet_name=1)
    sum_of_girls = how_many_at_year(girls_data)

    df_list = []
    for name_sheet in name_sheet_list:
        df_list.append(calc_name(name_sheet[0], name_sheet[1], [boys_data, girls_data][name_sheet[1]],
                                 [sum_of_boys, sum_of_girls][name_sheet[1]], normal))
    df = pd.concat(df_list, axis=1)
    df.plot()
    title = 'ילדים שנולדו באותה שנה לפי שם'
    if normal:
        title += ' באחוזים'
    plt.title(title[::-1])
    plt.show()


show_name_list([('יהונתן', 0),('יונתן', 0),('נועם', 0),('דוד', 0)], True)
