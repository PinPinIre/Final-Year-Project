import sys
import os
from chardet.universaldetector import UniversalDetector


def report_encoding(path):
    file = open(path)
    detector = UniversalDetector()
    for line in file.readlines():
        detector.feed(line)
        if detector.done: break
    detector.close()
    file.close()
    print detector.result["encoding"]


def main():
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        report_encoding(sys.argv[1])
    else:
        print "None"

if __name__ == "__main__": main()
