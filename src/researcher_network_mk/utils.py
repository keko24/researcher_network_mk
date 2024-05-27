import os
import json

from pathlib import Path

def get_project_root():
    return Path(__file__).parent.parent.parent

def get_researcher_paths():
    path = os.path.join(get_project_root(), "data", "researchers_names")
    return [(os.path.join(path, file), file[:-4]) for file in os.listdir(path) if not file.startswith(".")]

def save_coauthors(faculty, researcher_name, coauthors):
    path = os.path.join(get_project_root(), "data", "researchers_stats", faculty)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "_".join(researcher_name.split(" ")) + ".json"), "w") as f:
        json.dump(coauthors, f, indent=4)
