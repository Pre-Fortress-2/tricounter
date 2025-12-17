# tricounter
 Will generate a spreadsheet with data on all of the mdl files of a given folder.

## IMPORTANT
**The data outputted from `studiomdl.exe` is inconsistent and mostly relies on Shader Draw Count instead of actual Tris. Please bare this in mind!**

## Usage
- Place `tricounter.py` in `game/bin` folder, such as `Team Fortress 2/bin`.
- Run the program with 2 arguments
    1. Desired folder you wish to analyze the `.mdl` files of (e.g. `..\tf\models\props_movies\`)
    2. Location of `gameinfo.txt` file (e.g. `..\tf\`)
```cmd
python .\tricounter.py ..\tf\models\props_movies\ ..\tf\
```

In this example it would generate a `tf_vtx_data.csv` file that can be opened in any spreadsheet software.