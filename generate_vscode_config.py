#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import os, sys, json

def getRelativePathToKeilProject(projectPath, keilProjectPath, path):
    return os.path.relpath(os.path.join(projectPath, "./" + keilProjectPath + "/" + path), projectPath)

def generateCCppPropertiesConfig(root, projectPath, keilProjectPath):
    # 创建json字典
    outputJSON = {
        "configurations": [
            {
                "name": "Keil",
                "includePath": [],
                "defines": [],
                "cStandard": "c99",
            }
        ],
        "version": 4
    }
    # 创建includepath
    includesPath = root.find("./Targets/Target/TargetOption/TargetArmAds/Cads/VariousControls/IncludePath")
    includesPath = includesPath.text.replace("\\", "/")
    includesPath = includesPath.split(";")
    for includePath in includesPath:
        includePath = includePath.strip()
        print("Include path:", includePath) 
        outputJSON["configurations"][0]["includePath"].append("${workspaceFolder}/" + getRelativePathToKeilProject(projectPath, keilProjectPath, includePath))
    # 创建define
    defines = root.find("./Targets/Target/TargetOption/TargetArmAds/Cads/VariousControls/Define")
    defines = defines.text.replace(" ", ",")
    defines = defines.split(",")
    defines = list(filter(None, defines))
    for define in defines:
        print("Define:", define)
        outputJSON["configurations"][0]["defines"].append(define)
    with open(os.path.join(path, "./.vscode/c_cpp_properties.json"), 'w') as file:
        json.dump(outputJSON, file, indent=4)

def generateWorkspsceConfig(root, projectPath, keilProjectPath):
    # 创建json字典
    outputJSON = {
        "folders": [],
        "settings": {}
    }
    srcGroups = root.findall("./Targets/Target/Groups/Group")
    for group in srcGroups:
        groupPath = ""
        groupName = group.find("GroupName")
        isGeneratePath = True
        print("Group:", group.find("GroupName").text, end=' ')
        for groupFile in group.findall("Files/File"):
            filePath = getRelativePathToKeilProject(projectPath, keilProjectPath, os.path.join(groupFile.find("FilePath").text.replace("\\", "/"), "../"))
            if groupPath == "":
                groupPath = filePath
            elif groupPath != filePath:
                print("The members in this src group aren't all in same directory!")
                isGeneratePath = False
                break
        if isGeneratePath:
            print("Generate path:", groupPath)
            outputJSON["folders"].append({
                "path": groupPath,
                "name": group.find("GroupName").text
            })
    with open(os.path.join(projectPath, "./keil.code-workspace"), 'w') as file:
        json.dump(outputJSON, file, indent=4)

def generateVSCodeConfig(path):
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
    # 创建.vscode文件夹
    try:
        os.mkdir(os.path.join(path, "./.vscode"))
    except FileExistsError:
        pass
    generateCCppPropertiesConfig(root, path, keilProjectPath)
    #generateWorkspsceConfig(root, path, keilProjectPath)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 ./generate_vscode_config.py [YOUR_KEIL_CODE_PATH]")
        exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(path, "not found! ")
        exit(1)
    generateVSCodeConfig(path)