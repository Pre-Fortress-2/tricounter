import sys
import subprocess
import os
import pathlib
import csv

def gather_mesh_data(mdl_path: str, gameinfo_path: str) -> ([[str]], str, int):
    # We need to replace index 2 with each model in the folder 
    base_command = ["studiomdl.exe", "-mdlreport", None, "-perf", "-game", gameinfo_path, "-nop4", "-mdlreportspreadsheet"]
    meshes = []
    game_name = "mod"
    max_lod = 0
    for (root, _, files) in os.walk(mdl_path, topdown=True):
        for file in files:
            if file.endswith(".mdl"):
                print(f"Analyzing: {file:=<58}|", end="\r")
                try:
                    # Replace index 2 with .mdl file path
                    base_command[2] = root + "/" + file
                    returned_output = subprocess.check_output(base_command, text=True)
                except Exception as e:
                    print(" " * 70, end="\r")
                    print(f"ERROR: Failed to process {file}. Continuing.")

                # Turn output into list and find entry with dx90
                entries = returned_output.split("\n")
                for entry in entries:
                    if "dx90" in entry:
                        mesh_entry = entry

                # Replace forward slash with back slash and turn mesh path into list 
                mesh_data = mesh_entry.split(",")
                mesh_path = mesh_data[0].replace("/","\\").split("\\")
                
                if int(mesh_data[2]) > max_lod:
                    max_lod = int(mesh_data[2]) 

                # Find game name
                game_index = mesh_path.index("models") - 1
                game_name = mesh_path[game_index]
                # Turn mesh path back into string with back slash and replace path data
                mesh_data[0] = "\\".join(mesh_path[game_index:])
                meshes.append(mesh_data)
    print(f"{('Analysis Complete '):=<69}|") # nice
            
    return meshes, game_name, max_lod

def make_spreadsheet(meshes: [[str]], game_name: str, max_lod: int, models_root_dir: str) -> None:
    print(f"Saving to: {game_name}_{models_root_dir}_vtx_data.csv")
    heading = ["Path to VTX", "File Extension", "Number of LODs"]
    for i in range(max_lod):
        heading.extend([f"LOD{i} Tri Count", f"LOD{i} Batches Rendered", f"LOD{i} Materials Used"])
    meshes.insert(0, heading)
    
    with open(f"{game_name}_{models_root_dir}_vtx_data.csv", "w", newline="") as csv_file:
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

    print("Gathering mesh data. This could take a while...")
    meshes, game_name, max_lod = gather_mesh_data(mdl_path, gameinfo_path)
    
    mdl_root_dir = mdl_path.replace("/", "\\").split("\\")
    try:
        mdl_root_dir.remove("")
    except Exception as e:
        print("DEBUG: No empty space.")
    print("Generating spreadsheet. Nearly there!")

    make_spreadsheet(meshes, game_name, max_lod, mdl_root_dir[-1:][0])
    input("> Spreadsheet Complete!\nPress any key to exit.")

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
        input("Press any key to exit.")
        sys.exit()
    print("-" * 70)
    print("""Welcome to 
  _____     _                       _            
 |_   _| __(_) ___ ___  _   _ _ __ | |_ ___ _ __ *
   | || '__| |/ __/ _ \| | | | '_ \| __/ _ \ '__|
   | || |  | | (_| (_) | |_| | | | | ||  __/ |   
   |_||_|  |_|\___\___/ \__,_|_| |_|\__\___|_|   
""")
    print("-" * 70 + "\n*Your mileage may vary!\n")
    main()