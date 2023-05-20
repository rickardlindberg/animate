#!/usr/bin/env python3

import doctest
import importlib
import subprocess
import sys
import unittest

def usage():
    return [
        "Usage:",
        "",
        "    ./make.py build",
        "    ./make.py rundev",
    ]

if __name__ == "__main__":
    command = sys.argv[1:]
    if command == ["build"]:
        suite = unittest.TestSuite()
        for module in [
            "example",
            "animationstudio",
            "animationstudio.events",
            "animationstudio.graphics",
            "animationstudio.render",
            "animationstudio.preview",
            "animationstudio.geometry",
        ]:
            suite.addTest(doctest.DocTestSuite(
                importlib.import_module(module),
                optionflags=doctest.REPORT_NDIFF|doctest.FAIL_FAST
            ))
        if not unittest.TextTestRunner().run(suite).wasSuccessful():
            sys.exit(1)
    elif command == ["rundev"]:
        sys.exit(subprocess.run(["./bin/animationstudio", "exampley"]).returncode)
    else:
        sys.exit("\n".join(usage()))
