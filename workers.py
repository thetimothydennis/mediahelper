from pathlib import Path
import ffmpeg
from yt_dlp import YoutubeDL
import iofuncs
import menu
import subprocess
import time

# create batch list for ffmpeg jobs

def create_batch_list(input_folder, input_extension):
    global file_batch_list
    global default_batch_file
    default_batch_file = "FilesToJoin.txt"
    file_batch_list=list(Path(input_folder).rglob(f"*.{input_extension}"))
    with open(f"{input_folder}/{default_batch_file}", "w", encoding="utf-8") as files_to_join:
        for file in sorted(file_batch_list):
            files_to_join.write(f"file '{file}'\n")

# ffmpeg wrapper functions

def ffmpeg_trim(input_file, output_file):
    process = (
        ffmpeg
        .input(input_file, ss=iofuncs.in_time, to=iofuncs.out_time)
        .output(output_file, codec="copy")
    )
    process.run()

def ffmpeg_join(input_text_file, input_folder, output_folder, output_filename):
    global file_batch_list
    input_path = f"{input_folder}/{input_text_file}"
    process = (
        ffmpeg
        .input(input_path, f='concat', safe=0)
        .output(f"{output_folder}/{output_filename}")
    )
    process.run()
    Path(f"{input_folder}/{input_text_file}").unlink(missing_ok=True)

def timelapse_batch_process(input_folder, input_extension, speed_factor):
    create_batch_list(input_folder, input_extension)
    global file_batch_list
    for item in file_batch_list:
        process = (
            ffmpeg
            .input(item)
            .setpts(f"PTS/{speed_factor}")
            .output(f"{input_folder}/{Path(item).stem}_setpts.mp4")
        )
        process.run()

def ffmpeg_batch(input_folder, input_extension, output_folder):
    file_batch_list=list(Path(input_folder).rglob(f"*.{input_extension}"))
    for file in file_batch_list:
        filepath = Path(file)
        process = (
            ffmpeg
            .input(file)
            .output(f"{output_folder}/{filepath.stem}_h264.mp4", vcodec="libx264", preset="fast", crf=22, acodec="aac")
        )
        process.run()

def ffmpeg_video_to_audio(input_filename, output_folder, output_filename):
    process = (
        ffmpeg
        .input(f"{iofuncs.ingest_folder}/{input_filename}")
        .output(f"{output_folder}/{output_filename}", acodec="libmp3lame")
    )
    process.run()

# top level menu functions

def trim_function():
    global input_filename
    iofuncs.choose_and_check_input_file()
    iofuncs.input_start_and_end_timestamps()
    iofuncs.choose_output_file_details()
    ffmpeg_trim(f"{iofuncs.ingest_folder}/{iofuncs.input_filename}", f"{iofuncs.output_folder_choice}/{iofuncs.output_filename}")
    menu.menu_function()

def join_function():
    iofuncs.choose_input_folder_and_extension()
    iofuncs.choose_output_file_details()
    create_batch_list(iofuncs.input_folder_choice, iofuncs.input_extension_choice)
    ffmpeg_join(default_batch_file, iofuncs.input_folder_choice, iofuncs.output_folder_choice, iofuncs.output_filename)
    menu.menu_function()

def timelapse_function():
    iofuncs.choose_input_folder_and_extension()
    iofuncs.input_speed_factor()
    iofuncs.choose_output_file_details()
    timelapse_batch_process(iofuncs.input_folder_choice, iofuncs.input_extension_choice, iofuncs.speed_factor)
    global file_batch_list
    PTS_batch_file = "PTS_Files_to_join.txt"
    PTS_suffix = "_setpts.mp4"
    with open(f"{iofuncs.input_folder_choice}/{PTS_batch_file}", "w", encoding="utf-8") as pts_files:
        for item in sorted(file_batch_list):
            filepath = Path(item)
            pts_files.write(f"file '{filepath.parent}/{filepath.stem}{PTS_suffix}'\n")
    ffmpeg_join(PTS_batch_file, iofuncs.input_folder_choice, iofuncs.output_folder_choice, iofuncs.output_filename)
    remove_files = Path(f"{iofuncs.input_folder_choice}").rglob(f"*{PTS_suffix}")
    for file in remove_files:
        Path(file).unlink()
    Path(f"{iofuncs.input_folder_choice}/{default_batch_file}").unlink(missing_ok=True)
    menu.menu_function()

def batch_h264():
    iofuncs.choose_and_check_input_folder()
    iofuncs.choose_input_file_extension()
    iofuncs.choose_and_verify_output_folder()
    ffmpeg_batch(iofuncs.input_folder_choice, iofuncs.input_extension_choice, iofuncs.output_folder_choice)
    menu.menu_function()

def convert_video_to_audio():
    iofuncs.choose_and_check_input_file()
    iofuncs.choose_output_file_details()
    ffmpeg_video_to_audio(iofuncs.input_filename, iofuncs.output_folder_choice, iofuncs.output_filename)
    menu.menu_function()

def yt_download():
    iofuncs.choose_address()
    iofuncs.choose_output_file_details()
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': "mp4",
        'quiet': False,
        'outtmpl': f"{iofuncs.output_folder_choice}/{iofuncs.output_filename}"
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(iofuncs.address)
    menu.menu_function()

def convert_odt_to_pdf():
    iofuncs.choose_and_check_input_file()
    iofuncs.choose_output_file_details()
    subprocess.run([
        "lowriter", "--convert-to", "pdf", "--outdir", iofuncs.output_folder_choice, f"{iofuncs.ingest_folder}/{iofuncs.input_filename}"
    ])
    time.sleep(5)
    menu.menu_function()