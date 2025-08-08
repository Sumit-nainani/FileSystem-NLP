from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


class FileSystem(ABC):
    @abstractmethod
    def ls(self, path: str = "") -> List[str]:
        pass

class DirectoryClass(FileSystem):
    def __init__(self, name: str):
        self.name = name
        self.contents: List[FileSystem] = []

    def add(self, f: FileSystem):
        self.contents.append(f)

    def ls(self, file_extensions: List[str], file_creation_date: Optional[str], file_keywords: List[str], path: str = "") -> List[str]:
        matched_files = []
        current_path = path + self.name + "/"
        for f in self.contents:
            matched_files.extend(f.ls(file_extensions, file_creation_date, file_keywords, current_path))
        return matched_files
    
    def find_dir(self, target_path: str, current_path: str = "") -> Optional["DirectoryClass"]:
        full_path = current_path + self.name
        if full_path == target_path.rstrip("/"):
            return self
        new_path = full_path + "/"
        for f in self.contents:
            if isinstance(f, DirectoryClass):
                res = f.find_dir(target_path, new_path)
                if res:
                    return res
        return None
        
class FileClass(FileSystem):
    def __init__(self, file_name: str, file_creation_date: Optional[str]):
        self.file_name = file_name
        self.file_creation_date = file_creation_date

    def ls(self, file_extensions: List[str], file_creation_date: Optional[str], keywords: List[str], path: str = "") -> List[str]:

        # Checking file extension match
        file_extension_match = False
        if file_extensions:
            for extension in file_extensions:
                if self.file_name.lower().endswith(extension.lower()):
                    file_extension_match = True
                    break
        else:
            file_extension_match = True

        # Checking creation date match , if created_at is None , accepting all
        file_creation_date_match = True
        if file_creation_date:
            file_creation_date_match = (self.file_creation_date == file_creation_date)

        # Checking keywords match in file name
        keyword_match = True
        if keywords:
            lower_name = self.file_name.lower()
            keyword_match = any(kw.lower() in lower_name for kw in keywords)

        if file_extension_match and file_creation_date_match and keyword_match:
            return [path + self.file_name]
        else:
            return []
   
def makeFileSysytem() -> DirectoryClass:
    # Create some files
    f1 = FileClass("User.java", "15/07/2023")
    f2 = FileClass("FinanceReport.xlsx", "10/06/2023")
    f3 = FileClass("Test.java", "12/08/2023")
    f4 = FileClass("notes.txt", "15/07/2023")

    # Create directories and build structure
    root = DirectoryClass("root")
    src = DirectoryClass("src")
    docs = DirectoryClass("docs")

    src.add(f1)
    src.add(f3)
    docs.add(f2)
    docs.add(f4)

    root.add(src)
    root.add(docs)

    return root