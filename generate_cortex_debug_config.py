#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import os, sys, json, re, shutil

def getRelativePathToKeilProject(projectPath, keilProjectPath, path):
    return os.path.relpath(os.path.join(projectPath, "./" + keilProjectPath + "/" + path), projectPath)

def generateCMSISDAPConfig(targetElement, path, keilProjectPath, debugMode):
    # 获取设备类型
    deviceType = targetElement.find("./TargetOption/TargetCommonOption/PackID").text
    deviceType = deviceType[5:13].lower()
    print("Device type:", deviceType)
    with open("./cmsis-dap.cfg", "r") as file:
        configContent = file.read()
    configContent = configContent.replace("{DEBUG_MODE}", debugMode)
    configContent = configContent.replace("{DEVICE_TYPE}", deviceType)
    with open(os.path.join(path, keilProjectPath, "cmsis-dap.cfg"), 'w') as file:
        file.write(configContent)
    

def generateCortexDebugConfig(targetElement, path, keilProjectPath, debugMode):
    # 创建json字典
    outputJSON = {
        "version": "0.2.0",
        "configurations": [
            {
                "cwd": "",
                "executable": "",
                "name": "Debug (OpenOCD)",
                "request": "launch",
                "type": "cortex-debug",
                "servertype": "openocd",
                "svdFile": "",
                "device": "",
                "preLaunchTask": "build"
            },
            {
                "cwd": "",
                "executable": "",
                "name": "Debug (CMSIS-DAP)",
                "request": "launch",
                "type": "cortex-debug",
                "servertype": "openocd",
                "svdFile": "",
                "device": "",
                "configFiles": [
                    "cmsis-dap.cfg"
                ],
                "preLaunchTask": "build"
            },
            {
                "cwd": "",
                "executable": "",
                "name": "Debug (J-Link)",
                "request": "launch",
                "type": "cortex-debug",
                "servertype": "jlink",
                "svdFile": "",
                "device": "",
                "preLaunchTask": "build",
            },
            {
                "cwd": "",
                "executable": "",
                "name": "Debug (ST-Link)",
                "request": "launch",
                "type": "cortex-debug",
                "servertype": "stutil",
                "svdFile": "",
                "device": "",
                "preLaunchTask": "build"
            },
        ]
    }
    relativeOutputDirectory = targetElement.find("./TargetOption/TargetCommonOption/OutputDirectory").text
    relativeOutputDirectory = relativeOutputDirectory.replace("\\", "/")
    relativeOutputName = targetElement.find("./TargetOption/TargetCommonOption/OutputName").text
    relativeOutputName = relativeOutputName.replace("\\", "/")
    relativeOutputPath = os.path.join(relativeOutputDirectory, relativeOutputName)
    print("ELF Path:", relativeOutputPath)
    # 读取svd文件名称
    svdFileName = targetElement.find("./TargetOption/TargetCommonOption/SFDFile").text
    svdFileName = svdFileName[svdFileName.rfind("\\") + 1:]
    svdFilePath = os.path.join("./svd", svdFileName)
    print("SVD name:", svdFileName)
    if not os.path.exists(svdFilePath):
        print("SVD file not found, please download it from your mcu website and put it into", svdFilePath)
        return
    # 读取device id
    deviceID = targetElement.find("./TargetOption/TargetCommonOption/Device").text
    deviceID = deviceID[0:-2]
    print("Device id:", deviceID)
    # 拷贝svd文件
    shutil.copyfile(svdFilePath, os.path.join(path, keilProjectPath, svdFileName))
    for config in outputJSON["configurations"]:
        config["cwd"] = "${workspaceRoot}/" + keilProjectPath
        config["executable"] = relativeOutputPath
        config["svdFile"] = os.path.join(svdFileName)
        config["device"] = deviceID

    with open(os.path.join(path, "./.vscode/launch.json"), 'w') as file:
        json.dump(outputJSON, file, indent=4)



def generateDebugConfig(path, targetName, debugMode):
    # 绝对路径keil配置文件路径
    keilConfigPath = ""
    # 相对path而言的keil项目配置文件
    keilProjectPath = ""
    # 搜索Keil配置文件
    for root, dirs, files in os.walk(path):
        for fileName in files:
            if os.path.splitext(fileName)[-1] == ".uvprojx":
                keilProjectPath = os.path.relpath(root, path)
                keilConfigPath = os.path.join(root, fileName)
    if keilConfigPath == "" or keilProjectPath == "":
        print("Failed to find keil config!")
        return
    root = ET.parse(keilConfigPath)
    # 寻找指定的target
    targets = root.findall("./Targets/Target")
    targetElement = None
    for target in targets:
        if targetName == "" or target.find("./TargetName").text == targetName:
            targetElement = target
            break
    if targetElement == None:
        if targetName != "":
            print("Target:", targetName, "not found!")
        else:
            print("No target found!")
        return
    # 创建.vscode文件夹
    try:
        os.mkdir(os.path.join(path, "./.vscode"))
    except FileExistsError:
        pass
    generateCortexDebugConfig(targetElement, path, keilProjectPath, debugMode)
    generateCMSISDAPConfig(targetElement, path, keilProjectPath, debugMode)

def printUsage():
    print("Usage: python3 ./generate_cortex_debug_config.py [YOUR_KEIL_CODE_PATH] [TARGET_NAME] [DEBUG_MODE]")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        printUsage()
        exit(1)
    path = sys.argv[1]
    targetName = sys.argv[2]
    debugMode = sys.argv[3]
    if debugMode != "swd" and debugMode != "jtag":
        printUsage()
        exit(1)
    if not os.path.exists(path):
        print(path, "not found! ")
        exit(1)
    generateDebugConfig(path, targetName, debugMode)