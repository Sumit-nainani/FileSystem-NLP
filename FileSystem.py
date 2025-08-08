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
            if isinstance(file_creation_date, (list, tuple)):
                file_creation_date_match = self.file_creation_date in file_creation_date
            else:
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
   
def makeFileSystem():

    # Files
    f1 = FileClass("User.java", "15/07/2023")
    f2 = FileClass("FinanceReport.xlsx", "10/06/2023")
    f3 = FileClass("Test.java", "12/08/2023")
    f4 = FileClass("notes.txt", "15/07/2023")
    f5 = FileClass("main.cpp", "01/01/2023")
    f6 = FileClass("project.csv", "05/03/2023")
    f7 = FileClass("readme.txt", "11/07/2023")
    f8 = FileClass("budget.csv", "20/06/2023")
    f9 = FileClass("helper.cpp", "08/05/2023")
    f10 = FileClass("UserGuide.txt", "22/07/2023")
    f11 = FileClass("Setup.java", "02/07/2023")
    f12 = FileClass("data.csv", "30/06/2023")
    f13 = FileClass("Summary.txt", "15/08/2023")
    f14 = FileClass("Algorithm.cpp", "05/05/2023")
    f15 = FileClass("oldnotes.txt", "21/01/2023")
    f16 = FileClass("TestUser.java", "18/07/2023")
    f17 = FileClass("InstallGuide.txt", "28/06/2023")
    f18 = FileClass("DownloadsList.csv", "03/04/2023")
    f19 = FileClass("CV_JohnDoe.pdf", "10/09/2023")
    f20 = FileClass("Presentation.java", "12/06/2023")

    # Directories
    root = DirectoryClass("root")
    src = DirectoryClass("src")
    docs = DirectoryClass("docs")
    desktop = DirectoryClass("Desktop")
    downloads = DirectoryClass("Downloads")
    projects = DirectoryClass("projects")
    archives = DirectoryClass("archives")
    cpp_projects = DirectoryClass("cpp_projects")
    java_projects = DirectoryClass("java_projects")
    text_files = DirectoryClass("text_files")

    # Root level directories
    root.add(desktop)
    root.add(downloads)
    root.add(docs)
    root.add(src)

    # Desktop
    desktop.add(f19)  
    desktop.add(f17)  
    desktop.add(text_files)

    # Text files folder inside Desktop
    text_files.add(f4)   
    text_files.add(f13)  
    text_files.add(f15)  
    text_files.add(f10)  

    downloads.add(f18)  
    downloads.add(f2)   

    # Docs
    docs.add(f12)  
    docs.add(f8)   
    docs.add(archives)

    # Archives inside Docs
    archives.add(f7)  
    archives.add(f20)  

    # Src
    src.add(f1)  
    src.add(f3)  
    src.add(f11) 
    src.add(projects)

    # Projects inside src
    projects.add(java_projects)
    projects.add(cpp_projects)

    # Java projects
    java_projects.add(f16)  

    # Cpp projects
    cpp_projects.add(f5)   
    cpp_projects.add(f9)   
    cpp_projects.add(f14)  

    return root


