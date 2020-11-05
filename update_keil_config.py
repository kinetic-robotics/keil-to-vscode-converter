#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import os, sys, json, re

def updateKeilConfig(path):
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
    # 修改目标文件名
    outputNames = root.findall("./Targets/Target/TargetOption/TargetCommonOption/OutputName")
    for outputName in outputNames:
        print("Target raw name:", outputName.text, end=' ')
        exts = outputName.text.split(".")
        if exts[-1] == "elf" and len(exts) > 1:
            print("The target name extension doesn't need to change!")
        else:
            newName = (exts[0] if len(exts) == 1 else outputName.text[0:-len(exts[-1]) - 1]) + ".elf"
            outputName.text = newName
            print("The target name changes to", newName, ".")
    # 打开输出bat选项
    print("Now enable all targets' batch output!")
    batOptions = root.findall("./Targets/Target/TargetOption/TargetCommonOption/CreateBatchFile")
    for batOption in batOptions:
        batOption.text = "1"
    root.write(keilConfigPath, xml_declaration=True)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 ./update_keil_config [YOUR_KEIL_CODE_PATH]")
        exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(path, "not found! ")
        exit(1)
    updateKeilConfig(path)