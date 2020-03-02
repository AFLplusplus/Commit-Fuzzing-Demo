import os
import tempfile
import subprocess
import uuid

fuzzpath = os.path.expanduser("~/AFLplusplus/")
fuzztime = 10*60 # 10 minutes

harnesses = []

def add(h):
    global harnesses
    harnesses.append(h)

class Harness(object):
    def __init__(self, filename, deps, cmd, seeds):
        self.filename = filename
        self.deps = deps
        self.cmd = cmd
        self.seeds = seeds
        self.compiled = False
    
    def generate_whitelist(self):
        o = subprocess.getoutput("git diff --name-only HEAD HEAD~1")
        gitfiles = list(map(lambda x: x.strip(), o.split("\n")))
        w = []
        for f in self.deps:
            if f in gitfiles:
                w.append(f)
        return w
    
    def compile(self):
        print("Compiling " + self.filename)
        global fuzzpath
        wl = self.generate_whitelist()
        if len(wl) == 0:
            print ("Skipping, not touched by last commit")
            return
        env = os.environ.copy()
        tmplist = tempfile.NamedTemporaryFile(delete=False)
        env["AFL_LLVM_WHITELIST"] = tmplist.name
        tmplist.write(str.encode("\n".join(wl)))
        tmplist.close()
        for f in wl:
            print(f)
        env["CC"] = os.path.join(fuzzpath, "afl-clang-fast")
        env["CXX"] = os.path.join(fuzzpath, "afl-clang-fast++")
        env["LD"] = os.path.join(fuzzpath, "afl-clang-fast")
        env["AFL_LLVM_LAF_SPLIT_SWITCHES"] = "1"
        env["AFL_LLVM_LAF_TRANSFORM_COMPARES"] = "1"
        env["AFL_LLVM_LAF_SPLIT_COMPARES"] = "1"
        env["AFL_USE_UBSAN"] = "1"
        env["AFL_USE_ASAN"] = "1"
        env["HARNESS"] = self.filename
        process = subprocess.Popen(self.cmd, env=env, shell=True)
        process.wait()
        if process.returncode != 0:
            print("Compilation failed")
        else:
            self.compiled = True
        os.unlink(tmplist.name)
    
    def fuzz(self):
        if not self.compiled:
            print(self.filename + " not compiled!")
            return 0
        print("Fuzzing " + self.filename)
        global fuzzpath, fuzztime
        env = os.environ.copy()
        env["HARNESS"] = self.filename
        outdir = "/tmp/aflCI-out-" + str(uuid.uuid4())
        c = '"' + os.path.join(fuzzpath, "afl-fuzz") + '" -i "' + self.seeds + '" -o "' + outdir + '" -m none -d -V %d ' % fuzztime + " -- $HARNESS"
        print (c)
        process = subprocess.Popen(c, env=env, shell=True)
        process.wait()
        crashes = os.path.join(outdir, "crashes")
        if len(os.listdir(crashes)) > 1:
            print("Crashes found! " + crashes)
            return len(os.listdir(crashes)) -1
        else:
            print("All OK!")
            os.system("rm -rf '" + outdir + "'")
            os.unlink(self.filename)
            return 0

def run():
    global harnesses
    for h in harnesses:
        h.compile()
    crashes = 0
    for h in harnesses:
        crashes += h.fuzz()
    if crashes > 0:
        os.abort()
