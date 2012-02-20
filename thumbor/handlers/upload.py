#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/globocom/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com timehome@corp.globo.com

from os.path import exists

from thumbor.handlers import ContextHandler

class UploadHandler(ContextHandler):

    def write_file(self, filename, body, overwrite):
        storage = self.context.modules.original_photo_storage
        path = storage.resolve_original_photo_path(filename)
        normalized_path = storage.normalize_path(path)

        if not overwrite and exists(normalized_path):
            raise RuntimeError('File already exists.')

        storage.put(path, body)

        return normalized_path

    def extract_file_data(self):
        if not 'media' in self.request.files: raise RuntimeError("File was not uploaded properly.")
        if not self.request.files['media']: raise RuntimeError("File was not uploaded properly.")

        return self.request.files['media'][0]

    def save_and_render(self, overwrite=False):
        file_data = self.extract_file_data()
        body = file_data['body']
        filename = file_data['filename']

        path = self.write_file(filename, body, overwrite=overwrite)
        self.write(path)

    def post(self):
        self.save_and_render()

    def put(self):
        self.save_and_render(overwrite=True)
