'''
cli for kernel config checker
'''
import sys

from .kconfig import Kconfig

def usage(*args) -> None:
    print("Usage:")
    # Exit clean on help request or error on invalid arguments
    print("\tkernel-config-checker.py <configfile>")
    if '-h' in sys.argv \
            or '--help' in sys.argv:
        sys.exit(0)
    sys.exit(1)

def cli() -> None:
    if len(sys.argv) > 2 \
            or '-h' in sys.argv \
            or '--help' in sys.argv:
        usage()

    kconfig = Kconfig.default()
    if len(sys.argv) == 1:
        results = kconfig.check(sys.stdin)
    else:
        with open(sys.argv[1], "r") as input_file:
            results = kconfig.check(input_file)
    if not results:
        sys.exit(0)
    for opt, msg in results.items():
        print(opt, msg)
    sys.exit(1)
