from bs4 import BeautifulSoup
import markdown
import base64
import os
import re


class MarkdownReader:

    def decodePath(self, path = ""):
        """
        It takes a string, encodes it to ascii, then decodes it from base64 to ascii
        
        :param path: The path to the file you want to read
        :return: The path is being returned.
        """
        path = path.encode("ascii")
        return base64.b64decode(path).decode("ascii")

    def __init__(self, path = ""):
        self.global_path = path

    def __find_index(self, arr=[], query=""):
        """
        It takes an array of objects and a query string, and returns the index of the object in the array
        whose name property matches the query string

        :param arr: The array to search through
        :param query: The query string to search for
        :return: The index of the item in the array that matches the query.
        """
        for i, v in enumerate(arr):
            if v["name"] == query:
                return i
        return 0

    def listData(self):
        """
        It walks through the directory, and creates a list of dictionaries, each dictionary representing a
        folder or file

        :param path: The path to the directory you want to list
        :return: list of dictionary
        """
        data = []
        list_folder = []
        # listing folder
        for root, dirs, _ in os.walk(self.global_path, topdown=True):
            for d in dirs:
                context = {
                    "name": d,
                    "type": "folder",
                    "file": []
                }
                split_path = os.path.join(root, d).split("/")
                if len(split_path) <= 3 and d not in list_folder:
                    list_folder.append(d)
                    data.append(context)

        # listing file
        for root, dirs, files in os.walk(self.global_path, topdown=True):
            for f in files:
                file_path = os.path.join(root, f)
                split = file_path.split("/")

                # looking for files's folder name
                if len(split) > 3:
                    folder_name = file_path.split("/")[2]

                    # find data by spesific value on list of dictionary
                    index = self.__find_index(data, folder_name)

                    # make sure just markdown file that included
                    if f.split(".")[-1].lower() == "md":
                        data[index]['file'].append({
                            "name": f,
                            "path": base64.b64encode(os.path.join(root, f).encode("utf-8")).decode("ascii")
                        })

                # if there's no file inside folder the file will store to list of data
                elif len(split) > 2 and len(split) < 4:

                    if split[2].split(".")[-1].lower() == "md":
                        data.append({
                            "name": split[2],
                            "type": "file",
                            "path": base64.b64encode(os.path.join(root, f).encode("utf-8")).decode("ascii"),
                            "file": []
                        })
        return data
    

    def getHeadline(self, file):
        """
        It takes a file, reads it line by line, and if it finds a markdown headline, it appends it to a list

        :param file: the file you want to parse
        :return: A list of headlines
        """
        headlines = []

        with open(file) as f:
            file_read = f.readlines()
            for line in file_read:

                markdown_html = markdown.markdown(line)
                soup = BeautifulSoup(markdown_html, "html.parser")

                if len(re.findall("<h1>", markdown_html)) > 0:

                    headlines.append(soup.get_text())

                elif len(re.findall("<h2>", markdown_html)) > 0:

                    headlines.append(soup.get_text())

                elif len(re.findall("<h3>", markdown_html)) > 0:

                    headlines.append(soup.get_text())

                elif len(re.findall("<h4>", markdown_html)) > 0:

                    headlines.append(soup.get_text())

                elif len(re.findall("<h5>", markdown_html)) > 0:

                    headlines.append(soup.get_text())

                elif len(re.findall("<h6>", markdown_html)) > 0:

                    headlines.append(soup.get_text())

                else:
                    pass

        return headlines

    def readMarkdown(self, path = ""):
        """
        > This function reads a markdown file and returns the markdown as HTML

        :param path: The path to the file you want to read
        :return: The readMarkdown function is returning the read variable.
        """

        try:
            if os.path.exists(path):
                with open(path) as files:
                    read = markdown.markdown(files.read())
                return read
            else:
                return ""
        except:
            return ""

    def search(self, query):
        """
        > It takes a query, searches through all the files in the directory, and returns the path of the
        file with the highest score
        
        :param query: The query string to search for
        :return: The path of the file that has the highest score.
        """

        data = self.listData()
        result_score = []
        result_path = []

        for d in data:

            global_score = 0
            global_path = ''

            # read file inside the folder
            if d['type'] == "folder":

                score = []
                path = []
                for f  in d['file']:
                    file = self.decodePath(f['path'])

                    with open(file, "r") as r:
                        read = r.read()
                        soup = BeautifulSoup(markdown.markdown(read), "html.parser").get_text()
                        score.append(len(re.findall(query, soup)))
                        path.append(self.decodePath(f['path']))
                        r.close()
                
                global_score = score[score.index(max(score))]
                global_path = path[score.index(max(score))]

            else:

                file_score = []
                file_path = []

                with open(self.decodePath(d['path']), "r") as r:
                    read = r.read()
                    soups = BeautifulSoup(markdown.markdown(read), "html.parser").get_text()
                    file_score.append(len(re.findall(query, soups)))
                    file_path.append(self.decodePath(d['path']))
                    r.close()

                global_score = file_score[file_score.index(max(file_score))]
                global_path = file_path[file_score.index(max(file_score))]

            result_score.append(global_score)
            result_path.append(global_path)

        return result_path[result_score.index(max(result_score))]