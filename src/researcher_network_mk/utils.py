import os
import logging
import sys
import json

from pathlib import Path

def load_json(path) -> dict | None:
    if os.path.exists(path) and path.endswith(".json"):
        with open(path, "r") as f:
            data = json.load(f)
            return data
    else:
        raise ValueError("Invalid path")

def get_project_root():
    return Path(__file__).parent.parent.parent

def get_logger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="scholar_scraper.log", encoding="utf-8", level=logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_researcher_paths():
    data = {} 
    path = os.path.join(get_project_root(), "data", "researchers")
    universities = [university for university in os.listdir(path) if os.path.isdir(os.path.join(path, university))]
    for university in universities:
        data[university] = [(faculty, os.path.join(path, university, faculty, "researchers.csv")) for faculty in os.listdir(os.path.join(path, university)) if os.path.isdir(os.path.join(path, university, faculty))]
    return data

def save_publications(publications, university, faculty, researcher_name):
    path = os.path.join(get_project_root(), "data", "researchers", university, faculty, "publications")
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "_".join(researcher_name.split(" ")) + ".json"), "w") as f:
        json.dump(publications, f, indent=4)

def save_coauthors(faculty, researcher_name, coauthors):
    path = os.path.join(get_project_root(), "data", "researchers_stats", faculty)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "_".join(researcher_name.split(" ")) + ".json"), "w") as f:
        json.dump(coauthors, f, indent=4)

def list_universities():
    researchers_path = os.path.join(get_project_root(), "data", "researchers")
    return [university for university in os.listdir(researchers_path) if os.path.isdir(os.path.join(researchers_path, university))]

def list_faculties(university):
    university_path = os.path.join(get_project_root(), "data", "researchers", university)
    return [faculty for faculty in os.listdir(university_path) if os.path.isdir(os.path.join(university_path, faculty))]

def list_researchers(university, faculty):
    university_path = os.path.join(get_project_root(), "data", "researchers", university, faculty, "publications")
    return [researcher for researcher in os.listdir(university_path) if researcher.endswith(".json")]
