#!/usr/bin/env python3
# (C) Copyright 2022 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
import os
from html.parser import HTMLParser

import climetlab as cml
import requests
from climetlab import Source


def get_title_parser(txt):
    metadata = {}

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag != "meta":
                return
            attrs = dict(attrs)
            if attrs.get("property") != "og:title":
                return
            metadata["filename_on_google_drive"] = attrs.get("content")

    MyHTMLParser().feed(txt)
    return metadata


def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "version")
    with open(version_file, "r") as f:
        version = f.readlines()
        version = version[0]
        version = version.strip()
    return version


__version__ = get_version()


class GoogleDrive(Source):
    _google_metadata = None

    def __init__(self, file_id, *args, **kwargs):
        self._file_id = file_id

        url = (
            f"https://drive.google.com/uc?export=download&id={self._file_id}&confirm=t"
        )
        self.source = cml.load_source("url", url, *args, **kwargs)

    def google_metadata(self):
        if self._google_metadata is None:
            r = requests.get(f"https://drive.google.com/file/d/{self._file_id}/view")
            self._google_metadata = get_title_parser(r.text)
        return self._google_metadata

    def mutate(self):
        return self.source
