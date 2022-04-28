import base64
from core import MarkdownReader
import os

doc_path = "./documents"
mr = MarkdownReader(doc_path)
file_list = mr.listData()

class ReaderController:

    def dataHome(self):
        """
        It takes the file list and returns a context dictionary with the initial file, the initial headline,
        and the file list
        :return: The context is being returned.
        """
        file_init = ""
        if len(file_list) > 0:
            if file_list[0]['type'] == "folder":
                file_init = mr.decodePath(file_list[0]['file'][0]['path'])
            else:
                file_init = mr.decodePath(file_list[0]['path'])
            
        context = {
            'file_init': mr.readMarkdown(file_init),
            'headline_init': mr.getHeadline(file_init),
            'data': file_list
        }

        return context

    def readFileInFolder(self, path = ""):
        """
        It reads the file in the folder and returns the context
        
        :param folder: the folder name in the doc_path folder
        :param file: the file name
        :return: A dictionary with the following keys:
            - file_init: the markdown file read
            - headline_init: the headlines of the markdown file
            - data: the file list
            - title: the title of the markdown file
        """
        file_read = ""
        path = mr.decodePath(path)

        file_read = mr.readMarkdown(path)
        headline = mr.getHeadline(path)

        context = {
            'file_init': file_read,
            'headline_init': headline,
            'data': file_list,
            'title': path.split("/")[-1].split(".")[0]
        }

        return context


    def readSingleFile(self, path = ""):
        """
        It reads a single file and returns the file content and headline
        
        :param filename: the name of the file to be read
        :return: A dictionary with the file content, the headlines, the file list and the title of the file.
        """
        headline = []
        path = mr.decodePath(path)
        file = mr.readMarkdown(path)
        headline = mr.getHeadline(path)

        context = {
            'file_init': file,
            'headline_init': headline,
            'data': file_list,
            'title': path.split("/")[-1].split(".")[0]
        }

        return context

    def search(self, query):
        """
        It searches for a file that contains the query, reads the file, gets the headline, and returns the
        file, headline, and file list
        
        :param query: The search query
        :return: The context is being returned.
        """

        founded_file = mr.search(query)
        file = mr.readMarkdown(founded_file)
        headline = mr.getHeadline(founded_file)

        context = {
            'file_init': file,
            'headline_init': headline,
            'data': file_list,
            'title': founded_file.split("/")[-1].split(".")[0]
        }

        return context


if __name__ != "__main__":

    reader_controller = ReaderController()