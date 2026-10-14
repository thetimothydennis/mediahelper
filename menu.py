import subprocess
import workers
import time

break_point=True

# menu function
def menu_function():
    global break_point
    subprocess.run('clear')
    print("""
    ~~~~~~~~~~~~~~~~~~~~~~~~~ Media Utilities ~~~~~~~~~~~~~~~~~~~~~~~~~
    !!!!!  NOTE: All names of files and folders you want to use in this 
    program must be alphanumeric. The script will not work if there are
    nspaces in the file or folder names. !!!!!


    1. Trim utility
    2. Join utility
    3. Timelapse utility
    4. Batch H264 utility
    5. YouTube download utility
    6. Convert video to audio utility
    7. Convert ODT to PDF utility
    Q. Exit this program
    """)
    menu_choice=input("Choose your destiny: ")
      # menu choice cases
    
    match menu_choice:
        case "1": 
            print("You chose trim.")
            workers.trim_function()
        case "2":
            print("You chose join.")
            workers.join_function()
        case "3":
            print("You chose timelapse.")
            workers.timelapse_function()
        case "4":
            print("You chose batch H264.")
            workers.batch_h264()
        case "5":
            print("You chose YouTube download.")
            workers.yt_download()
        case "6":
            print("You chose convert video to audio.")
            workers.convert_video_to_audio()
        case "7":
            print("You chose convert ODT to PDF.")
            workers.convert_odt_to_pdf()
        case "Q" | "q":
            print("Goodbye!")
            break_point=False
        case _:
            print("That is not a valid option.")
            time.sleep(1)
            menu_function()
