"""
To store states in file ( simple solution for development purposes )
"""


import logging


class Write:
    
    def write_state(self, body: list, file: str):
        """
        Get's an array of IDs and overwrites them on the file.
        """
        with open(file, "w+") as f:
            for line in body:
                logging.info(f"writing {line} in state...")
                f.write(line + "\n")

class Read:
    def read_state(self, file: str) -> list:
        """
        Returns a list of IDs (states)
        """
        with open(file, "r") as f:
            return f.readlines()
