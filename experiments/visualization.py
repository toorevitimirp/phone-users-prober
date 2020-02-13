import pandas as pd
import matplotlib.pyplot as plt
from data import get_all_data

data_all = get_all_data()


def bar_plot():
    grouped = data_all.groupby('label')
    col = 'users_3w'
    grouped[col].value_counts().unstack().plot(kind='bar', figsize=(20, 4))


def main():
    bar_plot()


if __name__ == '__main__':
    main()
