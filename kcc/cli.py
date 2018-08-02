'''
cli for kernel config checker
'''
import sys

from .kconfig import Kconfig

def usage() -> None:
    print("Usage:")
    print("\tkernel-config-checker.py <configfile>")
    exit(0)

def cli() -> None:
    if len(sys.argv) != 1 and len(sys.argv) != 2:
        usage()

    kconfig = Kconfig.default()
    if len(sys.argv) == 1:
        results = kconfig.check(sys.stdin)
    else:
        with open(sys.argv[1], "r") as input_file:
            results = kconfig.check(input_file)
    for opt, msg in results.items():
        print(opt, msg)
