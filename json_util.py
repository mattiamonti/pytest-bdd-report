"""
Utilities for loading data from and saving data to JSON files.

This module provides functions to facilitate the loading of data from JSON files into variables
and the saving of Python objects as JSON data into files.
"""
import json


def load_from_json(path: str):
    """
    Load data from a JSON file.

    Args:
        path (str): The path to the JSON file.

    Returns:
        The data from the JSON file as a list or dictionary,
        or an empty list if the file is not found
    """

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_to_json(data, path: str) -> None:
    """
    Save data to a JSON file.

    Args:
        data: The data to be saved to the JSON file.
        path (str): The path to the JSON file.
    """
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
