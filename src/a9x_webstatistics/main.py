import io, sys, argparse, json, ast

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--statfile", help="json file that contains calculated statistics", default="webstat.json")
    parser.add_argument("-i", "--infile", help="filename including path to web server access log that contains input data", default="/var/log/nginx-access.json")
    args = parser.parse_args()

    if args.cmd == "crtstats":
        parser.print_help()
    elif args.cmd == "crtissues":
        parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
