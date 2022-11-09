"""Extract library objects from GLM files

Syntax: python3 extract.py CLASS [FOLDERS...] > GLMNAME

Valid classes are `transformer_configuration` and `regulator_configuration`.

Object naming convention are as follows:

- `tranformer_configuration`: `{connect_type}-{install_type}-{primary_voltage}-{secondary_voltage}-{power_rating}`
- `regulator_configuration`: `{"connect_type},{band_center},{band_width},{Control},{control_level}`
"""

import os,sys
import json
import random

NAMELIST = []
IGNOREDKEYS = ["id","class","rank","clock","rng_state","guid","flags"]

def find_objects(glmfile,oclass):
    tmpfile = f"/tmp/extract_{hex(random.randint(2**62,2**63))[2:]}.json"
    try:
        os.system(f"gridlabd -w -C {glmfile} -o {tmpfile}")
        with open(tmpfile,"r") as glm:
            data = json.load(glm)
            for obj,spec in data["objects"].items():
                if spec["class"] == oclass:
                    eval(f"write_{oclass}")(spec)
        os.remove(tmpfile)
    except Exception as err:
        os.remove(tmpfile)
        raise

def write_transformer_configuration(data):
    keys = [];
    for key,value in data.items():
        if key in ["connect_type","install_type","primary_voltage","secondary_voltage","power_rating"]:
            keys.append(value.replace(' ',''))
    name = '-'.join(keys)
    if name in NAMELIST:
        return False
    elif not NAMELIST:
        print("module powerflow;")
    print("object transformer_configuration")
    print("{")
    print(f"    name \"{name}\";")
    for key,value in data.items():
        if key not in IGNOREDKEYS:
            print(f"    {key} \"{value}\";")
    print("}")
    NAMELIST.append(name)
    return True

def write_regulator_configuration(data):
    keys = [];
    for key,value in data.items():
        if key in ["connect_type","band_center","band_width","Control","control_level"]:
            keys.append(value.replace(' ',''))
    name = '-'.join(keys)
    if name in NAMELIST:
        return False
    elif not NAMELIST:
        print("module powerflow;")
    print("object regulator_configuration")
    print("{")
    print(f"    name \"{name}\";")
    for key,value in data.items():
        if key not in IGNOREDKEYS:
            print(f"    {key} \"{value}\";")
    print("}")
    NAMELIST.append(name)
    return True

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Syntax: python3 extract.py CLASS [FOLDERS ...]",file=sys.stderr)
        exit(1)
    for folder in ["."] if len(sys.argv) < 2 else sys.argv[2:]:
        for file in os.listdir(folder):
            basename = os.path.basename(file)
            if os.path.splitext(basename)[1] == ".glm" and basename[:5] == "test_":
                objlist = find_objects(basename,sys.argv[1])
