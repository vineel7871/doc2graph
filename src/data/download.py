import os
import shutil
import requests
import zipfile
import json
import shutil
import wget
from src.utils import create_folder
from datasets import load_dataset
from uuid import uuid3
from pathlib import Path

from src.paths import CHECKPOINTS, DATA, DocLayNet_CACHE


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def funsd():
    print("Downloading FUNSD")

    dlz = DATA / 'funsd.zip'
    download_url("https://guillaumejaume.github.io/FUNSD/dataset.zip", dlz)
    with zipfile.ZipFile(dlz, 'r') as zip_ref:
        zip_ref.extractall(DATA)
    os.remove(dlz)
    os.rename(DATA / 'dataset', DATA / 'FUNSD')

    # adjusted annotations
    aa_train = os.path.join(DATA / 'adjusted_annotations.zip')
    wget.download(url="https://docs.google.com/uc?export=download&id=1cQE2dnLGh93u3xMUeGQRXM81tF2l0Zut", out=aa_train)
    with zipfile.ZipFile(aa_train, 'r') as zip_ref:
        zip_ref.extractall(DATA / 'FUNSD/training_data')
    os.remove(aa_train)

    aa_test = os.path.join(DATA / 'adjusted_annotations.zip')
    wget.download(url="https://docs.google.com/uc?export=download&id=18LXbRhjnkdsAvWBFhUdr7_44bfaBo0-v", out=aa_test)
    with zipfile.ZipFile(aa_test, 'r') as zip_ref:
        zip_ref.extractall(DATA / 'FUNSD/testing_data')
    os.remove(aa_test)

    # yolo_bbox
    yolo_train = os.path.join(DATA / 'yolo_bbox.zip')

    wget.download(url="https://docs.google.com/uc?export=download&id=1UzL5tYtBWDXk_nXj4KtoDMyBt7S3j-aS", out=yolo_train)
    with zipfile.ZipFile(yolo_train, 'r') as zip_ref:
        zip_ref.extractall(DATA / 'FUNSD/training_data')
    os.remove(yolo_train)

    yolo_test = os.path.join(DATA / 'yolo_bbox.zip')
    wget.download(url="https://docs.google.com/uc?export=download&id=1fWwbhfvINYFQmoPHpwlH8olyTyJPIe_-", out=yolo_test)
    with zipfile.ZipFile(yolo_test, 'r') as zip_ref:
        zip_ref.extractall(DATA / 'FUNSD/testing_data')
    os.remove(yolo_test)

    return


def pau():
    print("Downloading PAU")

    PAU = DATA / 'PAU'
    spl = os.path.join(DATA, 'pau_split.zip')
    wget.download(url="https://docs.google.com/uc?export=download&id=1NKlME13tRIDraSid7r3v_huTqFdHgo-G", out=spl)
    with zipfile.ZipFile(spl, 'r') as zip_ref:
        zip_ref.extractall(PAU)

    dlz = DATA / 'pau.zip'
    download_url("https://zenodo.org/record/3257319/files/dataset.zip", dlz)
    with zipfile.ZipFile(dlz, 'r') as zip_ref:
        zip_ref.extractall(PAU)

    create_folder(PAU / 'train')
    create_folder(PAU / 'test')
    create_folder(PAU / 'outliers')

    for split in ['train.txt', 'test.txt', 'outliers.txt']:
        with open(PAU / split, mode='r') as f:
            folder = split.split(".")[0]
            lines = f.readlines()
            for l in lines:
                l = l.rstrip('\n')
                src = PAU / l
                dst = PAU / '{}/{}'.format(folder, l)
                shutil.move(src, dst)

    os.remove(spl)
    os.remove(dlz)
    return


def doclaynet():
    docLayNet = DATA / "DocLayNet"
    create_folder(docLayNet)
    create_folder(DocLayNet_CACHE)
    dataset_large = load_dataset("pierreguillou/DocLayNet-base")

    create_folder(docLayNet / 'train')
    create_folder(docLayNet / 'train' / 'json')
    create_folder(docLayNet / 'train' / 'pdf')
    create_folder(docLayNet / 'train' / 'png')
    create_folder(docLayNet / 'validation')
    create_folder(docLayNet / 'validation' / 'json')
    create_folder(docLayNet / 'validation' / 'pdf')
    create_folder(docLayNet / 'validation' / 'png')
    create_folder(docLayNet / 'test')
    create_folder(docLayNet / 'test' / 'json')
    create_folder(docLayNet / 'test' / 'pdf')
    create_folder(docLayNet / 'test' / 'png')

    # print(dataset_large)

    PDF_PATH = Path(
        "/content/drive/MyDrive/data/DocLayNet/PDF")

    for k in dataset_large:
        for d in dataset_large[k]:
            if (PDF_PATH / (d["page_hash"] + ".pdf")).exists():
                # print(d.keys())

                image_content = d.pop("image")
                image_content.save(docLayNet / k / 'png' / (d["page_hash"] + ".png"))

                # pdf_content = d.pop("pdf")
                # with open(docLayNet / k / 'pdf' / (d["page_hash"]+".pdf", "wb")) as wb:
                #     wb.write(pdf_content)

                shutil.copyfile(PDF_PATH / (d["page_hash"] + ".pdf"), docLayNet / k / 'pdf' / (d["page_hash"] + ".pdf"))

                with open(docLayNet / k / 'json' / (d["page_hash"] + ".json"), "w") as w:
                    w.write(json.dumps(d))


def get_data():
    # funsd()
    # pau()
    doclaynet()
    return

