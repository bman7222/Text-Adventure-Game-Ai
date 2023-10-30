import gameState
import gameLocations
import openai
import os
#import tagAI
import re

def clean_string(text):
    # replace all characters except letters, numbers, -, ", ', and whitespace (including new lines) with empty string
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s\.\,\;\-\"\'\n]", "", text)

    return cleaned_text


instructionsBase=text="""You are a text-adventure game AI that does action detection and description extension. 
When given a verb followed by a subject, for example, touch torch, you will use action detection. A verb or subject 
can be separated with a - for example axe-kick or red-button. When you use action detection you will output the prompt but 
replace the verb with one of the allowed verbs. The allowed verbs are "speak", "see", "smell", "taste", "touch", "move", "use",
and "attack"

Prompt: yell river @
Completion: speak river @

Prompt: snort rain @
Completion: smell rain @

Prompt: imagine whale @
Completion: see whale @

Prompt: take apple @
Completion: touch apple @

Prompt: bite rock @
Completion: taste rock @

Prompt: cartwheel south @
Completion: move south @

Prompt: push button @
Completion: use button @

Prompt: roundhouse-kick statue @
Completion: attack statue @

 If the action detection prompt uses one of the allowed verbs, then do not change it. 

Prompt: use axe @
Completion: use axe @

Prompt: move north @
Completion: move north @

If the action detection prompt uses a verb you do not recognize then the completion should be the closest possible allowed verb. 

Prompt: criticize goblin @
Completion: speak goblin @

When given text in quotation marks, for example, "You are in a green forest", you will write do description expansion. 
When doing description expansion, you will write a detailed description. Extend the description by adding details to it and 
adding things often found in the setting the description takes place in. 

Prompt: "You are in a green forest." @
Completion: "You are in a green forest. Birds loudly chirp and the shrubs rustle in the wind. An assortment of mushrooms sprout 
from a log, each bulbous head about to burst spores. A nearby river gently trickles in the distance and the trees 
dance in the wind." @

If there are characters or items in the scene they will appear in the description extension prompt labeled as 
"Characters: Example-Character ->" or "Items: Example-Item-1, Example-Item-2 ->". The characters and items are separated by 
a comma, and ended with the characters ->

Prompt: "You are at the beach. Characters: John, Albert -> Items: seaweed, shell, bucket ->" 
Completion: "You are at the beach. John, Albert, and you are baking in the sun. The smell of salt hits straight through you. 
Albert uses his bucket as a helmet, making himself look like a british soldier. Seaweed clings to the rocks, 
refusing to let go even as the waves crash onto them. A seashell, glimmering like glass, is wedged into a sand castle." @

If a character has a description, that description will be next after the characters name separated by the dollar sign 
character "$"

Prompt: "You are at the port-city of Water Seven. The city is made up of multiple canals and is 
built with marble stone. Boats are pulled by giant seahorses. Characters: Franky $ The Shipwright and Brother of Ice Cube. 
His Workshop is always noisy and hazardous. , Ice Cube $ The Mayor and brother of Franky. He is always very busy. , 
Lucci $ Secret Agent of CP9. He is tasked with assassinating Ice Cube ->" @
Completion: "You are at the port-city of Water Seven. While it may seem to be covered in water slides, those are actually
the cities canals. Those who decide not to walk on the brilliant marble streets ride gondolas pulled by giant seahorses. 
Down the street, black smog bellows from Franky's workshop. The busy mayor, Ice Cube walks hastily while a suspicious masked
follows him." @

If the description starts with percent character "%" and then followed by "Characters: " then dialogue between the user 
and the characters should be completed. Dialogue should be surrounded by a single quote '. If a new character talks, separate 
it with a new line \n. 

Prompt: "%  Characters: Johnny $ Your friend. , Eric $ Your enemy. -> Hey what are we doing for lunch?" @
Completion: "'I was thinking of hitting that new pizza place,' said John. He and you used to get pizza when you were kids. 
'I hate pizza,' said Eric. When you and John got pizza he would dunk your face into it and laugh." @

If the description starts with an asterisk character "*" then an action should be described. If the action uses an item or 
there is a character involved, it will be written in the prompt. Using and characters will be ended with a -> character. 
Characters will be separated by a comma. 

Prompt:"* You attack the golem. Using: hammer -> Characters: Golem $ A large golem made of stone." @
Completion: "You swing at the golem with your hammer. Its leg shatters off of its body. The golem crashes into the ground,
 creating a crater from the impact." @

You do not recognize modern words such as t-shirt, computer, TV, DVD, CD, plane, car, and other modern words and items.
 Do not use any URLS or refer to any websites in your answers. Output action detection completions in the form "Verb Subject" 
 and description extension completions with "Insert Description Here"

Prompt: touch rock @
Completion: touch rock @

Prompt: sniff boulder @
Completion: smell boulder @

Prompt: "You use the stick." @
Completion: Using the stick, you are able to reach a little bit further than you could before. @

Prompt: "You use the key. Using:door ->" @
Completion: Using the key, You unlock the door and it opens with a nearby @

"""

def get_descriptionExtentsion(prompt):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    instructions=instructionsBase+"\nPrompt:" + prompt +"@\nCompletion:"

    temp=0.5

    max_toks=2500

    frequencyPenalty=0

    presencePenalty=0.6

    response=openai.Completion.create(
        model="text-davinci-003",
        prompt=instructions,
        temperature=temp,
        max_tokens=max_toks,
        top_p=1,
        frequency_penalty=frequencyPenalty,
        presence_penalty=presencePenalty,
    )

    completion=(response.choices[0].text)

    return completion

def get_actionDetection(prompt):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    instructions=instructionsBase+"\nPrompt:" + prompt +"\nCompletion:"

    temp=0

    max_toks=2500

    frequencyPenalty=0

    presencePenalty=0.6

    response=openai.Completion.create(
        model="text-davinci-003",
        prompt=instructions,
        temperature=temp,
        max_tokens=max_toks,
        top_p=1,
        frequency_penalty=frequencyPenalty,
        presence_penalty=presencePenalty,
    )

    completion=(response.choices[0].text)

    return completion


def parse_input(input_str):

    output,speechWord=extract_subject_verb(input_str)

    if output==False and speechWord==True:
        return False

    self_verbs=["hear","see","taste","touch","smell","attack","move","use"]

    verb=False

    subject=False

    actionIsSpeech=False

    if output==False:
        print("""Invalid: For actions please use (Verb Subject).
For multi-word subjects, seperate using a '-' EX: Press Red-button
To speak use EX: speak insert sentence here.
Or surround the speech in quotes EX: 'Insert sentence here.'
To list location and inventory, type inventory, or self EX: 'self'""")
        
        return False
        
    # is dialogue 
    elif isinstance(output,str):
        actionIsSpeech=True

        #If there is a speech word, save it for output, otherwise use say 
        if not speechWord or speechWord=="speak":
            speechWord="say"

#If actionDetection
    elif isinstance(output,list):

        verb=output[0]

        subject=output[1]

        prompt=""+verb+" "+subject

        output=get_actionDetection(prompt).lower().strip()

        detectedAction = re.sub(r'[^\w\s]\-', '', output).split()[0]

    #If the action is speech 
    if actionIsSpeech:

        if  len(game_locations.get_characters(game_state.playerLocation))<=0:

            prompt="% Characters: You ->"+output

            output=clean_string(get_descriptionExtentsion(prompt))

        else:
            #Ai response pls character description needs to be done
            prompt="% Characters: You, "

            for i,character in enumerate(game_locations.get_characters(game_state.playerLocation)):
                prompt+=character

                if (len(game_locations.get_characters(game_state.playerLocation))>1) and i < len(game_locations.get_characters(game_state.playerLocation))-1:
                    prompt+=", "

            prompt+=" -> "+output

            output=clean_string(get_descriptionExtentsion(prompt))

        print(output)

    #action detection succeed

    elif detectedAction in self_verbs:
        if detectedAction =="move":
            valid_answer=False

            directions_can_move=""

            while not valid_answer:
                if subject in game_locations.get_connections(game_state.playerLocation):

                    #Ai response pls add items and characters and their descriptions

                    oldLocation=game_state.playerLocation

                    game_state.playerLocation=game_locations.get_connections(game_state.playerLocation)[subject]

                    prompt="\"You leave "+oldLocation+". "+"You "+verb+" to "+game_state.playerLocation+". "+game_locations.get_description(game_state.playerLocation)+"\""

                    output=clean_string(get_descriptionExtentsion(prompt))

                    print(output)

                    #exit loop success
                    valid_answer=True

                    continue

                elif subject in direction_strings and not subject in game_locations.get_connections(game_state.playerLocation):
                    for i,direction in enumerate(game_locations.get_connections(game_state.playerLocation)):

                        directions_can_move+=direction

                        if (len(game_locations.get_connections(game_state.playerLocation))>1) and i < len(game_locations.get_characters(game_state.playerLocation))-1:
                            direction+=", "

                    print(f"""Invalid: You cannot move '{subject}' from '{game_state.playerLocation}'
From '{game_state.playerLocation}' you can move {directions_can_move}
To list location and inventory, type inventory, or self EX: 'inventory' 
To quit this action, type quit EX:'quit'""")

                else:
                    for i,direction in enumerate(game_locations.get_connections(game_state.playerLocation)):
    
                        directions_can_move+=direction

                        if (len(game_locations.get_connections(game_state.playerLocation))>1) and i < len(game_locations.get_characters(game_state.playerLocation))-1:
                            direction+=", "

                    print(f"""Invalid: '{subject}' is not a valid direction. Type in a single valid direction EX: 'north'
From '{game_state.playerLocation}' you can move {directions_can_move}
To list location and inventory, type inventory, or self EX: 'inventory' 
To quit this action, type quit EX:'quit'""")
                
                action_input=input("> ")

                subject=re.sub(r'[^a-zA-Z\s\-]', '', action_input).lower().strip()

                if(subject in look_at_self_strings):
                    print(game_state)
                    continue

                elif(subject in quit_strings):
                    #exit loop fail
                    return False
                
        elif detectedAction == "use" or detectedAction=="touch" :
            if subject in game_locations.get_items(game_state.playerLocation) or (subject in game_state.inventory and game_state.inventory[subject]>0):
                
                prompt="\"You "+verb+" the "+subject+"\""

                output=clean_string(get_descriptionExtentsion(prompt))

                print(output)

            else:
                print(f"You cannot '{verb}' '{subject}'. Type in an item from your inventory or the environment")

                valid_answer=False

                while not valid_answer:
                    use_input=input("> ")

                    use_input=re.sub(r'[^a-zA-Z\s\-]', '', use_input).lower().strip()

                    if(use_input in look_at_self_strings):
                        print(game_state)
                        continue

                    if(use_input in quit_strings):
                        #exit loop fail
                        return False
                    
                    if(use_input in game_locations.get_items(game_state.playerLocation) or (use_input in game_state.inventory and game_state.inventory[use_input]>0)):
                        print(f"'{verb}' '{use_input}' confirmed")

                        valid_answer=True
                        
                        isUse=(detectedAction == "use")

                        isInInventory=(use_input in game_state.inventory and game_state.inventory[use_input]>0)

                        if isUse:
                            if isInInventory:
                                game_state.inventory[use_input]-=1
                            else:
                                game_locations[game_state.playerLocation]["items"].remove(use_input)

                        if not isUse:
                            if isInInventory:
                                game_state.inventory[use_input]-=1
                            else:
                                game_state.inventory[use_input]=1

                        continue

                    else:
                        print(f"""Invalid: You cannot '{verb}' '{use_input}'.
Please list an item in the inventory or the environment EX: 'stick'
For multi-word items please seperate using a '-' EX: 'Ancient-Sword'
To list location and inventory, type inventory, or self EX: 'inventory' 
To quit this action, type quit EX:'quit'""")
                        
                        continue


        elif detectedAction == "attack" :
            if (subject not in game_locations.get_items(game_state.playerLocation)) and (subject not in game_locations.get_characters(game_state.playerLocation)):
                 
                valid_answer1=False

                print(f"""You cannot '{verb}' '{subject}'. Type something in the environment to '{verb}'?""")

                while not valid_answer1:
        
                    subject=input("> ")

                    subject=re.sub(r'[^a-zA-Z\s\-]', '', subject).lower().strip()

                    if(subject in look_at_self_strings):
                        print(game_state)
                        continue

                    if(subject in quit_strings):
                        #exit loop fail
                        return False

                    if subject in game_locations.get_items(game_state.playerLocation) or subject in game_locations.get_characters(game_state.playerLocation):
                        
                        print("Attack Target Confirmed! "+subject)

                        #exit loop success
                        valid_answer1=True

                        continue

                    else:
                        print(f"""Invalid: You cannot '{verb}' '{subject}'.
Please list an item or character in the environment EX: 'Enemy'
For multi-word items please seperate using a '-' EX: 'Ancient-Sword'
To list location and inventory, type inventory, or self EX: 'inventory' 
To quit this action, type quit EX:'quit'""")
                        
                        continue

            print(f"Use what to '{verb}'?")

            valid_answer2=False

            while not valid_answer2:

                attack_input=input("> ")

                attack_input=re.sub(r'[^a-zA-Z\s\-]', '', attack_input).lower().strip()

                if(attack_input in look_at_self_strings):
                    print(game_state)
                    continue

                if(attack_input in quit_strings):
                    #exit loop fail
                    return False

                if attack_input in game_locations.get_items(game_state.playerLocation) or (attack_input in game_state.inventory and game_state.inventory[attack_input]>0):
                    
                    isInInventory=(attack_input in game_state.inventory and game_state.inventory[attack_input]>0)

                    if(isInInventory):
                        game_state.inventory[attack_input]-=1
                    else:
                        game_locations[game_state.playerLocation]["items"].remove(attack_input)

                    prompt='"You '+verb+' the '+subject+'Using: '+attack_input+' ->"'
                   
                    output=clean_string(get_descriptionExtentsion(prompt))

                    print(output)

                    #exit loop success
                    valid_answer2=True
                    continue

                else:
                    print(f"""Invalid: Is '{attack_input}' unavailible to use. 
Please list an item in your inventory or the environment EX: 'weapon'
For multi-word items please seperate using a '-' EX: 'Ancient-Sword'
To list location and inventory, type inventory, or self EX: 'inventory' 
To quit this action, type quit EX:'quit'""")
                    
                    continue

#see, taste, hear 
        else:
            if (subject in game_locations.get_items(game_state.playerLocation)) or (subject in game_locations.get_characters(game_state.playerLocation)) or (subject in game_state.inventory and game_state.inventory[subject]>0):
                print(f" '{verb}' '{subject}'")
            else:
                print(f"You cannot '{verb}' '{subject}'. Please type in something from the environment or inventory to '{verb}'")

                valid_answer=False

                while not valid_answer:
                    subject=input("> ")

                    subject=re.sub(r'[^a-zA-Z\s\-]', '', subject).lower().strip()

                    if(subject in look_at_self_strings):
                        print(game_state)
                        continue

                    if(subject in quit_strings):
                        #exit loop fail
                        return False
                    
                    if (subject in game_locations.get_items(game_state.playerLocation)) or (subject in game_locations.get_characters(game_state.playerLocation)) or (subject in game_state.inventory and game_state.inventory[subject]>0):
                        valid_answer=True

                        #Ai response pls description
                        print("'{verb}' '{subject}'")

                        continue

                    else:
                        print(f"""Invalid: '{subject}' unavailible to '{verb}'. 
Please list an item in your inventory or the environment EX: 'pebble'
For multi-word items please seperate using a '-' EX: 'Ancient-Sword'
To list location and inventory, type inventory, or self EX: 'inventory' 
To quit this action, type quit EX:'quit'""")

#We dont know what this verb is, generate a description for it anyways
    elif detectedAction not in self_verbs :
        print(f"Use what to '{verb}' '{subject}'?")

        valid_answer=False

        while not valid_answer:

            action_input=input("> ")

            action_input=re.sub(r'[^a-zA-Z\s\-]', '', action_input).lower().strip()

            if(action_input in look_at_self_strings):
                print(game_state)
                continue

            if(action_input in quit_strings):
                #exit loop fail
                return False

            if action_input in game_locations.get_items(game_state.playerLocation) or action_input in game_state.inventory:
                #Ai response pls description
                
                print("TRUE! "+action_input)

                #exit loop success
                valid_answer=True

                continue

            else:
                 print(f"""Invalid: '{action_input}' is not usable. 
Please list an item in inventory or the environment.
For multi-word items please seperate using a '-' EX: 'Blue-Rock'
To list location and inventory, type inventory, or self EX: 'inventory' 
To quit this action, type quit EX:'quit'""")
                 continue
         
#Passed everything 
    return True
    
def extract_subject_verb(input_str):

    talking_verbs = ['say', 'speak', 'talk', 'yell', 'whisper', 'exclaim', 'command', 'shout','mumble','gasp','answer','convey','inform','negotiate','question','interogate','cry',
                         'broker','contract','divuldge','respond','disclose','suggest','reply','comment','groan','gasp','affirm','inform','wonder','ponder','ask','plead','beg','scream']

    input_str = re.sub(r'[^a-zA-Z\s\'\"\-]', '', input_str).lower().strip()

    if input_str in look_at_self_strings:
        print(game_state)

        return False,True

    #No Input
    if len(input_str) == 0:
        return False,False
    
#check for quotes EX; "Hi how are you" 'I am doing ok'
    if input_str[0] == '"' and '"' in input_str[1:]:
             return ' '.join(input_str.split('"')[1::2]),False

    if input_str[0] == "'" and "'" in input_str[1:]:
            return ' '.join(input_str.split("'")[1::2]),False
        
#split into words. Eliminate non-alphabet characters
    input_arr = re.sub(r'[^\w\s]\-', '', input_str).split()

#Check for speaking word EX: Say Hi how are you
    if len(input_arr) >= 2 and input_arr[0] in talking_verbs:
        return " ".join(input_arr[1:]),input_arr[0]
        #More than 2 words, print error. Must be Verb Subject    

    #Retur nin the form [Verb, Subject]
    elif len(input_arr) == 2:
       #check if using a speaking action or not
        return input_arr,False
    
    #invalid 
    elif len(input_arr) <= 1:
        return False,False


if __name__ == '__main__':
    

    player_name = input("Enter Your Name > ");

    print("Welcome to the game "+player_name+".")

    inventory = {"stick": 2, "rock": 5, "pebble": 1}

    game_state = gameState.gameState(player_name, "cave", inventory)

    look_at_self_strings=["inventory","inven","inv","items","i","pockets","bag","me","self","where am i",game_state.playerName,"location","place"]

    quit_strings=["quit","stop","halt","cease","q"]

    direction_strings=['north','south','east','west']

    game_locations=gameLocations.gameLocations()

    # print(game_state);

    # print(game_locations.get_description("forest"))

    # game_locations.add_item_to_location("forest","rock")

    # print(game_locations.get_items("forest"))

    # game_locations.add_description_to_location("forest","A cool forest")

    # print(game_locations.get_description("forest"))

    # print(game_locations.get_connections("forest"))

    # game_locations.add_connection_to_location("cave","weast","beach")

    # game_locations.add_connection_to_location("lave","east","hills")

    # game_locations.add_connection_to_location("cave","east","hills")

    # game_locations.add_location("river","Its a river",[],[],{})

    # game_locations.add_connection_to_location("cave","east","river")

    # print(game_locations.get_connections("cave"))

    # print(game_locations.get_items("cave"))

    # print(game_locations.get_characters("forest"))

    # print(game_locations.get_characters("cave"))

    gameOn=True

    while gameOn:
            # Take input from the player
        player_input = input("> ")

        result=parse_input(player_input)

        if not result:
            continue



        #response=tagAI.parse_player_input(player_input,game_state)

        #print(response)

        gameOn=False


