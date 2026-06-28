import argparse
from quiz import run_quiz


def main():
    parser = argparse.ArgumentParser(description="CLI tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("quiz", help="Run the quiz")

    args = parser.parse_args()

    if args.command == "quiz":
        run_quiz()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
