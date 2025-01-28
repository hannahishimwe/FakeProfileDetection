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
there are no NAs in my dataset
kevinhookebot is interesting to write about"""
import html
import re
import emoji

class CleanDatasets():

    def __init__(self, df, columns_to_rename, columns_to_drop, column_to_binary, binary_label="human", keep_capitalisation=True):
        self.df = df
        self.keep_capitalisation = keep_capitalisation
        self.columns_to_rename = columns_to_rename
        self.columns_to_drop = columns_to_drop
        self.column_to_binary = column_to_binary
        self.binary_label = binary_label

    def clean_whitespace(self, column="text"):
        self.df[column] = self.df[column].replace(r'\s+', ' ', regex=True).str.strip()
        return self.df
    
    def rename_columns(self, columns):
        self.df = self.df.rename(columns=columns)
        return self.df
    
    def drop_columns(self, columns):
        self.df = self.df.drop(columns=columns)
        return self.df
    
    def turn_category_to_binary(self, column):
        self.df[column] = self.df[column].apply(lambda x: 1 if x == self.binary_label else 0)
        return self.df
    
    def text_to_lowerCase(self, column="text"):
        if not self.keep_capitalisation:
            self.df[column] = self.df[column].str.lower()
        return self.df
    
    def decode_html_entities(self, column="text"):
        self.df[column] = self.df[column].apply(lambda x: html.unescape(x))
        return self.df

    def convert_unicode_to_emoji_description(self, column="text"):
        def unicode_to_char(text):
            """Convert <U+XXXX> to actual Unicode characters."""
            if isinstance(text, str): 
                return re.sub(r'<U\+([0-9A-Fa-f]+)>', lambda m: chr(int(m.group(1), 16)), text)
            return text  

        def demojize_text(text):
            """Convert emojis to text descriptions."""
            if isinstance(text, str):
                if any(char in emoji.EMOJI_DATA for char in text): 
                    return emoji.demojize(text) 
            return text

        self.df[column] = self.df[column].apply(unicode_to_char)
        self.df[column] = self.df[column].apply(demojize_text)
    
        return self.df

    
    def clean_df(self):
        """the order is very important to not lose information"""
        self.clean_whitespace()
        self.drop_columns(columns=self.columns_to_drop)
        self.turn_category_to_binary(column=self.column_to_binary)
        self.rename_columns(columns=self.columns_to_rename)
        self.convert_unicode_to_emoji_description()
        self.decode_html_entities()
        self.text_to_lowerCase()
        return self.df
