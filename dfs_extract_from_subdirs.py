from genericpath import isdir
import os
from collections import deque
import subprocess

##########################################################################################################

"""All you have to do is change these 5 globals and run the file"""

root = '/mnt/c/Users/moses/OneDrive/Desktop/python_projects/official_transcriptions'
dest = '/mnt/c/Users/moses/OneDrive/Desktop/python_projects/all_ot'
fnames = None
action = None

##########################################################################################################

class dfs_extractor:
    """A class that follows a depth-first pattern to move or copy files of a certain
    name and extension from subdirectories of a root directory into the destination directory.

    Call the constructor with the desired arguments, then call the "extract" method to carry out the extraction.
    
    ***WARNING: ANY ACTIONS PERFORMED WITH THIS SCRIPT ARE IRREVERSIBLE***
    ***CONSIDER MAKING A BACKUP OF ANY DATA, OR USING "COPY" INSTEAD OF "MOVE"***

    Attributes:
        root: the directory in which to start (defaults to current directory)
        dest: the location to which files are to be copied (defaults to root)
        fnames: a list of strings of wildcard expressions specifying what files to affect (defaults to ["*"])
        action: either "copy" or "move" (defaults to "copy")
        flags: a string containing any flags to be passed to the command
        stack: a stack used for the DFS
        """

    def __init__(self, root=None, dest=None, fnames=None, action="copy"):
        """Initializes class parameters from given arguments"""

        # Sets root as current directory if no argument is given
        if root == None:
            self.root = os.getcwd()
        else:
            self.root = root

        # Sets dest as root if no argument is given
        if dest == None:
            self.dest = self.root
        else:
            self.dest = dest

        # Sets fnames to default wildcard (which will move all files) if no argument is given
        if fnames == None:
            self.fnames = ["*"]
        else:
            self.fnames = fnames

        # Sets action to either "cp" or "mv" based on input (default is "cp"), or raises ValueError for bad input
        if action in ["copy", "cp", "c", None]:
            self.action = "cp"
        elif action in ["move", "mv", "m"]:
            self.action = "mv"
        else:
            raise ValueError(f"Argument \"action\" takes as input \"copy\" or \"move\", not {action}")

        self.stack = deque()


    def extract(self):
        """Carries out the extraction"""

        def _recurse(curr_path):
            """Continues searching recursively"""

            # Push all children onto stack
            for item in os.listdir(curr_path):
                if isdir(item):
                    self.stack.append(curr_path + "/" + item)

            # Move all files matching wildcard expr. to dest directory
            for exp in self.fnames:
                try:
                    assert os.system(f"{self.action} {curr_path}/{exp} {self.dest}") == 0
                except AssertionError:
                    # If command fails (exit code other than 0), print error message and move on
                    #print(f"{e.cmd} failed with exit code {e.returncode}, please double check expression is valid.")
                    pass
            

        self.stack.append(self.root)

        # Pop first item off stack
        while len(self.stack) != 0:
            item = self.stack.pop()
            _recurse(item)
        return


if __name__ == "__main__":
    extractor = dfs_extractor(root, dest, fnames, action)
    extractor.extract()
