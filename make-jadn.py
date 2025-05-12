import json
import os


def main():
    with open(os.path.join('json', 'codes.json')) as fp:
        ccodes = json.load(fp)
    print(len(ccodes))
    col = {ccodes[0][n]: n for n in range(len(ccodes[0]))}

    fields = [[int(cc[col['Numeric']]), cc[col['Alpha-2 code']], cc[col['English short name']]] for cc in ccodes[1:]]
    types = [['ISO-3166-1', 'Enumerated', [], 'Country codes'], fields]

    with open('iso-3166-1.jadn', 'w') as fp:
        json.dump({'meta': {'package': 'http://iso.org/3166-1'}, 'types': types}, fp)

if __name__ == "__main__":
    main()