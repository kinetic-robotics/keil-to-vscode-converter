#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import os, sys, json

def getRelativePathToKeilProject(projectPath, keilProjectPath, path):
    return os.path.relpath(os.path.join(projectPath, "./" + keilProjectPath + "/" + path), projectPath)

def generateTasksConfig(path, cmd):
    # 创建json字典
    outputJSON = {
        "tasks": [
            {
                "label": "build",
                "type": "shell",
                "command": cmd,
                "problemMatcher": {
                    "owner": "armcc",
                    "pattern":[
                        {
                            "regexp": "^\"\\.(.*)\", line (\\d+): (Error|Warning|Info):  (.*): (.+)",
                            "file": 1,
                            "line": 2,
                            "severity": 3,
                            "code": 4,
                            "message": 5
                        }
                    ]
                }
            }
        ],
        "version": "2.0.0"
    }
    with open(os.path.join(path, "./.vscode/tasks.json"), 'w') as file:
        json.dump(outputJSON, file, indent=4)

def generateBuildConfig(path, targetName, systemName, vmName, windowsPath):
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
    targetName = targetElement.find("./TargetName").text
    # 创建.vscode文件夹
    try:
        os.mkdir(os.path.join(path, "./.vscode"))
    except FileExistsError:
        pass
    if systemName == "mac":
        windowsPath = windowsPath.replace("/", "\\")
        windowsPath = windowsPath.replace("\\","\\\\")
        cmd = "prlctl exec \"{}\" pd_keil_compile_tool.bat \"{}\"".format(vmName, windowsPath)
    else:
        batFileName = targetName.upper() + ".BAT"
        cmd = os.path.join("./", keilProjectPath, batFileName)
    print("Command:", cmd)
    generateTasksConfig(path, cmd)

def printUsage():
    print("Usage: python3 ./generate_build_config.py [YOUR_KEIL_CODE_PATH] [TARGET_NAME] [--mac | --windows] [VM_NAME] [WINDOWS_PROJECT_PATH]")

if __name__ == '__main__':
    if len(sys.argv) < 5:
        printUsage()
        exit(1)
    path = sys.argv[1]
    targetName = sys.argv[2]
    systemName = sys.argv[3][2:]
    vmName = sys.argv[4] if len(sys.argv) > 4 else ""
    windowsPath = sys.argv[5] if len(sys.argv) > 5 else ""
    if not os.path.exists(path):
        print(path, "not found! ")
        exit(1)
    if systemName != "mac" and systemName != "windows":
        printUsage()
        exit(1)
    if systemName == "mac" and (windowsPath == "" or vmName == ""):
        printUsage()
        exit(1)
    generateBuildConfig(path, targetName, systemName, vmName, windowsPath)