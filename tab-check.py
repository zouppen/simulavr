#!/usr/bin/python
import subprocess
import sys
from optparse import OptionParser

GIT_CMD = ["git", "ls-files"]
GIT_FILE_FILTER = ["*.cpp", "*.h", "*.c", "*.py", "*.tcl"]

HELP = """Counts tabs in source files, which are controlled by git. Source files are: %s. In summary
mode (default without options) it shows only a total count of tabs and files, which contain tabs. In
detailed mode it shows file names and count of tabs in this file, ordered by tab count. (files with 
most tabs last)
""" % ", ".join(["'%s'" % i for i in GIT_FILE_FILTER])

def readArgs():
  p = OptionParser(description = HELP)
  p.add_option("-d", "--detailed", dest = "detailed", action = "store_true",
                        help = "detailed mode, lists files wich contain tabs",
                        default = False)
  opts, args = p.parse_args()
  if len(args) > 0 : p.error("to much arguments, none expected")
  return opts
  
def getFileList():
  try:
    raw = subprocess.Popen(GIT_CMD + GIT_FILE_FILTER, stdout = subprocess.PIPE).communicate()[0]
  except:
    print "error: can't run '%s'" % " ".join(GIT_CMD)
    sys.exit(1)
  return filter(None, raw.split("\n"))

def getTabFromFile(name):
  try:
    f = open(name, "r")
    cnt = 0
    for c in f.read():
      if c == "\t": cnt += 1
    f.close()
  except:
    print "warning: can't read '%s'" % name
    return (name, 0)
  return (name, cnt)

def zeroTabs(i):
  if i[1] == 0: return False
  return True

def printSummary(totalTabs, totalTabFiles, totalFiles):
  print "tabs total: %d, files with tabs total: %d, all source files: %d" % (totalTabs,
                                                                             totalTabFiles,
                                                                             totalFiles)

def printDetailed(filtered):
  def _sort(a, b):
    if a[1] > b[1]: return 1
    if a[1] < b[1]: return -1
    return 0
  filtered.sort(_sort)
  for i in filtered: print "%4d %s" % (i[1], i[0])

if __name__ == "__main__":

  opts = readArgs()
  raw = getFileList()
  totalFiles = len(raw)
  tabs = [getTabFromFile(i) for i in raw]
  filtered = filter(zeroTabs, tabs)
  totalTabs = sum([i[1] for i in filtered])
  totalTabFiles = sum([1 for i in filtered if not i[1] == 0])
  if opts.detailed:
    printDetailed(filtered)
  else:
    printSummary(totalTabs, totalTabFiles, totalFiles)
  sys.exit(0)

# EOF
