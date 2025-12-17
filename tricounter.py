import sys
import subprocess
import os
import pathlib
import csv

def call_studiomdl(mdl_path: str, gameinfo_path: str) -> [[str]], str:
    # We need to replace index 2 with each model in the folder 
    base_command = ["studiomdl.exe", "-mdlreport", None, "-perf", "-game", gameinfo_path, "-nop4", "-mdlreportspreadsheet"]
    meshes = []
    game_name = "mod" # placeholder
    for (root, _, files) in os.walk(mdl_path, topdown=True):
        for file in files:
            if file.endswith(".mdl"):
                try:
                    # Replace index 2 with .mdl file path
                    base_command[2] = root + "/" + file
                    returned_output = subprocess.check_output(base_command, text=True)
                except Exception as e:
                    print(e)
                    sys.exit()

                # Turn output into list and find entry with dx90
                entries = returned_output.split("\n")
                for entry in entries:
                    if "dx90" in entry:
                        mesh_entry = entry

                # Replace forward slash with back slash and turn mesh path into list 
                mesh_data = mesh_entry.split(",")
                mesh_path = mesh_data[0].replace("/","\\").split("\\")

                # Find game name
                game_index = mesh_path.index("models") - 1
                game_name = mesh_path[game_index]
                # Turn mesh path back into string with back slash and replace path data
                mesh_data[0] = "\\".join(mesh_path[game_index:])

                meshes.append(mesh_data)
    
    return meshes, game_name

def make_spreadsheet(meshes: [[str]], game_name: str) -> None:
    # "[Path to VTX, VTX file extension, Number of LODs], [Tri count, Batches rendered, Materials used], [Tri count, Batches rendered, Materials used]"
    # ..\tf_OLD\models\buildables\dispenser.dx80.vtx,.dx80.vtx,5,14172,4,2,9860,4,2,7490,5,2,4928,5,2,3196,5,2,
    
    meshes.insert(0, ["Path to VTX", "File Extension", "Number of LODs", "LOD0 Tri Count", "LOD0 Batches Rendered", "LOD0 Materials Used"])

    with open(f"{game_name}_vtx_data.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(meshes)
    
def main() -> None:
    mdl_path = sys.argv[1]
    gameinfo_path = sys.argv[2]  
    print(f"Selected Path: {mdl_path}\nSelected GameInfo: {gameinfo_path}")

    if not os.path.isdir(mdl_path) or not os.path.isdir(gameinfo_path):
        if not os.path.isdir(mdl_path):
            print(f"{mdl_path} is not a real path or directory.")
        if not os.path.isdir(gameinfo_path):
            print(f"{gameinfo_path} is not a real path or directory.")
        input("Press any key to exit.")
        sys.exit()

    meshes, game_name = call_studiomdl(mdl_path, gameinfo_path)
    make_spreadsheet(meshes, game_name)
    # input("Spreadsheet Complete.\nPress any key to exit.")

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
        print("Incorrect usage: This program should only be run from the 'game/bin' folder.")
        # input("Press any key to exit.")
        # sys.exit()
    main()