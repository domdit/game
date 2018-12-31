from termcolor import cprint
import simplejson as json
import os
import random
import pickle
from itertools import groupby
import bisect
from time import sleep

# JSON FILE KEY ####################
location_json = "location.json"
json_data = open(location_json)
location_data = json.load(json_data)

enemy_json = "enemy.json"
json_data = open(enemy_json)
enemy_data = json.load(json_data)

item_json = "item.json"
json_data = open(item_json)
item_data = json.load(json_data)

spell_json = "spells.json"
json_data = open(spell_json)
spells_data = json.load(json_data)
# ##################################

# Prompts the user to answer question with either y/n
def yn(question):
    while "the answer is invalid":
        reply = str(input(str(question) +' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        elif reply[0] == 'n':
            return False
        else:
            print("Incorrect Input")
            wait()
            yn(question)


# roll dice, first argument is how many sides, second is how many die
def dice_roll(side, n):
    total = 0
    for x in range(n):
        total += random.randint(1, side)
    return total


# clear the screen
def cls():
    unused_variable = os.system("cls")


# this is clear the screen after user presses enter
def wait():
    input("Press ENTER to continue...")
    cls()


# The class for the user, stores all stats data and saves the game
class Char:

    def __init__(
            self, name, race, exp, str, int, dex, con, spd, current_hp, mp_bonus, current_mp,
            gold, weapon, shield, helm, chest, legs, hands, feet, ring, neck, current_capacity,
            sleep_speed
    ):
        self.name = name
        self.race = race
        self.exp = exp
        self.str = str
        self.int = int
        self.dex = dex
        self.con = con
        self.spd = spd
        self.current_hp = current_hp
        self.mp_bonus = mp_bonus
        self.current_mp = current_mp
        self.current_capacity = current_capacity

        self.gold = gold

        self.update()

        self.weapon = weapon
        self.shield = shield
        self.helm = helm
        self.chest = chest
        self.legs = legs
        self.hands = hands
        self.feet = feet
        self.ring = ring
        self.neck = neck

        self.sleep = sleep_speed

    def update(self):
        self.hp = (self.con + self.str) / 2
        self.mp = (self.int * self.mp_bonus)
        self.capacity = self.str * 5

    def save(self):
        with open("char_save.sav", "wb") as save_game:
            pickle.dump(self, save_game, protocol=pickle.HIGHEST_PROTOCOL)


# the default values for the user, this gets updated in get_char()
player = Char("x", "x", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "none", "none", "none",
                      "none", "none", "none", "none", "none", "none", 0, 2)


# amount of xp needed to level up
levels = [
    100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500,
    6600, 7800, 9100, 10500, 12000, 13600, 15300, 17100, 19000,
    21000, 23100, 25300, 27600, 30000, 32500, 35100, 37800, 40600,
    43500, 46500, 49600, 52800, 59500, 63000, 66600, 70300, 74100,
    78000, 82000, 86100, 90300, 94600, 99000, 103500, 108100, 112800,
    117600, 122500
    ]


# displays the level of the player
def get_level(dude):
    exp = dude.exp
    lvl = bisect.bisect(levels, exp) + 1
    return lvl


# displays how much xp needed to level up
def exp_left(dude):
    exp = dude.exp
    i = bisect.bisect_right(levels, exp)
    val = levels[i]
    left = val - exp
    return left

def exp_until(dude):
    exp = dude.exp
    i = bisect.bisect_right(levels, exp)
    val = levels[i]
    return val


# level up sequence... allots 3 skill points for a character to
# add to any skill
def lvl_up(dude):
    skill_points = 3
    while skill_points > 0:
        cls()
        cprint("Congratulations! You are now level " + str(get_level(dude)) + "!", "yellow")
        print(" ")
        print(
            "Add a skill point to a skill by typing the corresponding number below.")
        print("_____________________")
        print("1. str:  " + str(dude.str))
        print("2. int:  " + str(dude.int))
        print("3. dex:  " + str(dude.dex))
        print("4. con:  " + str(dude.con))
        print("5. spd:  " + str(dude.spd))
        print("_____________________")
        print("You have " + str(skill_points) + " skill point(s) left")
        action = input("Which skill would you like to level up: ")
        if action == "1":
            dude.str = dude.str + 1
            skill_points = skill_points - 1
        elif action == "2":
            dude.int = dude.int + 1
            skill_points = skill_points - 1
        elif action == "3":
            dude.dex = dude.dex + 1
            skill_points = skill_points - 1
        elif action == "4":
            dude.con = dude.con + 1
            skill_points = skill_points - 1
        elif action == "5":
            dude.spd = dude.spd + 1
            skill_points = skill_points - 1
        else:
            print("you input a wrong key, try again")
            wait()
    else:
        pass
    dude.update()
    dude.current_hp = dude.hp
    dude.current_mp = dude.mp


# the item inventory (maybe I should add this to the Char class?)
item_inventory = []

# spell list
spells = []


# saving the item inventory
def inv_save():
    with open("inv_save.sav", "wb") as save_game:
        pickle.dump(item_inventory, save_game, protocol=pickle.HIGHEST_PROTOCOL)


def spell_save():
    with open("spell_save.sav", "wb") as save_game:
        pickle.dump(spells, save_game, protocol=pickle.HIGHEST_PROTOCOL)


# this will load any save file
def load(file):
    with open(file, "rb") as save_game:
        return pickle.load(save_game)


# enemy class, all stats for enemies are stored in enemy.json
class Enemy:

    def __init__(self, enemy):

        self.nom = enemy_data[enemy]['nom']
        self.img = enemy_data[enemy]['img']
        self.lvl = enemy_data[enemy]['lvl']
        self.exp = enemy_data[enemy]['exp']
        self.str = enemy_data[enemy]['str']
        self.int = enemy_data[enemy]['int']
        self.dex = enemy_data[enemy]['dex']
        self.con = enemy_data[enemy]['con']
        self.spd = enemy_data[enemy]['spd']
        self.mp_bonus = enemy_data[enemy]['mp_bonus']
        self.hp = int((self.str + self.con) / 2)
        self.mp = int(self.int * self.mp_bonus)
        self.current_hp = self.hp
        self.current_mp = self.mp
        self.item_id = enemy_data[enemy]['item_id']
        self.item_name = enemy_data[enemy]['item_name']


# same as Enemy class, except this will auto-add an item
# to the player's inventory
class Item:

    def __init__(self, id):

        self.id = item_data[id]['id']
        self.name = item_data[id]['name']
        self.consume = item_data[id]['consume']
        self.heal = item_data[id]['hp']
        self.flavor = item_data[id]['flavor']
        self.weight = item_data[id]['weight']

        item_inventory.append(self.name)
        player.current_capacity += self.weight


def equip(dude, id):

    item_name = item_data[id]['name']
    type = item_data[id]['item_type']
    if type == 0:
        dude.weapon = item_name
    elif type == 1:
        dude.shield = item_name
    elif type == 2:
        dude.helm = item_name
    elif type == 3:
        dude.chest = item_name
    elif type == 4:
        dude.legs = item_name
    elif type == 5:
        dude.hands = item_name
    elif type == 6:
        dude.feet = item_name
    elif type == 7:
        dude.ring = item_name
    elif type == 8:
        dude.neck = item_name
    else:
        print("something went wrong")

    dude.str += item_data[id]['str']
    dude.int += item_data[id]['int']
    dude.dex += item_data[id]['dex']
    dude.con += item_data[id]['con']
    dude.spd += item_data[id]['spd']

    item_inventory.remove(item_name)


# here player defines his name and what race
# we eventually need to add more races
# as well as add classes
# furthermore, it would be cool if each race gets special bonuses
# and this info needs to be available at the user's request
# so they can type "info" + race and they will get starting stats
def get_char(char):
    global player
    cls()
    name = input("Welcome to the game, please, tell me your name: ")
    print("Hello " + name + " Please select a race\n1. Human\n2. Elf ")
    race = int(input("type in the number you wish to choose: "))
    if race == 1:
        player = char(
            name, "Human", 0, 40, 35, 30, 40, 40, 40, 1, 35, 0, "none", "none", "none",
            "none", "none", "none", "none", "none", "none", 0, 2
          )
        spells.extend((
            spells_data[0]['name'],
            spells_data[1]['name']
        ))
        main(player)
    elif race == 2:
        player = char(name, "Elf", 0, 30, 40, 40, 30, 45, 30, 1.25, 50, 0, "none", "none", "none",
                      "none", "none", "none", "none", "none", "none", 0, 2
                      )
        spells.extend((
            spells_data[0]['name'],
            spells_data[1]['name']
        ))
        main(player)
    else:
        print("you chose improperly")


def speed_option(dude):
    cls()
    print("Here you can choose the speed of the battle dialogue.")
    print("Your currently ")
    print("1. Ludicrous Speed \n2. Fast Speed \n3. Normal Speed \n4. Slow Speed")
    action = input("Enter the number of your choice here: ")
    if action == "1":
        dude.sleep = .5
    elif action == "2":
        dude.sleep = 1
    elif action == "3":
        dude.sleep = 2
    elif action == "4":
        dude.sleep = 3
    else:
        print("you entered a wrong number")
    wait()
    options(dude)


# health and mana are below, don't fuck with this,
# it is unreasonably fragile
def health(dude):
    if dude.current_hp > dude.hp:
        dude.current_hp = dude.hp
    else:
        pass

    hp = dude.current_hp  # Current Health
    max_health = dude.hp  # Max Health
    health_dashes = 10  # Max Displayed dashes

    dash_convert = int(max_health/health_dashes)
    current_dashes = int(hp/dash_convert)
    remaining_health = health_dashes - current_dashes

    health_display = ''.join(['|' for i in range(current_dashes)])
    remaining_display = ''.join([' ' for i in range(remaining_health)])
    # percent = str(int((health/maxHealth)*100)) + "%"
    if dude.current_hp <= 0:
        cprint("[" + health_display + remaining_display + "] " + "0/" + str(int(max_health)), "red")
    elif dude.current_hp <= 5 > 0:
        cprint("[" + health_display + remaining_display + "] " + "!!!", "red")
    else:
        cprint("[" + health_display + remaining_display + "] " + str(int(hp)) + "/" + str(int(max_health)), "red")


def mana(dude):
    if dude.current_mp > dude.mp:
        dude.current_mp = dude.mp
    else:
        pass

    mp = dude.current_mp
    max_mp = dude.mp
    health_dashes = 10

    dash_convert = int(max_mp / health_dashes)
    current_dashes = int(mp / dash_convert)
    remaining_health = health_dashes - current_dashes

    health_display = ''.join(['|' for i in range(current_dashes)])
    remaining_display = ''.join([' ' for i in range(remaining_health)])
    # percent = str(int((health/maxHealth)*100)) + "%"

    if dude.current_hp > 5:
        cprint("[" + health_display + remaining_display + "] " + str(int(mp)) + "/" + str(int(max_mp)), "blue")
    else:
        cprint("[" + health_display + remaining_display + "]!!!", "blue")


# the location will change depending where the player is
# everything is defined in json
# while this works fine it may need some tweaking as time goes on
# ask for more info
class Location:

    def __init__(self, id):

        self.name = location_data[id]['name']

        self.enemy_1 = location_data[id]['enemy'][0]
        self.enemy_2 = location_data[id]['enemy'][1]
        self.enemy_3 = location_data[id]['enemy'][2]
        self.enemy_4 = location_data[id]['enemy'][3]

        self.item_1 = location_data[id]['item'][0]
        self.item_2 = location_data[id]['item'][1]

        self.rand_1 = location_data[id]['rand'][0]
        self.rand_2 = location_data[id]['rand'][1]
        self.rand_3 = location_data[id]['rand'][2]
        self.rand_4 = location_data[id]['rand'][3]
        self.rand_5 = location_data[id]['rand'][4]
        self.rand_6 = location_data[id]['rand'][5]

    def print_loc(self):
        print(self.name)

    def random_number(self):
        return random.randint(0, 100)

    def rand_enc(self):
        x = self.random_number()

        if x <= self.rand_1:
            baddy = Enemy(self.enemy_1)
            encounter(player, baddy)

        elif self.rand_1 < x <= self.rand_2:
            baddy = Enemy(self.enemy_2)
            encounter(player, baddy)

        elif self.rand_2 < x <= self.rand_3:
            baddy = Enemy(self.enemy_3)
            encounter(player, baddy)

        elif self.rand_3 < x <= self.rand_4:
            baddy = Enemy(self.enemy_4)
            encounter(player, baddy)

        elif self.rand_4 < x <= self.rand_5:
            get_item(player, self.item_1)

        elif self.rand_5 < x <= self.rand_6:
            rand_gold(player)

        else:
            print("you fucked up")


# adds an item to a player's inventory without creating
# another instance for it (may be unnecessary)
def get_item(player, x):

    item_name = item_data[x]['name']
    item_disp = item_data[x]['disp']

    cls()
    print(player.name + " found " + item_disp + "!!!")
    # instead of appending the item to the dictionary, I just sent it
    # through the item class, this needs to happen, I am just writing this
    # in case something goes wrong
    Item(x)
    wait()
    main(player)


#    BATTLE PHASES

# first phase, checks if enemy is still above 0 hp and loops
# through the other battle phases
def encounter(player, enemy):
    cls()
    print(player.name + " encountered a " + enemy.nom + "!!!")
    sleep(player.sleep)
    while enemy.current_hp > 0:
        battle(player, enemy)
    else:
        cls()
        stats(player)


# here the player chooses to attack, flee, use an item
# only attack is implemented now.
# need to add spells, items, flee,
# need cooler attacks, weapons, shit like that
def battle(player, enemy):
    cls()
    cprint(enemy.nom)
    health(enemy)
    mana(enemy)
    cprint(enemy.img)
    print("")
    print("")
    print("")
    cprint(player.name)
    health(player)
    mana(player)
    cprint("1. Melee Attack\n2. Magic Attack\n3. Use Item\n4. Run Away")
    action = input("")
    if action == "1":
        do_spd(player, enemy, spell=False)
    elif action == "2":
        do_spd(player, enemy, spell=True)
    elif action == "3":
        use_item(player, enemy)
    elif action == "4":
        run_away(player, enemy)
    else:
        print("you put the input in wrong, try again")
        battle(player, enemy)

def use_item(player, enemy):
    cls()
    print("Capacity: " + str(player.current_capacity) + "/" + str(player.capacity))
    print("ID     ITEM NAME")
    print("_____________________")

    item_list = groupby(sorted(item_inventory))

    for k, g in item_list:
        count = sum(1 for _ in g)
        if count > 1:
            print(k, "(" + str(count) + ")")
        else:
            print(k)

    print("_____________________")
    while True:
        try:
            action = input("Enter the ID of the item you wish to use: ")
            if action.isdigit():
                item_id = int(action)
                item_name = item_data[item_id]['name']
                consumable = item_data[item_id]['consume']
                effect = item_data[item_id]['effect']
                hp = item_data[item_id]['hp']
                mp = item_data[item_id]['mp']
                weight = item_data[item_id]['weight']
                if consumable and item_name in item_inventory:
                    cls()
                    print(effect)
                    player.current_hp = player.current_hp + hp
                    player.current_mp = player.current_mp + mp
                    item_inventory.remove(item_name)
                    player.current_capacity -= weight
                    sleep(player.sleep)
                    enemy_atk(player, enemy)
                elif item_name not in item_inventory:
                    print("you do not own this item!")
                    wait()
                    battle(player, enemy)
                else:
                    print("You cannot do that right now.")
                    wait()
                    battle(player, enemy)
        except IndexError:
            print("You entered an incorrect ID, try again!")
            wait()
            use_item(player, enemy)

def run_away(player, enemy):
    if player.spd >= enemy.spd:
        cls()
        cprint("Ran away successfully!", "green")
        sleep(player.sleep)
        main(player)
    elif enemy.spd > player.spd:
        chance = dice_roll(10, 1)
        if chance > 9:
            cls()
            cprint("Ran away successfully!", 'green')
            sleep(player.sleep)
            main(player)
        else:
            cls()
            cprint("Cannot run away!", 'red')
            sleep(player.sleep)
            enemy_atk(player, enemy)
    else:
        print("there was a problem")
        main(player)

# decides who goes first based on their speed stat
def do_spd(player, enemy, spell):
    if not spell:
        if player.spd > enemy.spd:
            char_atk(player, enemy)
        elif enemy.spd > player.spd:
            enemy_atk(player, enemy)
        elif player.spd == enemy.spd:
            char_atk(player, enemy)
        else:
            print("error with speed")
    if spell:
        if player.spd > enemy.spd:
            char_spell(player, enemy)
        elif enemy.spd > player.spd:
            enemy_atk(player, enemy)
        elif player.spd == enemy.spd:
            char_spell(player, enemy)
        else:
            print("error with speed")


# both char_atk and enemy_atk are self explanatory but need
# to be totally reworked. the variable "damage" needs to
# be more dynamic. an equation based on char's str stat
def char_atk(player, enemy):
    dice_mod = int(player.str/10)
    damage = dice_roll(4, dice_mod)
    cls()
    cprint(player.name + " did " + str(damage) + " damage!!", 'green')
    sleep(player.sleep)
    enemy.current_hp = int(enemy.current_hp - damage)
    if enemy.current_hp <= 0:
        end_encounter(player, enemy)
    else:
        enemy_atk(player, enemy)
        # this needs to be changed
        # will cause problems when enemy is faster...

#do magic attack
def char_spell(player, enemy):
    cls()
    print("ID     SPELL NAME")
    print("_____________________")

    spellList = groupby(sorted(spells))
    for k, g in spellList:
        print(k)
    print("_____________________")

    while True:
        try:
            action = input("What would you like to do? [h]: ")

            if action == "h":
                cls()
                print("To use a spell, simply type in its ID and hit enter"
                      "\n to cancel and return to main battle screen, type 'x'")
                wait()
                char_spell(player, enemy)

            elif action == 'x':
                battle(player, enemy)

            elif action.isdigit():
                action = int(action)
                spell_disp = spells_data[action]['disp']
                spell_name = spells_data[action]['name']
                spell_flavor = spells_data[action]['flavor']
                hp = spells_data[action]['hp']
                mp = spells_data[action]['mp']
                dmg = spells_data[action]['dmg']

                if spell_name in spells:
                    player.current_mp -= mp
                    player.current_hp += hp
                    enemy.current_hp -= dmg
                    cls()
                    cprint(player.name + " used " + spell_disp + "!!", 'blue')
                    cprint(spell_flavor, 'blue')
                    sleep(player.sleep)

                    if enemy.current_hp <= 0:
                        end_encounter(player, enemy)

                    else:
                        enemy_atk(player, enemy)

                elif spell_name not in spells:
                    print("That spell is not in your spell list")
                    wait()
                    char_spell(player, enemy)

                else:
                    print("something went wrong!!")
        except IndexError:
            print("You entered an incorrect ID, try again!")
            wait()
            char_spell(player, enemy)


def enemy_atk(player, enemy):
    # each enemy should have their own melee attack name
    # so it reads "slime pounced and did x dmg!!" or something
    # in order to differentiate between magic and melee
    dice_mod = int(enemy.str/10)
    damage = dice_roll(4, dice_mod)
    player.current_hp = int(player.current_hp - damage)
    health(player)
    cls()
    cprint(enemy.nom + " did " + str(damage) + " melee damage!!", 'red')
    sleep(player.sleep)
    if player.current_hp <= 0:
        print("how did you die to a slime?")
    else:
        battle(player, enemy)


# ends the encounter, checks if player leveled up or not
def end_encounter(player, enemy):
    cls()
    print("Good job, you slaughtered " + enemy.nom + "!!!!!")
    health(enemy)
    sleep(player.sleep)
    cls()
    print("You found " + enemy.item_name)
    sleep(player.sleep)
    enemy.current_hp = enemy.hp
    enemy.current_mp = enemy.mp

    # in this section we are checking whether or not
    # the player has levelled up
    # line 2/3 adds the exp
    # lines 1 and 3 are checked against eachother to see if there is any change
    lvl = bisect.bisect(levels, player.exp) + 1
    player.exp = player.exp + enemy.exp
    check_lvl = bisect.bisect(levels, player.exp) + 1
    if lvl != check_lvl:
        lvl_up(player)
    else:
        pass
    Item(enemy.item_id)
    main(player)


# this is the inventory screen, here players can use the items
# consume, combine, examine.. these words are too much to type
# need to be changed, or given a number
# so player can type 2 to combine, then type the id numbers
# of the items he wishes to combine
def inventory(dude):

    cls()
    print("Capacity: " + str(dude.current_capacity) + "/" + str(dude.capacity))
    print("ID     ITEM NAME")
    print("_____________________")

    item_list = groupby(sorted(item_inventory))

    for k, g in item_list:
        count = sum(1 for _ in g)
        if count > 1:
            print(k, "(" + str(count) + ")")
        else:
            print(k)

    print("_____________________")
    action = input("What would you like to do [h]: ")

    if action == "h":
        cls()
        print("INVENTORY COMMANDS")
        print("Type 1 or 'examine' to examine an item")
        print("Type 2 or 'consume' to consume an item")
        print("Type 3 or 'combine' to combine two items")
        print("type 4 or 'equip' to equip an item")
        print("type 5 or 'equipment' to view or unequip equipped items")
        print("type 6 or 'discard' to discard an item")
        print("Type 0 or 'exit' to return to main menu")
        wait()
        inventory(dude)

    elif action == "exit" or action == '0':
        main(dude)

    elif action == "examine" or action == "1":
        while True:
            try:
                item_id = int(input("Enter the id of the item you would like to examine: "))
                item_name = item_data[item_id]['name']
                item_disp = item_data[item_id]['disp']
                flavor = item_data[item_id]['flavor']
                weight = item_data[item_id]['weight']
                if item_name in item_inventory:
                    cls()
                    print(item_disp)
                    print(flavor)
                    print("weight: " + str(weight))
                    wait()
                    inventory(dude)
                else:
                    print("you either do not have that item, or have entered an incorrect id")
                    wait()
                    inventory(dude)
            except IndexError:
                print("You entered an incorrect ID, try again")
                wait()
                inventory(dude)

    elif action == "consume" or action == '2':
        while True:
            try:
                item_id = int(input("Enter the id of the item you would like to consume: "))
                item_name = item_data[item_id]['name']
                consumable = item_data[item_id]['consume']
                effect = item_data[item_id]['effect']
                hp = item_data[item_id]['hp']
                mp = item_data[item_id]['mp']
                weight = item_data[item_id]['weight']
                if consumable and item_name in item_inventory:
                    cls()
                    print(effect)
                    dude.current_hp = dude.current_hp + hp
                    dude.current_mp = dude.current_mp + mp
                    health(dude)
                    mana(dude)
                    item_inventory.remove(item_name)
                    dude.current_capacity -= weight
                    wait()
                    inventory(dude)
                elif item_name not in item_inventory:
                    print("you do not own this item!")
                    wait()
                    inventory(dude)
                else:
                    print("This item is either not consumable, or not in your inventory")
                    wait()
                    inventory(dude)
            except IndexError:
                print("You entered an incorrect ID, try again")
                wait()
                inventory(dude)

    elif action == "combine" or action == '3':
        while True:
            try:
                item_id = int(input("Enter the id of the first item you would like to combine: "))
                item_name = item_data[item_id]['name']
                item_disp = item_data[item_id]['disp']
                if item_name not in item_inventory:
                    print("You do not own that item")
                    wait()
                    inventory(dude)
                else:
                    pass

                while True:
                    try:
                        other_id = int(input("Enter the id of the second item you would like to combine: "))
                        other_name = item_data[other_id]['name']
                        other_disp = item_data[other_id]['disp']

                        if other_name not in item_inventory:
                            print("You do not own that item")
                            wait()
                            inventory(dude)
                        else:
                            pass

                        combine = item_data[item_id]['combine']
                        other_combine = item_data[other_id]['combine']
                        result_id = item_data[item_id]['result']
                        result_name = item_data[result_id]['name']
                        result_disp = item_data[result_id]['disp']

                        if combine == other_id and other_combine == item_id and (combine and other_combine) and (item_name in item_inventory) and (other_name in item_inventory):
                            cls()
                            print("You combined " + item_disp + " with " + other_disp + " and got " + result_disp + "!!")
                            item_inventory.remove(item_name)
                            item_inventory.remove(other_name)
                            item_inventory.append(result_name)
                            wait()
                            inventory(dude)

                        elif not combine and not other_combine or combine != other_id or other_combine != item_id:
                            print("these item's are not combinable")
                            wait()
                            inventory(dude)
                        else:
                            print("something went wrong, try again!")
                            wait()
                            inventory(dude)

                    except IndexError:
                        print("You entered an incorrect ID, try again")
                        wait()
                        inventory(dude)

            except IndexError:
                print("You entered an incorrect ID, try again")
                wait()
                inventory(dude)

    elif action == "equip" or action == '4':
        while True:
            try:
                item_id = int(input("Enter the id of the item you would like to equip: "))
                item_name = item_data[item_id]['name']
                item_disp = item_data[item_id]['disp']
                equipo = item_data[item_id]['equip']
                if item_name in item_inventory and equipo:
                    equip(player, item_id)
                    print("You equipped " + item_disp)
                    wait()
                    inventory(dude)
                elif item_name not in item_inventory:
                    print("You do not own this item.")
                    wait()
                    inventory(dude)
                elif not equipo:
                    print("This item is not equippable")
                    wait()
                    inventory(dude)
                else:
                    print("you fucked up")
                    wait()
                    inventory(dude)
            except IndexError:
                print("You entered an incorrect ID, try again")
                wait()
                inventory(dude)

    elif action == "equipment" or action == '5':
        equipment(dude)

    elif action == "discard" or action == '6':
        while True:
            try:
                item_id = int(input("Enter the id of the item you would like to discard: "))
                item_name = item_data[item_id]['name']
                item_disp = item_data[item_id]['disp']
                item_weight = item_data[item_id]['weight']
                if item_name in item_inventory:
                    item_inventory.remove(item_name)
                    dude.current_capacity -= item_weight
                    cls()
                    print("You discarded " + item_disp)
                    wait()
                    inventory(dude)
                else:
                    print("You do not own that item!")
                    wait()
                    inventory(dude)
            except IndexError:
                print("You entered an incorrect ID, try again")
                wait()
                inventory(dude)
    else:
        print("choose something else")
        wait()
        inventory(dude)


def equipment(dude):
    cls()
    print("EQUIPMENT")
    print("_____________________")
    print("a. weapon : " + dude.weapon)
    print("b. shield : " + dude.shield)
    print("c. head   : " + dude.helm)
    print("d. chest  : " + dude.chest)
    print("e. legs   : " + dude.legs)
    print("f. hands  : " + dude.hands)
    print("g. feet   : " + dude.feet)
    print("h. ring   : " + dude.ring)
    print("i. neck   : " + dude.neck)
    print("_____________________")
    action = input("1. Unequip Item | 2. Return to Inventory | 3. Return to Main Menu ")
    if action == "1":
        id = input("Enter the LETTER of the equipped area you would like to unequip")
        dequip(player, id)
    elif action == "2":
        inventory(dude)
    elif action == "3":
        main(dude)
    else:
        print("you muffed up")
        equipment(dude)


def dequip(dude, id):

    cls()

    if id == "a":
        match = next(d for d in item_data if d['name'] == dude.weapon)
        item_id = match['id']
        item_inventory.append(dude.weapon)
        print("you unequipped " + dude.weapon)
        dude.weapon = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    elif id == "b":
        match = next(d for d in item_data if d['name'] == dude.shield)
        item_id = match['id']
        item_inventory.append(dude.shield)
        print("you unequipped " + dude.shield)
        dude.shield = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    elif id == "c":
        match = next(d for d in item_data if d['name'] == dude.helm)
        item_id = match['id']
        item_inventory.append(dude.helm)
        print("you unequipped " + dude.helm)
        dude.helm = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    elif id == "d":
        match = next(d for d in item_data if d['name'] == dude.chest)
        item_id = match['id']
        item_inventory.append(dude.chest)
        print("you unequipped " + dude.chest)
        dude.chest = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    elif id == "e":
        match = next(d for d in item_data if d['name'] == dude.legs)
        item_id = match['id']
        item_inventory.append(dude.legs)
        print("you unequipped " + dude.legs)
        dude.legs = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    elif id == "f":
        match = next(d for d in item_data if d['name'] == dude.hands)
        item_id = match['id']
        item_inventory.append(dude.hands)
        print("you unequipped " + dude.hands)
        dude.hands = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    elif id == "g":
        match = next(d for d in item_data if d['name'] == dude.feet)
        item_id = match['id']
        item_inventory.append(dude.feet)
        print("you unequipped " + dude.feet)
        dude.feet = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    elif id == "h":
        match = next(d for d in item_data if d['name'] == dude.ring)
        item_id = match['id']
        item_inventory.append(dude.ring)
        print("you unequipped " + dude.ring)
        dude.ring = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    elif id == "i":
        match = next(d for d in item_data if d['name'] == dude.neck)
        item_id = match['id']
        item_inventory.append(dude.neck)
        print("you unequipped " + dude.neck)
        dude.neck = "none"
        dude.str -= item_data[item_id]['str']
        dude.int -= item_data[item_id]['int']
        dude.dex -= item_data[item_id]['dex']
        dude.con -= item_data[item_id]['con']
        dude.spd -= item_data[item_id]['spd']
    else:
        print("you entered an incorrect key, try again")
    wait()
    equipment(dude)


# displays list of spells out of battle... can only view and delete spells here.
# I would like to add an option for people to have a quick-bar of spells... so 5 spells are always
# readily available for them in battle.... that is to be done at another time.
def spell_list(dude):
    cls()
    print("ID     SPELL NAME")
    print("_____________________")

    for k, g in groupby(sorted(spells)):
            print(k)

    print("_____________________")
    action = input("What would you like to do? [h]: ")
    if action == "h":
        cls()
        print("type '1' or 'examine' to examine a spell."
              "\ntype '2' or 'delete' to delete a spell."
              "\ntype '3' or 'main' to return to the main menu")
        wait()
        spell_list(dude)
    if action == "1" or action == "examine":
        while True:
            try:
                id = int(input("Enter the ID of the spell you want to examine: "))
                spell_name = spells_data[id]['name']
                if spell_name in spells:
                    cls()
                    print(spells_data[id]['examine'])
                elif spell_name not in spells:
                    cls()
                    print("This spell is not in your spell list.")
                else:
                    print("try again!")
                wait()
                spell_list(dude)

            except IndexError:
                print("you input an incorrect ID, try again.")
                wait()
                spell_list(dude)

    elif action == "2" or action == "delete":
        while True:
            try:
                id = int(input("Enter the ID of the spell you would like to delete: "))
                spell_name = spells_data[id]['name']
                disp_name = spells_data[id]['disp']
                if spell_name in spells:
                    spells.remove(spell_name)
                    cls()
                    print("You successfully deleted " + disp_name)
                elif spell_name not in spells:
                    print("This spell is not in your spell list.")
                else:
                    print("try again!")
                wait()
                spell_list(dude)

            except IndexError:
                print("you input an incorrect ID, try again.")
                wait()
                spell_list(dude)

    elif action == "3" or action == "main":
        main(dude)
    else:
        print("Try Again")
        spell_list(dude)



# shows the stats of the character, it is self explanatory
def stats(dude):
    cls()
    print("STATS")
    print("_____________________")
    print(dude.name)
    print("lvl:  " + str(get_level(dude)))
    print("exp:  " + str(dude.exp))
    print("race: " + str(dude.race))
    health(dude)
    mana(dude)
    print("str:  " + str(dude.str))
    print("int:  " + str(dude.int))
    print("dex:  " + str(dude.dex))
    print("con:  " + str(dude.con))
    print("spd:  " + str(dude.spd))
    print("_____________________")
    input("press Enter to return to main menu ")
    main(dude)


# screen to make sure they want to quit the game
def exit_screen(dude):
    cls()
    exit_q = yn("Are you sure you would like to quit?")
    if exit_q:
        exit()
    else:
        main(dude)

def load_all(dude):
    global player, item_inventory, spells
    cls()
    item_inventory = load("inv_save.sav")
    spells = load("spell_save.sav")
    c = load("char_save.sav")
    player = dude(
        c.name, c.race, c.exp, c.str, c.int, c.dex, c.con, c.spd, c.current_hp, c.mp_bonus, c.current_mp,
        c.gold, c.weapon, c.shield, c.helm, c.chest, c.legs, c.hands, c.feet, c.ring, c.neck, c.current_capacity,
        c.sleep
    )

    cls()
    print("Load Complete")
    wait()
    main(player)


# options to save, load, and quit, will add more as they
# are needed
def options(dude):
    global player

    cls()
    print("OPTIONS")
    print("_____________________")
    print("1. Save Game")
    print("2. Load Game")
    print("3. Speed Options")
    print("4. Return to Main Menu")
    print("0. Quit Game")
    print("_____________________")
    select = input("please type in the corresponding letter or number: ")

    if select == "1":
        player.save()
        inv_save()
        spell_save()
        cls()
        print("Save Complete")
        wait()
        main(dude)
    elif select == "2":
        load_all(dude)
    elif select == "3":
        speed_option(dude)
    elif select == "4":
        main(dude)
    elif select == "0":
        exit_screen(dude)
    else:
        print("you chose the wrong key")
        wait()
        options(dude)

def rand_gold(dude):
    chance = dice_roll(100, 1)
    if chance <= 80:
        cls()
        cprint("You Found 10 Gold!", "yellow")
        player.gold += 10
    elif 80 < chance <= 90:
        cls()
        cprint("You Found 100 Gold !!!", "yellow")
        player.gold += 100
    elif 90 < chance <= 95:
        cls()
        cprint("You Found 500 Gold !!!!!!!", "yellow")
        player.gold += 500
    else:
        cls()
        cprint("You lost 10 gold!!")
        player.gold -= 10
        if player.gold < 0:
            player.gold = 0
        else:
            pass
    wait()
    main(dude)



# main screen where player chooses what to do
def main(dude):
    dude.update()
    global player
    cls()
    print("MAIN MENU")
    print("_____________________")
    print(dude.name)
    print("lvl:  " + str(get_level(dude)))
    print("exp:  " + str(dude.exp) + "/" + str(exp_until(dude)))
    print("race: " + str(dude.race))
    print("gold: " + str(dude.gold))
    health(dude)
    mana(dude)
    print("1. Explore   | 2. Stats     | 3. Spells \n4. Inventory | 5. Equipment | 6. Options")
    print("_____________________")
    select = input("Please type in the corresponding number: ")

    if select == "2":
        stats(dude)
    elif select == "4":
        inventory(dude)
    elif select == "1":
        first_forest = Location(0)
        first_forest.rand_enc()
    elif select == "3":
        spell_list(dude)
    elif select == "5":
        equipment(dude)
    elif select == "6":
        options(dude)
    else:
        print("you chose the wrong key")
        wait()
        main(dude)


# the main start screen before the game starts
def start_screen(char):
    global player
    cls()
    print("THIS GAME HAS NO TITLE YET!")
    print("_____________________")
    print("1. Start New Game")
    print("2. Load Saved Game")
    print("3. Exit")

    select = input("Please type in the corresponding number: ")

    if select == "1":
        get_char(char)
    elif select == "2":
        load_all(char)
    elif select == "3":
        exit()
    else:
        print("you chose the wrong key")
        wait()
        start_screen(char)


start_screen(Char)


'''
TODO:

Fix str as attack

chance to miss when attacking

effects.json

implement map system

items need to have value

'''

