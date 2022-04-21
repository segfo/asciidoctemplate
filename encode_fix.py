from importlib.resources import path
import os
import urllib.parse


def isExt(path, expect_ext_list):
    norm_path = os.path.normpath(path)
    os.path.isfile(norm_path)
    _, actual_ext = os.path.splitext(norm_path)
    for expect_ext in expect_ext_list:
        if actual_ext.endswith(expect_ext):
            return True
    return False


def decodeUrlEncodeList(strList):
    result = []
    for string in strList:
        result.append([string, urllib.parse.unquote(string)])
    return result


def specifyFilePathResolve(basePath, extList, recursive=False):
    # if recursive:
    if recursive:
        result = []
        for path, dirList, fileList in os.walk(basePath):
            result[len(result):len(result)] = list(map(lambda file: os.path.normpath(
                os.path.join(path, file)), fileList))
        result = list(filter(lambda path: isExt(path, extList), result))
        return result
    else:
        return [f for f in os.listdir(basePath) if isExt(
            os.path.join(basePath, f), extList)]


imagePathList = ["images"]
asciidocExtList = ["adoc"]
asciidocPathList = ["./"]
imageExtList = ["png"]

encodedImagePathList = []

for imagePath in imagePathList:
    encodedImagePathList.append([imagePath, decodeUrlEncodeList(
        specifyFilePathResolve(imagePath, imageExtList))])

print(encodedImagePathList)

# adocの書き換え
for adocPath in asciidocPathList:
    filePathList = specifyFilePathResolve(
        adocPath, asciidocExtList, recursive=True)
    for file in filePathList:
        with open(file, "r") as fp:
            buf = fp.read()
            for encodedImagePathes in encodedImagePathList:
                for encodedImagePath in encodedImagePathes[1]:
                    buf = buf.replace(encodedImagePath[0], encodedImagePath[1])
        with open(file, "w") as fp:
            fp.write(buf)

# imagesの書き換え
for encodedImagePathes in encodedImagePathList:
    pathBase = encodedImagePathes[0]
    for encodedImagePath in encodedImagePathes[1]:
        old = os.path.join(pathBase, encodedImagePath[0])
        new = os.path.join(pathBase, encodedImagePath[1])
        os.rename(old, new)
