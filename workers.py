from pathlib import Path
import ffmpeg
from yt_dlp import YoutubeDL
import iofuncs
import helpers
import menu
import subprocess
import time

# ffmpeg wrapper functions

def ffmpeg_trim(input_file, output_file):
    process = (
        ffmpeg
        .input(input_file, ss=iofuncs.in_time, to=iofuncs.out_time)
        .output(output_file, codec="copy")
    )
    process.run()

def ffmpeg_join(input_text_file, input_folder, output_folder, output_filename):
    input_path = f"{input_folder}/{input_text_file}"
    process = (
        ffmpeg
        .input(input_path, f='concat', safe=0)
        .output(f"{output_folder}/{output_filename}")
    )
    process.run()
    helpers.remove_batch_file(input_folder, input_text_file)

def ffmpeg_timelapse_batch_process(input_folder, input_extension, speed_factor, output_folder, output_filename):
    PTS_batch_file = "PTS_Files_to_join.txt"
    PTS_suffix = "_setpts.mp4"
    helpers.create_ffmpeg_batch_file(input_folder, input_extension)
    for item in helpers.file_batch_list:
        process = (
            ffmpeg
            .input(item)
            .setpts(f"PTS/{speed_factor}")
            .output(f"{input_folder}/{Path(item).stem}{PTS_suffix}")
        )
        process.run()
    helpers.create_ffmpeg_batch_file(input_folder, input_extension, PTS_batch_file, PTS_suffix)
    ffmpeg_join(PTS_batch_file, input_folder, output_folder, output_filename)
    helpers.remove_files_by_ext(input_folder, PTS_suffix)
    helpers.remove_batch_file(input_folder, helpers.default_batch_file)

def ffmpeg_batch(input_folder, input_extension, output_folder):
    helpers.create_batch_list(input_folder, f"*.{input_extension}")
    for file in helpers.file_batch_list:
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
    iofuncs.choose_and_check_input_file()
    iofuncs.input_start_and_end_timestamps()
    iofuncs.choose_output_file_details()
    ffmpeg_trim(f"{iofuncs.ingest_folder}/{iofuncs.input_filename}", f"{iofuncs.output_folder_choice}/{iofuncs.output_filename}")
    menu.menu_function()

def join_function():
    iofuncs.choose_input_folder_and_extension()
    iofuncs.choose_output_file_details()
    helpers.create_ffmpeg_batch_file(iofuncs.input_folder_choice, iofuncs.input_extension_choice)
    ffmpeg_join(helpers.default_batch_file, iofuncs.input_folder_choice, iofuncs.output_folder_choice, iofuncs.output_filename)
    menu.menu_function()

def timelapse_function():
    iofuncs.choose_input_folder_and_extension()
    iofuncs.input_speed_factor()
    iofuncs.choose_output_file_details()
    ffmpeg_timelapse_batch_process(iofuncs.input_folder_choice, iofuncs.input_extension_choice, iofuncs.speed_factor, iofuncs.output_folder_choice, iofuncs.output_filename)
    menu.menu_function()

def batch_h264():
    iofuncs.choose_input_folder_and_extension()
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