import os
import tempfile
import uuid

fuzzpath = "~/AFLplusplus/"
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
        self.harness = "/tmp/aflCI-" + uuid.uuid4()
    
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
        env = os.environ.copy()
        tmplist = tempfile.NamedTemporaryFile(delete=False)
        env["AFL_LLVM_WHITELIST"] = tmplist.name
        tmp.write(self.generate_whitelist())
        tmp.close()
        env["CC"] = os.path.join(fuzzpath, "afl-clang-fast")
        env["CXX"] = os.path.join(fuzzpath, "afl-clang-fast++")
        env["LD"] = os.path.join(fuzzpath, "afl-clang-fast")
        env["AFL_LLVM_LAF_SPLIT_SWITCHES"] = "1"
        env["AFL_LLVM_LAF_TRANSFORM_COMPARES"] = "1"
        env["AFL_LLVM_LAF_SPLIT_COMPARES"] = "1"
        env["HARNESS"] = self.harness
        process = subprocess.Popen(self.cmd, env=env, shell=True)
        process.wait()
        os.unlink(tmp.name)
    
    def fuzz(self):
        print("Fuzzing " + self.filename)
        global fuzzpath, fuzztime
        env = os.environ.copy()
        env["HARNESS"] = self.harness
        outdir = tempfile.TemporaryDirectory(dir="/tmp")
        c = '"' + os.path.join(fuzzpath, "afl-fuzz") + '" -i "' + self.seeds + '" -o "' + outdir + " -d -V %d " % fuzztime + " -- $HARNESS"
        print (c)
        outdir.cleanup()

def run():
    global harnesses
    for h in harnesses:
        h.compile()
    for h in harnesses:
        h.fuzz()
