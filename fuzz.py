#!/usr/bin/env python3

import aflCI
import os

aflCI.fuzzpath = os.path.expanduser("~/AFLplusplus/")
aflCI.fuzztime = 20 # 20 seconds

aflCI.add(
    aflCI.Harness("harnesses/test1", [
      "include/header.h",
      "src/file1.c",
      "src/file2.c"
    ],
    "$CC harnesses/test1.c src/* -o $HARNESS",
    "harnesses/test1_seeds/"
  )
)

aflCI.add(
    aflCI.Harness("harnesses/test2", [
      "include/header.h",
      "src/file2.c",
      "src/file3.c"
    ],
    "$CC harnesses/test1.c src/* -o $HARNESS",
    "harnesses/test2_seeds/"
  )
)

aflCI.run()
