import random
import re

def random_capitalization(string, probability):
    if string.endswith(" "):
        ending_space = True
        string = string.rstrip()
    else:
        ending_space = False
        
    words = string.split()
    for i, word in enumerate(words):
        if random.random() < probability:
            words[i] = word.capitalize()

    result = ' '.join(words)
    
    if ending_space:
        result += " "
        
    return result

if __name__ == '__main__':
        # create an instance of the fileWriter class
    #fw = fileWriter('example.txt')

    iterLoops=10

    # call the write_sentence method to write the sentence to the file
        # open the file in write mode

    seeVerbs=[
        "visualize",
        "imagine",
        "look",
        "look-at",
        "see",
        "investigate",
        "sight",
        "notice",
        "percieve",
        "distinguish"
    ]

    tasteVerbs=[
        "taste",
        "lick",
        "bite",
        "chomp",
        "nibble",
        "kiss",
        "smooch"
    ]

    smellVerbs=[
        "smell",
        "sniff",
        "whiff",
        "inhale",
        "snort",
        "snuffle"
    ]

    hearVerbs=[
        "hear",
        "listen",
        "easedrop",
        "ease-drop",
        "overhear"
    ]

    touchVerbs=[
        "grab",
        "take",
        "touch",
        "steal",
        "covet",
        "nab",
        "swipe",
        "pick-up",
        "get",
        "hold",
        "grip",
        "clutch",
        "feel"
    ]

    useVerbs=[
        "use",
        "find",
        "make",
        "utilize",
        "give",
        "pull",
        "light",
        "ignite",
        "press",
        "shove",
        "drag",
        "push"
    ]

    moveVerbs=[
        "move",
        "depart",
        "trek",
        "hike",
        "go",
        "travel",
        "head",
        "walk",
        "ride",
        "run",
        "crawl",
        "jump",
        "roll",
        "fly",
        "manuever",
        "follow",
        "cartwheel"
    ]

    attackVerbs=[
        "hit",
        "attack",
        "kick",
        "punch",
        "slap",
        "drop-kick",
        "roundhouse-kick",
        "knee",
        "throw",
        "ambush",
        "assault",
        "combo",
        "bash",
        "crush",
        "cut",
        "sever",
        "rend",
        "shoot",
        "fire",
        "pummel",
        "beat-up",
        "fist",
        "headbutt",
        "head-butt",
        "tackle",
        "charge",
        "drop-kick",
        "axe-kick",
        "mash",
        "annhiliate",
        "whip",
        "slash",
        "stab",
        "lunge",
        "pierce",
        "slam",
        "spear",
        "skewer",
        "drill",
        "hammer",
        "crack",
        "elbow"
    ]

    talking_verbs = ['say', 'speak', 'talk', 'yell', 'whisper', 'exclaim', 'command', 'shout','mumble','gasp','answer','convey','inform','negotiate','question','interogate','cry',
                         'broker','contract','divuldge','respond','disclose','suggest','reply','comment','groan','gasp','affirm','inform','wonder','ponder','ask','plead','beg','scream']

    exampleStart = tasteVerbs+touchVerbs+useVerbs+moveVerbs+attackVerbs+smellVerbs+hearVerbs+seeVerbs
    
    exampleEnd=["car",
    "gun",
    "bazooka",
    "lazer",
    "laser",
    "teleporter",
    "portal",
    "helicopter",
    "plane",
    "airplane",
    "TV",
    "Tesla",
    "Twitter",
    "bicycle",
    "bike",
    "biology",
    "e-book",
    "e-mail",
    "ebook",
    "email",
    "ereader",
    "e-reader",
    "tshirt",
    "engine",
    "gaming",
    "gsas",
    "pimbo",
    "hospital",
    "hydrant",
    "hydraulics",
    "scooter",
    "motorcycle",
    "subway",
    "sub-way",
    "train",
    "ferrari",
    "sports-car",
    "ambulance",
    "lightsaber",
    "light-saber",
    "plasma"
    "t-shirt",
    "smartphone",
    "computer",
    "tablet",
    "television",
    "camera",
    "airplane",
    "train",
    "boat",
    "submarine",
    "motorcycle",
    "skateboard",
    "rollerblades",
    "coffee",
    "briefcase",
    "wallet",
    "passport",
    "drivers-license",
    "credit card",
    "ticket",
    "magazine",
    "newspaper",
    "dvd",
    "cd",
    "copyright",
    "mp3-player",
    "headphones",
    "printer",
    "scanner",
    "atm",
    "projector",
    "whiteboard",
    "calculator",
    "thermometer",
    "barometer",
    "microscope",
    "blender",
    "toaster",
    "microwave",
    "washing-machine",
    "dishwasher",
    "submarine",
    "nuclear",
    "nuke",
    "missile",
    "bullet",
    "ammo",
    "magazine",
    "mag",
    "c4",
    "windshield",
    "steering-wheel",
    "land-mine",
    "vacuum-cleaner",]

    
    #"As you collect the gold, you hear a loud rumbling noise. What would you like to do?","completion":" [\'investigate the noise\', \'ignore the noise\', \'leave the room\']"}'

    with open('names.txt', 'r') as file:
        text = file.read()
        fixedText=re.sub(r'[^a-zA-Z\s\-]', '', text).lower().strip()
        names = fixedText.split()
    file.close()

    with open('nouns.txt', 'r') as file:
        text = file.read()
        fixedText=re.sub(r'[^a-zA-Z\s\-]', '', text).lower().strip()
        nouns = fixedText.split()
    file.close()

    validSentenceEnd=nouns+names

    iterLoops=9450

    iterLoops2=iterLoops

    with open('r.txt', 'w') as f:
        # loop through the range 1 to 11 (11 is exclusive)
        for i in range(0, iterLoops):
            randomNum1 = random.randint(0, (len(exampleStart)-1))

            #word1=random_capitalization(exampleStart[randomNum1],0.5);

            word1=re.sub(r'[^a-zA-Z\s\-]', '', exampleStart[randomNum1]).lower().strip()

            x='{"prompt":"'+word1+" "

            randomNum2 = random.randint(0, (len(exampleEnd)-1))

            #word2=random_capitalization(exampleEnd[randomNum2],0.5);

            word2=re.sub(r'[^a-zA-Z\s\-]', '', exampleEnd[randomNum2]).lower().strip()

            x+=word2

            x+=' ->","completion":"Invalid: Unregonized word in sentence\n"}'

            # write the number followed by a new line character
            f.write(x + '\n')
    f.close()

    with open('actDetect.txt', 'w') as f:
        # loop through the range 1 to 11 (11 is exclusive)
        for i in range(0, iterLoops2):
            randomNum1 = random.randint(0, (len(exampleStart)-1))

            #word1=random_capitalization(exampleStart[randomNum1],0.5);

            word1=re.sub(r'[^a-zA-Z\s\-]', '', exampleStart[randomNum1]).lower().strip()

            x='{"prompt":"'+word1+" "

            randomNum2 = random.randint(0, (len(validSentenceEnd)-1))

            #word2=random_capitalization(exampleEnd[randomNum2],0.5);

            word2=re.sub(r'[^a-zA-Z\s\-]', '', validSentenceEnd[randomNum2]).lower().strip()

            shouldAddSecondWord=False

            x+=word2+' ->","completion":'+" "

            if word2 not in exampleEnd:
                shouldAddSecondWord=True

                if word1 in talking_verbs:
                    x+='"speak'

                elif word1 in moveVerbs:
                    x+='"move'

                elif word1 in attackVerbs:
                    x+='"attack'

                elif word1 in seeVerbs:
                    x+='"see'

                elif word1 in hearVerbs:
                    x+='"hear'

                elif word1 in smellVerbs:
                    x+='"smell'

                elif word1 in tasteVerbs:
                    x+='"taste'

                elif word1 in touchVerbs:
                    x+='"touch'

                elif word1 in useVerbs:
                    x+='"use'

                if word2 =="up" or word2=="forward" or word2=="forwards":
                    word2="north"

                if word2 =="down" or word2=="backward" or word2=="backwards": 
                    word2="south"

                if word2=="left":
                    word2="west"

                if word2=="right":
                    word2="east"

            else:
            
                x+='"Invalid: Unregonized word in sentence\n"}'

                            # write the number followed by a new line character
            if shouldAddSecondWord:
                x+=(" "+word2+"\n"+'"}')
            
            f.write(x + '\n')
    f.close()

    # with open('descriptionExtension.txt', 'w') as f:
    #     # loop through the range 1 to 11 (11 is exclusive)
    #     for i in range(0, iterLoops):
    #         randomNum1 = random.randint(0, (len(exampleStart)-1))

    #         word1=random_capitalization(exampleStart[randomNum1],0.5);

    #         x='{"prompt":"'+word1+" "

    #         randomNum2 = random.randint(0, (len(exampleEnd)-1))

    #         word2=random_capitalization(exampleEnd[randomNum2],0.5);

    #         x+=word2

    #         x+=' ->","completion":"Error --> Unregonized word in sentence"}'

    #         # write the number followed by a new line character
    #         f.write(x + '\n')
    # f.close()