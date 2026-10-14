from pathlib import Path

ingest_folder=Path('/mnt/ingest')
main_output_folder=Path('/mnt/output')

## input
# input functions
def choose_input_folder():
    global input_folder_choice
    input_folder_choice=input("Type name of input folder ('.' for current folder): ")

def choose_input_file():
    global input_filename
    input_filename=input("Type name of input file: ")

def choose_input_file_extension():
    global input_extension_choice
    input_extension_choice=input("Type file extension for files to be modified (no '.'): ")

def choose_address():
    global address
    address=input("Type address for YouTube video to download: ")

def input_start_timestamp():
    # prompt for in-point timestamp
    global in_time
    in_time=input("Input timestamp for in-point (ex: HH:MM:SS.mss) -- ")

def input_end_timestamp():
    # prompt for out-point timestamp
    global out_time
    out_time=input("Input timestamp for out-point (ex: HH:MM:SS.mss) -- ")

def input_speed_factor():
    print("Factor by which to speed up the video.")
    global speed_factor
    speed_factor=input("For double speed, use 2, for quadrouple speed, use 4, etc.: ")


# input check functions
def check_input_folder():
    global input_folder_choice
    is_folder = False
    while is_folder is False:
        if Path(f"{ingest_folder}/{input_folder_choice}").is_dir():
            print(f"folder {ingest_folder}/{input_folder_choice} exists")
            input_folder_choice = f"{ingest_folder}/{input_folder_choice}"
            is_folder = True
        else:
            print(f"folder {input_folder_choice} does not exist, try atain")
            choose_input_folder()
            
def check_input_filename():
    global input_filename
    global ingest_folder
    is_file = False
    while is_file is False:
        if Path(f"{ingest_folder}/{input_filename}").is_file():
            print(f"file {input_filename} exists")
            is_file = True
        else:
            print(f"file {input_filename} does not exist, try again.")
            choose_input_file()


# grouped input functions
def choose_and_check_input_folder():
    choose_input_folder()
    check_input_folder()

def choose_and_check_input_file():
    choose_input_file()
    check_input_filename()

def choose_input_folder_and_extension():
    choose_and_check_input_folder()
    choose_input_file_extension()

def input_start_and_end_timestamps():
    input_start_timestamp()
    input_end_timestamp()


## output
# output functions
def choose_output_folder():
    global output_menu_choice
    print("\n~~~~~Choose output directory.~~~~~\n")
    print("1. Ingest folder")
    print("2. Output folder")
    output_menu_choice=input("Make a selection: ")

def choose_output_filename():
    global output_filename
    output_filename=input("Type filename for final file output: ")

# output check functions
def verify_output_folder_choice():
    global output_menu_choice
    global output_folder_choice
    global ingest_folder
    global main_output_folder
    invalid_output=True
    while invalid_output:
        match output_menu_choice:
            case "1":
                print("You chose Ingest")
                output_folder_choice=ingest_folder
                invalid_output=False
            case "2":
                print("You chose Output")
                output_folder_choice=main_output_folder
                invalid_output=False
            case _:
                print("Not a valid output directory choice, try again")
                choose_output_folder()


# grouped output functions
def choose_output_file_details():
    choose_output_filename()
    choose_output_folder()
    verify_output_folder_choice()

def choose_and_verify_output_folder():
    choose_output_folder()
    verify_output_folder_choice()