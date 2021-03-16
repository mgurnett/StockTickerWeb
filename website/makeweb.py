from pretty_html_table import build_table

def make_web (name, df):
    # html_table = build_table(df, 'blue_dark')
    # file_name = ('games_folder/' + name + ".html")
    file_name = (name + ".html")
    # text_file = open(file_name, "w")
    # text_file.write(html_table)
    # text_file.close()

    with open(file_name, 'w') as fo:
        df.to_html(fo)