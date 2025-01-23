"""
Cleaning text dataset
Remove extra lines
Remove extra spaces
Remove extra tabs
Remove extra new lines
Rename columns
Drop columns - not needed for research problem
Get rid of unicode characters
Rename Account type to isHuman -> if human 1 else 0
have parameters for preprocessing dependent on what will be trained? (e.g. capitilisation left in or out)
there are no NAs in my dataset"""
class CleanDatasets():

    def __init__(self, df, columns_to_rename, columns_to_drop, column_to_binary, keep_capitalisation=False):
        self.df = df
        self.keep_capitalisation = keep_capitalisation
        self.columns_to_rename = columns_to_rename
        self.columns_to_drop = columns_to_drop
        self.column_to_binary = column_to_binary

    def remove_extra_lines(self):
        self.df = self.df.replace(r'\n', ' ', regex=True)
        return self.df

    def remove_extra_spaces(self): 
        self.df = self.df.replace(r'\s+', ' ', regex=True)
        return self.df
    
    def remove_extra_tabs(self):
        self.df = self.df.replace(r'\t', ' ', regex=True)
        return self.df
    
    """
    IMPLEMENT AND ALSO OTHER WEIRD UNICODE CHARACTERS
    """
    def remove_unicode_characters(self):
        self.df = self.df.replace(r'[^\x00-\x7F]+', ' ', regex=True)
        return self.df

    def remove_extra_new_lines(self):
        self.df = self.df.replace(r'\r', ' ', regex=True)
        return self.df
        
    def rename_columns(self, columns):
        self.df = self.df.rename(columns=columns)
        print(self.df.head())
        return self.df
    
    def drop_columns(self, columns):
        self.df = self.df.drop(columns=columns)
        print(self.df.head())
        return self.df
    
    def turn_category_to_binary(self, column):
        self.df[column] = self.df[column].apply(lambda x: 1 if x == 'human' else 0)
        print(self.df.head())
        return self.df
    
    def text_to_lowerCase(self, column="text"):
        if not self.keep_capitalisation:
            self.df[column] = self.df[column].str.lower()
        return self.df
    
    def clean_df(self):
        self.df = self.remove_extra_lines()
        self.df = self.remove_extra_spaces()
        self.df = self.remove_extra_tabs()
        self.df = self.remove_extra_new_lines()
        self.df = self.drop_columns(columns=self.columns_to_drop)
        self.df = self.turn_category_to_binary(column=self.column_to_binary)
        self.df = self.rename_columns(columns=self.columns_to_rename)
        self.df = self.text_to_lowerCase()
        return self.df
