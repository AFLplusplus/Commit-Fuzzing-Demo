import aflCI

aflCI.fuzzpath = "~/Videos/AFLplusplus/"
aflCI.fuzztime = 5*60 # 5 minutes

aflCI.add(
  aflCI.Harness("harnesses/test1.c", [
    "include/header.h",
    "src/file1.c",
    "src/file2.c"
  ],
  "$CC harnesses/test1.c src/* -o $HARNESS",
  "harnesses/test1_seeds/"
)

aflCI.add(
  aflCI.Harness("harnesses/test2.c", [
    "include/header.h",
    "src/file2.c",
    "src/file3.c"
  ],
  "$CC harnesses/test1.c src/* -o $HARNESS",
  "harnesses/test2_seeds/"
)

aflCI.run()
