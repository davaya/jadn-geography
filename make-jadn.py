import json
import os


def main():
    with open(os.path.join('json', 'codes.json')) as fp:
        ccodes = json.load(fp)
    print(len(ccodes))
    col = {ccodes[0][n]: n for n in range(len(ccodes[0]))}
    pass

if __name__ == "__main__":
    main()