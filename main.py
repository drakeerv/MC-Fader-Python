from PIL import Image
import numpy as np
import os

def merge(base, mask, output, outputDir, fade, show=False):
    if(os.path.exists(base + ".mcmeta")):
        return

    def getAverageRGBA(image):
      im = np.array(image)
      w,h,d = im.shape
      im.shape = (w*h, d)
      return tuple(im.mean(axis=0))
    
    if not(".png" in base):
        base += ".png"
    if not(".png" in mask):
        mask += ".png"
    if not(".png" in output):
        output += ".png"

    fade /= 100
        
    maskImg = Image.open(f"{mask}")
    baseImg = Image.open(f"{base}")

    alphaMask = baseImg.split()[-1]

    maskSize = maskImg.size
    baseSize = baseImg.size

    maskImg = maskImg.convert("RGBA")
    baseImg = baseImg.convert("RGBA")

    maskImg = maskImg.resize(baseSize)
    averageR, averageB, averageG, averageA = getAverageRGBA(baseImg)
    maskImg = Image.blend(maskImg, Image.new('RGBA', baseSize, color=(int(round(averageR)),int(round(averageB)),int(round(averageG)))).convert("RGBA"), 0.25)
    maskImg.show()
    
    try:
        maskImg.putalpha(alphaMask)
    except ValueError:
        maskImg.putalpha(255)
    
    outImg = Image.blend(baseImg, maskImg, alpha=fade)
    outImg.save(f'{outputDir}{output}', "PNG")

    if show: outImg.resize((256, 256)).show()

def getFiles(folder):
    search = folder + "/minecraft/textures/block"
    
    files = []
    
    for file in os.listdir(search):
        if file.endswith(".png"):
            files.append(str(os.path.join(search, file)).replace("\\", "/"))

    search = folder + "/minecraft/textures/item"

    for file in os.listdir(search):
        if file.endswith(".png"):
            files.append(str(os.path.join(search, file)).replace("\\", "/"))
            
    return(files)

def getNames(folder):
    search = folder + "/minecraft/textures/block"
    
    names = []
    
    for file in os.listdir(search):
        if file.endswith(".png"):
            names.append("block/" + file)

    search = folder + "/minecraft/textures/item"

    for file in os.listdir(search):
        if file.endswith(".png"):
            names.append("item/" + file)
            
    return(names)

def createPack(folder):
    lines = ['{\n',
             '  "pack": {\n',
             '    "pack_format": 6,\n',
             '    "description": "Pack made by MC Fader Python"\n',
             '  }\n',
             '}\n']
             
    
    os.mkdir(folder)

    mcmeta = open(folder + "/pack.mcmeta", "w")
    mcmeta.writelines(lines)
    mcmeta.close()
    
    os.mkdir(folder + "/assets")
    os.mkdir(folder + "/assets/minecraft")
    os.mkdir(folder + "/assets/minecraft/textures")
    os.mkdir(folder + "/assets/minecraft/textures/block")
    os.mkdir(folder + "/assets/minecraft/textures/item")

    return(folder + "/assets/minecraft/textures/")

textures = getFiles("./default")
names = getNames("./default")
newPack = createPack("./edited")

mask = "./mask.png"

for i in range(len(textures)):
    merge(textures[i], mask, names[i], newPack, 60)
