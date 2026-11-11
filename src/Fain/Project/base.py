class Project:
    def __init__(self, project_name):
        self.name = project_name    
        self.categories = ["audio", "config", "inter", "output", "sprites","script"]
        self.fs = FileStorageService()
        self.path = PathService()
        self.setup_folders()
    
    def setup_folders(self):
        _project = self.path.get_pfolder(self.name)
        self.fs.create_directory(_project)
        for catergory in self.categories:
            _subpath = self.path.get_psubfolder(self.name, catergory)
            self.fs.create_directory(_subpath)
        
    def upload_sprite(self, path):  
        _dest = self.path.get_psubfolder(self.name, "sprites")
        self.fs.copy_file(path, _dest)

def main():
    p = Project("test")
    p.upload_sprite("C:\\Users\\Franklin\\Downloads\\wolfsheet1.png")
    
    ...

if __name__ == "__main__":
    main()