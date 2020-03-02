# AFL++ Commit Fuzzing Demo

This is an example library to show how to fuzz with AFL++ only the code modified by the last commit.

This can be easily integrated as pre-commit hook or CI script.

Basically, for each of your harnesses, you have to define the list of source files covered by fuzzing that harness.

When `fuzz.py` is runned, it checks the files modified by the last commit in git and, if there are some harnesses that depends on one of such files, fuzz them for a fixed period of time using the LLVM whitelisting and so collecting coverage feedback only from the modified files.

This can be called "commit oriented fuzzing" if you want.

This code was written in 10 minutes, don't expect something for your production-ready library.
