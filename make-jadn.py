import json
import os
from collections import defaultdict


def main():
    with open(os.path.join('json', 'codes.json')) as fp:
        ccodes = json.load(fp)
    print(len(ccodes))
    col = {ccodes[0][n]: n for n in range(len(ccodes[0]))}

    fields = [[int(cc[col['Numeric']]), cc[col['Alpha-2 code']], cc[col['English short name']]] for cc in ccodes[1:]]
    types = [['ISO-3166-1', 'Enumerated', [], 'Country codes', fields]]

    dt = defaultdict(list)
    for t in types[0][4]:
        dt[t[0]].append(t)
    for k, v in dt.items():
        if len(v) > 1:
            print(v)

    os.makedirs('out', exist_ok=True)
    with open('out/iso-3166-1.jadn', 'w') as fp:
        json.dump({'meta': {'package': 'http://iso.org/3166-1'}, 'types': types}, fp)

if __name__ == "__main__":
    main()