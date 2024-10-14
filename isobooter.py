import os
import subprocess
import shutil

# Function to copy the local ISO file
def copy_iso(source, destination):
    print(f"Copying ISO from {source} to {destination}...")
    shutil.copy2(source, destination)
    print(f"Copy complete: {destination}")

# Function to create bootisofile.cfg
def create_bootisofile(destination_path):
    isopath_line = f"    set isopath='{destination_path}'\n"
    bootisofile_content = f"""\
# 
#  Menu Entry 0       Boot An ISO file
#
#  ** Grub will boot this entry by default **
#
menuentry   'Boot An ISO file                                                   Hotkey=i'   --hotkey=i    --class isoboot   --class icon-isoboot  {{
     set reviewpause=2
     echo GNU Grub is preparing to boot  Boot An ISO file
     set gfxpayload=1024x768
# start-grub2win-custom-code
#
#            This is sample code for booting from an iso file
#            via the Grub2Win g2wisoboot function
#
#            See the Grub2Win help file advanced topics section for more information
#
#            Note: There are many many ISO files available. They are all different.
#                  You must examine your particular ISO file with a utility like 7-Zip to
#                  obtain the proper kernel and initrd paths.
#                  You can then set the kernelpath and initrdpath variables below.
#                  The kernel and initrd files will not be found unless the correct paths are set.         
#
     clear
{isopath_line}\
     set kernelpath='/casper/vmlinuz'                 # Example '/vmlinuz'
     set initrdpath='/casper/initrd.lz'                 # Example '/initrd.img'
     set bootparms='boot=casper iso-scan/filename=$isopath reboot=cold nomodeset noprompt noeject ---'          # Example 'boot=/ iso-scan/filename=$isopath noprompt noeject ---'
#
     g2wisoboot                                          # Run the g2wisoboot function
#
# end-grub2win-custom-code
     savelast 0 'Boot An ISO file'
}}\
"""
    # Create or overwrite the bootisofile.cfg with the new content
    with open("C:/grub2/windata/customconfigs/bootisofile.cfg", 'w') as f:
        f.write(bootisofile_content)
    print("bootisofile.cfg created successfully.")

# Function to copy the configuration file
def copy_config(source, destination):
    print(f"Copying config file from {source} to {destination}...")
    shutil.copy2(source, destination)
    print(f"Config file copy complete: {destination}")

# Disable test signing (Windows command)
subprocess.run(["bcdedit", "-set", "TESTSIGNING", "OFF"], shell=True)

# Start Grub2Win installation
grub2win_path = os.path.join(os.getcwd(), "grub2win", "G2WInstall.exe")
subprocess.run([grub2win_path], shell=True)
input("Press any key after Grub2Win installation is complete...")

# Copy grub.cfg
shutil.copyfile(os.path.join(os.getcwd(), "grub.cfg"), "C:/grub2/grub.cfg")
os.makedirs("C:/grub2/windata/customconfigs", exist_ok=True)

# Get the path to the local ISO from the user
iso_path = input("Enter the full path to the local ISO file: ")
iso_name = os.path.basename(iso_path)
destination_path = os.path.join("C:/", iso_name)

# Copy the ISO file to the destination
copy_iso(iso_path, destination_path)

# Create bootisofile.cfg with the correct isopath
create_bootisofile(destination_path)

# Define the configuration file name and paths
config_file_name = "bootisofile.cfg"
source_config_path = "C:/grub2/windata/customconfigs/bootisofile.cfg"
destination_config_path = os.path.join(os.getcwd(), config_file_name)

# Copy the modified config file back to the original location
copy_config(source_config_path, destination_config_path)

# Ask if the user wants to shut down
shutdown_choice = input("Do you want to shut down now? (Y/N): ").strip().lower()

if shutdown_choice == 'y':
    subprocess.run(["shutdown", "/r"], shell=True)
else:
    print("Shutdown canceled. The system will not restart.")
