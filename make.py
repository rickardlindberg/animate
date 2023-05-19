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
            "animationstudio",
            "animationstudio.events",
            "animationstudio.graphics",
            "animationstudio.process",
            "animationstudio.render",
            "animationstudio.preview",
        ]:
            suite.addTest(doctest.DocTestSuite(
                importlib.import_module(module),
                optionflags=doctest.REPORT_NDIFF|doctest.FAIL_FAST
            ))
        if not unittest.TextTestRunner().run(suite).wasSuccessful():
            sys.exit(1)
    elif command == ["rundev"]:
        sys.exit(subprocess.run([sys.executable, "animate.py"]).returncode)
    else:
        sys.exit("\n".join(usage()))
