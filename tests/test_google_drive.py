#!/usr/bin/env python3
# (C) Copyright 2022 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import climetlab as cml

from climetlab_google_drive_source import GoogleDrive


def test_source_metadata():
    # This is not necessary for the source to work properly
    # by is useful to check that the filenames are correct

    source = GoogleDrive(file_id="1PCkX-c1HQCjvmEmGJLyhPqhEGp6oVPiM")
    meta = source.google_metadata()

    assert isinstance(meta, dict), meta
    assert meta.get("filename_on_google_drive") == "ML_Crash_Course_final.zip", meta


def test_source():
    ds = cml.load_source(
        "google-drive",
        file_id="1PCkX-c1HQCjvmEmGJLyhPqhEGp6oVPiM",
    )

    for arr in ds:
        nparr = arr.to_numpy()
        assert nparr.shape == (5265488,)


if __name__ == "__main__":
    test_source_metadata()
    test_source()
