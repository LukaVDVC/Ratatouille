import os

class FileSearch:
    @staticmethod
    def search(filename, search_path="/"):
        result = []
        for root, dirs, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result

    @staticmethod
    def search_file(filename):
        return "\n".join(FileSearch.search(filename))
