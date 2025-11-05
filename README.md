# book_disambiguation
Disambiguate book titles with the CBDB data.
# dependencies
pandas\
sqlite3\
os\
char_converter\
rapidfuzz
# usage
1. Extract the latest.db from [latest.7z](https://huggingface.co/datasets/cbdb/cbdb-sqlite/blob/main/latest.7z) to the program root directory.
2. Run "join_tables_from_latestdb.py" to get the CBDB data to compare your list against.
  - You can modify line 10 "DY_FILTER_LIST = []" to filter the data by dynasties.
  - The output of this step is the file "JOINED_BIOG_TEXT.xlsx".
3. Prepare your "input.xlsx" file.
  - Note that the file should be an xlsx file, NOT a csv or txt file.
  - The file must have the following columns: "internalindex", "title", "authorid" and/or "authorname"
  - The file can have many other columns as needed.
4. Run "book_disambiguation.ipynb". The default setting is to compare book titles against those by the author with the same CBDB id.
# variations of step 4
The "book_disambiguation.ipynb" can be modified in a number of ways. 
1. There are three modes of comparisons:
```
func = fuzzy_lookup_simple_id
# default setting: match author by CBDB id
func = fuzzy_lookup_by_id
# match author by CBDB id AND if no match by id, check against works with no known author (c_name_chn = 未詳)
func = fuzzy_lookup_by_name
# match author by Chinese character AND if no match by author name, check against works with no known author (c_name_chn = 未詳)
```
2. There are two defined algorithms of fuzzymatch:
```
scorer = fuzz.WRatio # for higher accuracy
scorer = compare_chars_scorer # for higher sensitivity
```
3. The score_cutoff for the fuzzymatch function can be adjusted:
```
score_cutoff = 80 # adjust if necessary
```
4. The data table to be compared against can also be replaced with the table of your own, with necessary modifications to the following lines:
```
comparetablename = "JOINED_BIOG_TEXT.xlsx" # change name if necessary
comparetable = pd.read_excel("JOINED_BIOG_TEXT.xlsx", sheet_name=0) 
comparecols=["c_title_chn", "c_textid", "c_name_chn", "c_personid","row_id"] # change column headers if necessary
```
5. You can disable char_converter by changing the value run_char = 1 to run_char = 0
