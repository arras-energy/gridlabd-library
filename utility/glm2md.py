import os, sys
import json
import random

tmpfile = f"/tmp/glm2md_{hex(random.randint(2**62,2**63))[2:]}.json"

os.system(f"gridlabd -C {sys.argv[1]} -o {tmpfile}")

IGNOREDKEYS = ["id","class","rank","clock","rng_state","guid","flags"]

try:
    with open(tmpfile,"r") as fh:
        glm = json.load(fh)
        first = True
        for name in list(glm["objects"].keys()):
            data = glm["objects"][name]
            for key in list(data.keys()):
                if key in IGNOREDKEYS:
                    del data[key]
            if first:
                def title(x):
                    x = x.replace('_',' ').strip().split()
                    if len(x) == 1:
                        return x[0][0].upper() + x[0][1:].lower()
                    else:
                        return ' '.join([title(y) for y in x])
                labels = [title(x) for x in data.keys()]
                print(f"| Name | {' | '.join(labels)} |")
                first = False
            print(f"| {name} | {' | '.join(data.values())} |")
    os.remove(tmpfile)
except:
    os.remove(tmpfile)


