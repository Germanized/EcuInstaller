# Minecraft Essential Unlocker Mod Installer
original github where mod is located https://github.com/dxxxxy/EssentialCosmeticsUnlocker

This is a Python-based GUI application using PyQt5 designed to help users install Minecraft mods easily. Specifically, it handles the installation of the Essential Mod and ECU-1.4.0.jar file into the Minecraft directory.

## Features

- **User-friendly GUI**: Intuitive interface with drag-to-move functionality.
- **File Browsing**: Browse and select `ecu-1.4.0.jar` and the Essential Mod JAR files.
- **Automatic Download**: Downloads `ecu-1.4.0.jar` from a predefined URL if not provided.
- **Install Mods**: Copies selected JAR files to the appropriate Minecraft directories.

## Installation

To use this application, follow these steps:

1. **Clone the Repository**:
git clone https://github.com/Germanized/EcuInstaller.git


2. **Navigate to the Directory**:
cd EcuInstaller


3. **Install Dependencies**:
Ensure you have Python and PyQt5 installed. If not, install them using:
pip install PyQt5


4. **Run the Application or PY if you dont trust the exe**:


## How to Use

1. **Open the Application**: Run the `main.py` script to launch the GUI.

2. **Select JAR Files**:
- Click on **Browse for ecu-1.4.0.jar** to select the ECU JAR file.
- Click on **Browse for Essential Mod** to select the Essential Mod JAR file.

3. **Choose Minecraft Directory**:
- Click **Install Mods** and select your Minecraft directory. The script will create necessary folders and copy the JAR files.

4. **Automatic Download**:
If the `ecu-1.4.0.jar` file is not provided, it will be downloaded from [this URL](https://github.com/dxxxxy/EssentialCosmeticsUnlocker/releases/download/1.4.0/ecu-1.4.0.jar).

5. **Completion**:
A success message will appear once the mods are installed.

## Credits

**[Germanized](https://github.com/Germanized)**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Note**: Ensure you have Python installed and that PyQt5 is correctly set up in your environment to run this application. For any issues, please refer to the [PyQt5 documentation](https://www.riverbankcomputing.com/software/pyqt/intro) for troubleshooting.

