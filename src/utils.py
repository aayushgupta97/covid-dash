from numpy import random

def get_sliced_dataframe(df, start_col_index, end_col_index):
    return df.iloc[:, start_col_index:end_col_index+1]


def get_dataframe_with_columns(column_list, df):
    return df[column_list]


def sort_dataframe_desc_on_int_column(column, df):
    df[column] = df[column].astype(int)
    return df.sort_values(by=[column], ascending=False)

def rename_columns_df(mapping_dictionary, df):
    return df.rename(columns=mapping_dictionary)

def label_to_color(names, r_min=0, r_max=255, g_min=0, g_max=255, b_min=0, b_max=255):
    """Mapping of names to random rgb colors.
    Parameters:
    df (Series): Pandas Series containing names.
    r_min (int): Mininum intensity of the red channel (default 0).
    r_max (int): Maximum intensity of the red channel (default 255).
    g_min (int): Mininum intensity of the green channel (default 0).
    g_max (int): Maximum intensity of the green channel (default 255).
    b_min (int): Mininum intensity of the blue channel (default 0).
    b_max (int): Maximum intensity of the blue channel (default 255).
    Returns:
    dictionary: Mapping of names (keys) to random rgb colors (values)
    """
    mapping_colors = dict()
    
    for name in names.unique():
        red = random.randint(r_min, r_max)
        green = random.randint(g_min, g_max)
        blue = random.randint(b_min, b_max)
        rgb_string = 'rgb({}, {}, {})'.format(red, green, blue)
    
        mapping_colors[name] = rgb_string
    
    return mapping_colors