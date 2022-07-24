import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis


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


def calc_name(name, sheet_name, table, sum_per_year, normal):
    df = pd.DataFrame()
    i = 0
    for row in table:
        i += 1
        if i < 13:
            continue
        total_count = row[1][1]
        row = process_row(row[1])
        if not row.name == name[::-1]:
            continue
        if normal:
            row *= (1 / sum_per_year)
            row *= 100

        row.name = edit_name(name, sheet_name)
        df = pd.DataFrame(row)
        break
    return df


def check_names(table, count, high, test, sheet_name):
    test_method = lambda x: 1
    if test == 'skew':
        test_method = skew
    if test == 'kurtosis':
        test_method = kurtosis
    results = []
    i = 0
    for row in table:
        i += 1
        if i < 13:
            continue
        total_count = row[1][1]
        if total_count < 200:
            continue
        row = process_row(row[1])
        test = test_method(row)
        if len(results) < count:
            results.append((row.name, test))
        elif (high and test > results[0][1]) or (not high and test < results[0][1]):
            results[0] = (row.name, test)

        results = sorted(results, key=lambda i: i[1])
        if not high:
            results = results[::-1]

    return list(map(lambda x: (x[0][::-1], sheet_name), results))


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
        table = [boys_data, girls_data][name_sheet[1]].iterrows()
        sum_per_year = [sum_of_boys, sum_of_girls][name_sheet[1]]
        df_list.append(calc_name(name_sheet[0], name_sheet[1], table, sum_per_year, normal))
    df = pd.concat(df_list, axis=1)
    df.plot()
    title = 'ילדים שנולדו באותה שנה לפי שם'
    if normal:
        title += ' באחוזים'
    plt.title(title[::-1])
    plt.show()


def search_name(sheet_name, count, high, test):
    excel_data = pd.read_excel('./data.xlsx', sheet_name=sheet_name)
    table = excel_data.iterrows()
    return check_names(table, count, high, test, sheet_name)


names = search_name(1, 5, True, 'kurtosis')
show_name_list(names, False)
