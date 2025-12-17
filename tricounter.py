import sys
import subprocess
import os
import pathlib

def call_studiomdl(mdl_path: str, gameinfo_path: str) -> None:
    base_command = ["studiomdl.exe" "-mdlreport", None, "-perf", "-game", None, "-nop4", "-mdlreportspreadsheet"] # we need index 2 and 5
    base_command[2] = mdl_path
    base_command[5] = gameinfo_path

    returned_output = subprocess.check_output(base_command)
    make_spreadsheet(returned_output)

def make_spreadsheet(studio_mdl_output: str):
    print(studio_mdl_output)
    
def main() -> None:
    mdl_path = sys.argv[1]
    gameinfo_path = sys.argv[2]  
    print(f"Selected Path: {mdl_path}\nSelected GameInfo: {gameinfo_path}")

    if not os.path.isdir(mdl_path) or not os.path.exists(gameinfo_path):
        if not os.path.isdir(mdl_path):
            print(f"{mdl_path} is not a real path.")
        if not os.path.exists(gameinfo_path):
            print(f"{gameinfo_path} is not a real path.")
        input("Press any key to exit.")
        sys.exit()

    call_studiomdl(mdl_path, gameinfo_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Incorrect usage: Too few parameters. Must specify folder path and 'gameinfo.txt' path.")
        input("Press any key to exit.")
        sys.exit()
    if len(sys.argv) > 3:
        print("Incorrect usage: Too many parameters. Must specify folder path and 'gameinfo.txt' path.")
        input("Press any key to exit.")
        sys.exit()
    if not os.getcwd().endswith("bin"):
        print("Incorrect usage: This program should only be run from the 'bin' folder.")
        # input("Press any key to exit.")
        # sys.exit()
    main()