"""Taller presencial"""
import os
import glob
import shutil
import re
from itertools import groupby


def copy_raw_files_to_input_folder(n):
    raw_files = glob.glob("files/raw/*.txt")
    os.makedirs("files/input", exist_ok=True)
    for file in raw_files:
        base = os.path.basename(file)
        name, ext = os.path.splitext(base)
        for i in range(1, n + 1):
            new_name = f"{name}_{i}{ext}"
            shutil.copy(file, os.path.join("files/input", new_name))


def load_input(input_directory):
    result = []
    for filepath in glob.glob(f"{input_directory}/*.txt"):
        with open(filepath, encoding="utf-8") as f:
            filename = os.path.basename(filepath)
            for line in f:
                result.append((filename, line.strip()))
    return result


def line_preprocessing(sequence):
    result = []
    for filename, line in sequence:
        cleaned = re.sub(r"[^\w\s]", "", line).lower()
        words = cleaned.split()
        result.extend([(word, 1) for word in words])
    return result


def mapper(sequence):
    return sequence


def shuffle_and_sort(sequence):
    return sorted(sequence, key=lambda x: x[0])


def reducer(sequence):
    result = []
    for key, group in groupby(sequence, key=lambda x: x[0]):
        total = sum(count for _, count in group)
        result.append((key, total))
    return result


def create_ouptput_directory(output_directory):
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory)


def save_output(output_directory, sequence):
    with open(os.path.join(output_directory, "part-00000"), "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")


def create_marker(output_directory):
    open(os.path.join(output_directory, "_SUCCESS"), "w").close()


def run_job(input_directory, output_directory):
    create_ouptput_directory(output_directory)
    data = load_input(input_directory)
    preprocessed = line_preprocessing(data)
    mapped = mapper(preprocessed)
    sorted_data = shuffle_and_sort(mapped)
    reduced = reducer(sorted_data)
    save_output(output_directory, reduced)
    create_marker(output_directory)
