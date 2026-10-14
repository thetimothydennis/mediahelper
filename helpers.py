from pathlib import Path
# create batch list for ffmpeg jobs

default_batch_file = "FilesToJoin.txt"
file_batch_list = []

def create_batch_list(input_folder, suffix):
    global file_batch_list
    file_batch_list = list(Path(input_folder).rglob(f"*{suffix}"))

def create_ffmpeg_batch_file(input_folder, input_extension, batch_list_name="FilesToJoin.txt", suffix=""):
    global file_batch_list
    if suffix is not "":
        create_batch_list(input_folder, suffix)
    else:
        create_batch_list(input_folder, f".{input_extension}")
    with open(f"{input_folder}/{batch_list_name}", "w", encoding="utf-8") as files_to_join:
        for file in sorted(file_batch_list):
            files_to_join.write(f"file '{file}'\n")

def remove_batch_file(input_folder, batch_file):
    Path(f"{input_folder}/{batch_file}").unlink(missing_ok=True)

def remove_files_by_ext(input_folder, suffix):
    remove_files = Path(f"{input_folder}").rglob(f"*{suffix}")
    for file in remove_files:
        Path(file).unlink(missing_ok=True)