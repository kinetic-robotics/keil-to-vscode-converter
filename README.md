# Keil To Visual Studio Code Converter
Hate to use Keil but your project is based on Keil? Try me, I can help you get rid of Keil!  
This project can help you develop and debug your project using Visual Studio Code, and Keil is only used as a compiler!

# Requirements
- Visual Studio Code
    - Cortex-Debug Plugin
- Python 3
- Python Libraries
    - chardet
- For Windows User
    - Keil UVision 5
- For Mac User
    - Parallels Desktop
        - Windows VM
        - Keil Uvision 5


## Usage
Install requirements, and run
```
./utf8_converter.py [YOUR_KEIL_SOURCE_PROJECT]
./update_keil_config.py [YOUR_KEIL_SOURCE_PROJECT]
./generate_vscode_config.py [YOUR_KEIL_SOURCE_PROJECT]
./generate_cortex_debug_config.py [YOUR_KEIL_SOURCE_PROJECT] [TARGET_NAME] [DEBUG_MODE]
```
Then start Keil, run `Build All`, wait for completion.
### For Windows User
```
./generate_build_config.py [YOUR_KEIL_SOURCE_PROJECT] [TARGET_NAME] --windows
```

### For OS X User
Copy `pd_keil_compile_tool.bat` to `C:\Windows\System32` of your Parallels Desktop VM, and run this.  
More information about how to use this script, please see [this]().  
```
./generate_build_config.py [YOUR_KEIL_SOURCE_PROJECT] [TARGET_NAME] --mac [VM_NAME] [WINDOWS_PROJECT_PATH],
```
Then start your experience!

# Commands
- utf8_converter.py: Because the default codeset of Keil isn't utf8, but vscode uses utf8 as its default codeset, so we need to convert.
    - YOUR_KEIL_SOURCE_PROJECT: The path of your Keil project
- update_keil_config.py: Update some Keil Project Configurations, such as open `Creat Batch File` and rename the target output name to generate `.elf` file.
    - YOUR_KEIL_SOURCE_PROJECT: The path of your Keil project
- generate_vscode_config.py: This script will generate C config and auto build config, this parameters will be parsed from Keil project.
    - YOUR_KEIL_SOURCE_PROJECT: The path of your Keil project
- generate_cortex_debug_config.py: This script will generate Cortex-Debug Plugin configurations.
    - YOUR_KEIL_SOURCE_PROJECT: The path of your Keil project
    - TARGET_NAME: The name of your Keil target. Can be "" to select the first target.
    - DEBUG_MODE: The transport mode when download program. Can be `swd` or `jtag`.
- generate_build_config.py: This script will generate build config.
    - YOUR_KEIL_SOURCE_PROJECT: The path of your Keil project
    - TARGET_NAME: The name of your Keil target. Can be "" to select the first target.
    - SYSTEM: The third parameters. Can be `--mac` or `--windows`
    - VM_NAME: The name of Parallels Desktok Virual Machine.
    - WINDOWS_PROJECT_PATH: This parameter is only used when `SYSTEM` == `mac`. Should be the path of Keil project under windows vm, if the project is under the virual home disk(Mapping to OS X's Home Direcrory) Parallels Desktop created, uses `X:` instead of its drive letter. For example, my home disk letter is `Y:`, and my project is under `Y:\Downloads\test`, so I need to use `X:\Downloads\test` to instead of using its raw path.
