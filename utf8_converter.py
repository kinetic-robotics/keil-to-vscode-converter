#!/usr/bin/env python3

import os, sys, chardet

def covertFilesToUtf8(path):
    for root, dirs, files in os.walk(path):
        for fileName in files:
            # 只处理.c和.h
            if os.path.splitext(fileName)[-1] == ".c" or os.path.splitext(fileName)[-1] == ".h":
                filePathName = os.path.join(root, fileName)
                print("File:", filePathName, end=' ')
                with open(filePathName, 'rb') as file:
                    content = file.read()
                    codecs = chardet.detect(content)
                if codecs["confidence"] < 0.7:
                    print("Coding detection failed!")
                else:
                    print("Raw coding =", codecs["encoding"], end='')
                    if codecs["encoding"] != 'utf-8':
                        print(", now covert to utf-8")
                        with open(filePathName, 'wb') as file:
                            file.write(content.decode(codecs["encoding"], "ignore").encode("utf8"))
                    else:
                        print(", no need to covert")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 ./utf8_converter [YOUR_KEIL_CODE_PATH]")
        exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(path, "not found! ")
        exit(1)
    covertFilesToUtf8(path)