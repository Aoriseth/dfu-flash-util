import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QComboBox

connected_devices = []


def run_command(command):
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')


@dataclass
class Device(object):
    alt: str
    name: str
    address: str
    size: str


class MultiLineText(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setText("=== Waiting for command ===\n")


class DeviceInfo(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.device_alt = QLabel()
        self.device_alt.setText("Alt: ")
        self.device_name = QLabel()
        self.device_name.setText("Name: ")
        self.device_address = QLabel()
        self.device_address.setText("Address: ")
        self.device_size = QLabel()
        self.device_size.setText("Size: ")

        self.addWidget(self.device_alt)
        self.addWidget(self.device_name)
        self.addWidget(self.device_address)
        self.addWidget(self.device_size)

    def set_device(self, device):
        self.device_alt.setText("Alt: "+device.alt)
        self.device_name.setText("Name: "+ device.name)
        self.device_address.setText("Address: "+device.address)
        self.device_size.setText("Size: "+device.size+" Kb")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.multiline_text = MultiLineText()
        self.backup_button = self.create_backup_button()
        self.list_button = self.create_list_button()
        self.device_selection = self.create_device_selection()
        self.device_details = DeviceInfo()
        self.active_device = Device("", "No devices found", "", "")
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        button_bar = QVBoxLayout()

        main_layout.addWidget(self.multiline_text)
        button_bar.addWidget(self.list_button)
        button_bar.addWidget(self.device_selection)
        button_bar.addLayout(self.device_details)
        button_bar.addWidget(self.backup_button)

        main_layout.addLayout(button_bar)
        self.setLayout(main_layout)
        self.setGeometry(50, 50, 640, 400)
        self.setWindowTitle("DFU Flasher")
        self.show()

    def create_backup_button(self):
        button = QPushButton()
        button.setText("Backup device firmware")
        button.clicked.connect(self.backup_firmware)
        return button

    def create_list_button(self):
        button = QPushButton()
        button.setText("Scan for devices")
        button.clicked.connect(self.list_devices)
        return button

    def create_device_selection(self):
        combobox = QComboBox()
        combobox.addItem("No Devices found")
        combobox.activated[str].connect(self.change_device_selection)
        return combobox

    def list_devices(self):
        command_output = run_command(['sudo', 'dfu-util', '-l'])
        devices = re.findall('alt=(.*),.*name="(.*?)/(.*)/(.*)' + re.escape('*'), command_output)
        self.device_selection.clear()
        if not devices:
            devices.append(("", "No Devices Found", "", ""))
        for device in devices:
            new_device = Device(device[0], device[1], device[2], device[3])
            connected_devices.append(new_device)
            self.device_selection.addItem(new_device.name)
            self.device_details.set_device(new_device)
            self.device_selection.setCurrentIndex(self.device_selection.count()-1)
            self.active_device = new_device
        self.append_text(command_output)

    def append_text(self, text):
        self.multiline_text.setText(self.multiline_text.toPlainText() + text)
        self.multiline_text.moveCursor(QTextCursor.End)

    def backup_firmware(self):
        if not self.active_device.alt:
            self.append_text("::: No device selected for backup\n")
            return

        command_output = run_command(['sudo', 'dfu-util',
                                      '-a', self.active_device.alt,
                                      '-U', str(datetime.now())+'-backup.bin',
                                      '-s', self.active_device.address+':'+self.active_device.size*1024])
        print(command_output)
        self.append_text(command_output)

    def change_device_selection(self, value):
        selected_device = filter(lambda x: x.name == value, connected_devices)
        for device in selected_device:
            self.device_details.set_device(device)
            self.active_device = device


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
