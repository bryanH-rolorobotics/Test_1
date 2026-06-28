import argparse
from utils import foo


def main():
    parser = argparse.ArgumentParser(description="CLI for foo.py functions")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    subparsers.add_parser("foo", help="Call foo()")

    args = parser.parse_args()

    if args.subcommand == "foo":
        print(foo())


if __name__ == "__main__":
    main()
