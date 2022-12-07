# Executes GREP on your Android device, and returns a Pandas DataFrame 

```python
pip install adb-grep-search
```

```python
from adb_grep_search import ADBGrep
adb_path = "C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"
deviceserial = "localhost:5875"
gre = (
    ADBGrep(adb_path=adb_path, deviceserial=deviceserial)
    .connect_to_adb()
    .activate_root_grep() # If your device is rooted, su will be activated
)
df = gre.grep(
    folder_to_search="data/data",
    filetype="*.db",
    regular_expression=r"CREATE.TABLE",
    exit_keys="ctrl+x", 
    timeout=None,
    remove_control_characters=True,
)
print(df)
                                               aa_file  ...      aa_regex
0    data/data/com.android.providers.media/database...  ...  CREATE.TABLE
1    data/data/com.android.providers.media/database...  ...  CREATE.TABLE
2    data/data/com.android.providers.media/database...  ...  CREATE.TABLE
3    data/data/com.android.providers.media/database...  ...  CREATE.TABLE
4    data/data/com.android.providers.contacts/datab...  ...  CREATE.TABLE
..                                                 ...  ...           ...
99   data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
100  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
101  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
102  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
103  data/data/com.roblox.client/databases/google_a...  ...  CREATE.TABLE
[104 rows x 5 columns]

```
