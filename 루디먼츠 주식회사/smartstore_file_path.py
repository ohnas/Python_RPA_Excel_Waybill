import pickle
import os

# pickle 라이브러리를 사용하여 저장경로를 임시저정하고 프로그램이 종료되어도 프로그램에서 받았던 값을 pickle 파일에 저장해두고 ,
# 프로그램 재시작할 때 전에 저장해놓았던 경로를 다시 보여줄 수 있게 만들기


def row_file_new_path(path):
    with open("row_file.pickle", "wb") as file:
        pickle.dump(path, file)


def row_file_saved_path():
    # os 모듈에서 exists를 사용하여 파일 존재 여부를 확인하기
    if os.path.exists("row_file.pickle") == False:
        data = "C:\\"
        with open("row_file.pickle", "wb") as file:
            pickle.dump(data, file)
        with open("row_file.pickle", "rb") as file:
            file_path = pickle.load(file)
    else:
        with open("row_file.pickle", "rb") as file:
            file_path = pickle.load(file)
    return file_path


def sample_file_new_path(path):
    with open("sample_file.pickle", "wb") as file:
        pickle.dump(path, file)


def sample_file_saved_path():
    # os 모듈에서 exists를 사용하여 파일 존재 여부를 확인하기
    if os.path.exists("sample_file.pickle") == False:
        data = "C:\\"
        with open("sample_file.pickle", "wb") as file:
            pickle.dump(data, file)
        with open("sample_file.pickle", "rb") as file:
            file_path = pickle.load(file)
    else:
        with open("sample_file.pickle", "rb") as file:
            file_path = pickle.load(file)
    return file_path


def waybill_file_new_path(path):
    with open("waybill_file.pickle", "wb") as file:
        pickle.dump(path, file)


def waybill_file_saved_path():
    # os 모듈에서 exists를 사용하여 파일 존재 여부를 확인하기
    if os.path.exists("waybill_file.pickle") == False:
        data = "C:\\"
        with open("waybill_file.pickle", "wb") as file:
            pickle.dump(data, file)
        with open("waybill_file.pickle", "rb") as file:
            file_path = pickle.load(file)
    else:
        with open("waybill_file.pickle", "rb") as file:
            file_path = pickle.load(file)
    return file_path
