import json
import os
import jsbeautifier
import setup

unassignedItemModels = list()
unassignedBlockModels = list()

for blockModel in setup.modelBlockFolder.iterdir():
    with open(blockModel) as f:
        data = json.load(f)
        if (not 'textures' in data): continue
        textures = data['textures']
        for key in textures:
            isAssigned = len(str(textures[key]).split(':')) > 1
            if (not isAssigned):
                unassignedBlockModels.append(blockModel)
                break

for itemModel in setup.modelItemFolder.iterdir():
    with open(itemModel) as f:
        data = json.load(f)
        if (not 'textures' in data): continue
        textures = data['textures']
        for key in textures:
            isAssigned = len(str(textures[key]).split(':')) > 1
            if (not isAssigned):
                unassignedItemModels.append(itemModel)
                break

if (len(unassignedBlockModels) == 0 and len(unassignedItemModels) == 0):
    print("None unassigned textures were found, make sure to add your items and blocks to the models folder!")
    raise SystemExit

print(f"Found {len(unassignedItemModels)} unassigned item textures.")
print(f"Found {len(unassignedBlockModels)} unassigned block textures.")

inp = input('Do you wish to continue? Y/N ')
if (str(inp).lower() == 'n'): raise SystemExit

convertedBlockModels = 0
convertedItemModels = 0

for blockModel in unassignedBlockModels:
    with open(blockModel) as f:
        model = json.load(f)
        if (not 'textures' in model): continue
        textures = model['textures']
        for key in textures:
            model['textures'][key] = f"{setup.modId}:block/{os.path.splitext(blockModel.name)[0]}"
        with open(blockModel, 'w') as f:
            f.write(jsbeautifier.beautify(json.dumps(model), setup.opts))
            convertedBlockModels += 1

for itemModel in unassignedItemModels:
    with open(itemModel) as f:
        model = json.load(f)
        if (not 'textures' in model): continue
        textures = model['textures']
        for key in textures:
            model['textures'][key] = f"{setup.modId}:item/{os.path.splitext(itemModel.name)[0]}"
        with open(itemModel, 'w') as f:
            f.write(jsbeautifier.beautify(json.dumps(model), setup.opts))
            convertedItemModels += 1

if (convertedBlockModels > 0):
    print(f"Finished converting {convertedBlockModels} block model(s).")

if (convertedItemModels > 0):
    print(f"Finished converting {convertedItemModels} item model(s).")