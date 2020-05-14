import subprocess
import tkinter

main = tkinter.Tk()


def create_textarea():
    textfield = tkinter.Text(main)
    textfield.pack()
    textfield.insert(tkinter.INSERT, "=== Waiting for command ===\n")
    return textfield


def run_command(command):
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')


def list_directory():
    command_output = run_command(['ls'])
    text.insert(tkinter.INSERT, command_output)


def list_devices():
    command_output = run_command(['sudo', 'dfu-util', '-l'])
    text.insert(tkinter.INSERT, command_output)


def backup_firmware():
    command_output = run_command(['sudo', 'dfu-util', '-a', '0', '-U', 'backup.bin', '-s', '0x08000000:131072'])
    text.insert(tkinter.INSERT, command_output)


def create_list_button(location):
    return tkinter.Button(location, text="List connected devices", command=list_devices).pack(side=tkinter.LEFT)


def create_backup_button(location):
    return tkinter.Button(location, text="Backup device firmware", command=backup_firmware).pack(side=tkinter.LEFT)


menu_bar = tkinter.Frame(main)
menu_bar.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
list_button = create_list_button(menu_bar)
backup_button = create_backup_button(menu_bar)
text = create_textarea()

main.mainloop()
