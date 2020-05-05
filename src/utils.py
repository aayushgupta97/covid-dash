

def get_sliced_dataframe(df, start_col_index, end_col_index):
    return df.iloc[:, start_col_index:end_col_index+1]


def get_dataframe_with_columns(column_list, df):
    return df[column_list]


def sort_dataframe_desc_on_int_column(column, df):
    df[column] = df[column].astype(int)
    return df.sort_values(by=[column], ascending=False)