from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "dev-key"


# Character class
class Character:
    def __init__(self):
        self.points_pool = 1 #for testing set to one. set 27 in production
        self.proficiency = 2 #Proficiency modifier, starts at +2
        
        self.race = None
        self.char_class = None
        self.background = None

        self.abilities = {
            #Testing / set to 0 in production
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10
        }

        self.skills = {
            "acrobatics": False,
            "animal_handling": False,
            "arcana": False,
            "athletics": False,
            "deception": False,
            "history": False,
            "insight": False,
            "intimidation": False,
            "investigation": False,
            "medicine": False,
            "nature": False,
            "perception": False,
            "performance": False,
            "persuasion": False,
            "religion": False,
            "sleight_of_hand": False,
            "stealth": False,
            "survival": False
        }
    
    def increase(self, ability):
        if self.points_pool > 0: #If there are points available
            self.abilities[ability] += 1 #Increase selected ability by 1
            self.points_pool -= 1 #Reduce available points by 1
    
    def decrease(self, ability):
        if self.abilities[ability] > 0: #If selected ability is not 0
            self.abilities[ability] -= 1 #Reduce selected ability by 1
            self.points_pool += 1 #Increase available points by 1

    def calculate_modifiers(self):
        self.modifiers = {}
        for ability, score in self.abilities.items():
            self.modifiers[ability] = (score - 10) // 2

    def calculate_skill_bonuses(self):
        skill_bonuses = {}

        for skill, ability in SKILLS.items():
            mod = self.modifiers.get(ability, 0)
            proficient = self.skills.get(skill, False)
            bonus = mod + (self.proficiency if proficient else 0)
            skill_bonuses[skill] = bonus

        return skill_bonuses

    def apply_background(self, background_data):
        for prof in background_data.get("proficiencies", []):
            self.skills[prof] = True

    @classmethod
    def from_dict(cls, data):
        c = cls()
        c.points_pool = data.get("points_pool", 27)
        c.proficiency = data.get("proficiency", c.proficiency)
        c.race = data.get("race")
        c.char_class = data.get("char_class")
        c.background = data.get("background")
        c.abilities = data.get("abilities", {}).copy()
        c.skills = data.get("skills", {}).copy()
        return c

    def to_dict(self):
        return {
            "abilities": self.abilities,
            "points_pool": self.points_pool,
            "proficiency": self.proficiency,
            "race": self.race,
            "char_class": self.char_class,
            "background": self.background,
            "skills": self.skills
        }
#============ End Character Class ============



#============ Libraries ============
RACES = {
    "human": {
        "name": "Human",
        "description": "Human description.",
        "traits": [
            "Trait#1: traitdescription.",
            "Trait#2: traitdescription."
        ],
        "modifiers": {
            "strength": 1,
            "dexterity": 1,
            "constitution": 1,
            "intelligence": 1,
            "wisdom": 1,
            "charisma": 1
        }
    },

    "elf": {
        "name": "Elf",
        "description": "Elf description.",
        "traits": [
            "Trait#1: traitdescription.",
            "Trait#2: traitdescription."
        ],
        "modifiers": {
            "dexterity": 2
        }
    },

    "dwarf": {
        "name": "Dwarf",
        "description": "dwarf description.",
        "traits": [
            "Trait#1: traitdescription.",
            "Trait#2: traitdescription."
        ],
        "modifiers": {
            "constitution": 2
        }
    }
}

CLASSES = {
    "fighter": {
        "name": "Fighter",
        "description": "Masters of martial combat, skilled with weapons and armor.",
        "primary_abilities": ["strength", "constitution"],
        "saving_throws": ["strength", "constitution"],
        "hit_die": 10,
        "skill_choices": 2,
        "skill_list": [
            "acrobatics",
            "animal_handling",
            "athletics",
            "history",
            "insight",
            "intimidation",
            "perception",
            "survival"
        ],
        "spellcaster": False,
        "spellbook": None,
        "spell_slots": None
    },

    "rogue": {
        "name": "Rogue",
        "description": "Stealthy experts who excel at precision, agility, and cunning.",
        "primary_abilities": ["dexterity", "intelligence"],
        "saving_throws": ["dexterity", "intelligence"],
        "hit_die": 8,
        "skill_choices": 4,
        "skill_list": [
            "acrobatics",
            "athletics",
            "deception",
            "insight",
            "intimidation",
            "investigation",
            "perception",
            "performance",
            "persuasion",
            "sleight_of_hand",
            "stealth"
        ],
        "spellcaster": False,
        "spellbook": None,
        "spell_slots": None
    },

    "wizard": {
        "name": "Wizard",
        "description": "Scholars of arcane magic who rely on intellect and study.",
        "primary_abilities": ["intelligence"],
        "saving_throws": ["intelligence", "wisdom"],
        "hit_die": 6,
        "skill_choices": 2,
        "skill_list": [
            "arcana",
            "history",
            "insight",
            "investigation",
            "medicine",
            "religion",
        ],
        "spellcaster": True,
        "spellbook": "WIZARD_SPELLBOOK",
        "spell_slots": 2
    }
}

SKILLS = {
    "acrobatics": "dexterity",
    "animal_handling": "wisdom",
    "arcana": "intelligence",
    "athletics": "strength",
    "deception": "charisma",
    "history": "intelligence",
    "insight": "wisdom",
    "intimidation": "charisma",
    "investigation": "intelligence",
    "medicine": "wisdom",
    "nature": "intelligence",
    "perception": "wisdom",
    "performance": "charisma",
    "persuasion": "charisma",
    "religion": "intelligence",
    "sleight_of_hand": "dexterity",
    "stealth": "dexterity",
    "survival": "wisdom"
}

BACKGROUNDS = {
    "acolyte": {
        "name": "Acolyte",
        "description": "Acolyte description.",
        "proficiencies": ["insight", "religion"]
    },

    "criminal": {
        "name": "Criminal",
        "description": "Criminal description.",
        "proficiencies": ["deception", "stealth"]
    },

    "folk_hero": {
        "name": "Folk Hero",
        "description": "Folk Hero description.",
        "proficiencies": ["animal_handling", "survival"]
    },

    "noble": {
        "name": "Noble",
        "description": "Noble description.",
        "proficiencies": ["history", "persuasion"]
    },

    "sage": {
        "name": "Sage",
        "description": "Sage description.",
        "proficiencies": ["arcana", "history"]
    },

    "soldier": {
        "name": "Soldier",
        "description": "Soldier description.",
        "proficiencies": ["athletics", "intimidation"]
    }
}



# Spellbook libraries
WIZARD_SPELLBOOK = {
    "cantrips": [
        {
            "name": "Fire Bolt",
            "description": "You hurl a mote of fire at a creature or object within range.",
            "casting_time": "1 action",
            "range": "120 feet",
            "components": "V, S",
            "duration": "Instantaneous"
        },
        {
            "name": "Mage Hand",
            "description": "A spectral, floating hand appears at a point you choose within range.",
            "casting_time": "1 action",
            "range": "30 feet",
            "components": "V, S",
            "duration": "1 minute"
        }
    ],
    "level_1": [
        {
            "name": "Magic Missile",
            "description": "You create three glowing darts of magical force.",
            "casting_time": "1 action",
            "range": "120 feet",
            "components": "V, S",
            "duration": "Instantaneous"
        },
        {
            "name": "Shield",
            "description": "An invisible barrier of magical force appears and protects you.",
            "casting_time": "1 reaction",
            "range": "Self",
            "components": "V, S",
            "duration": "1 round"
        }
    ]
}



def get_character():
    if "character" not in session:
        session["character"] = Character().to_dict()
    return session["character"]

def save_character(char_dict):
    session["character"] = char_dict




# =======================
# RENDER Pages
# =======================

@app.route("/") #Render the landing page
def index():
    character = get_character()
    return render_template("abilities.html", character=character, races=RACES, classes=CLASSES)

@app.route("/skills") #Render skills selection page
def skills():
    sheet = session.get("character_sheet", {})
    class_data = CLASSES.get(sheet.get("class"), {})

    return render_template(
        "skills.html",
        sheet=sheet,
        skills=SKILLS,
        allowed_skills=class_data.get("skill_list", []),
        max_choices=class_data.get("skill_choices", 0)
    )

@app.route("/background") #Render the background selection page
def background():
    return render_template("background.html", backgrounds=BACKGROUNDS)

@app.route("/index")
def home():
    sheet = build_character_sheet()
    if sheet is None:
        sheet = {}
    return render_template("index.html", sheet=sheet)

@app.route("/dice")
def dice():
    return render_template("dice.html")

@app.route("/spellbook")
def spellbook_page():
    sheet = session.get("character_sheet", {})
    spellbook_name = sheet.get("spellbook")

    # Load the correct spellbook dict
    spellbook = globals().get(spellbook_name, {})

    return render_template("spellbook.html", spellbook=spellbook)


# =======================
# ROUTES
# =======================

@app.route("/increase", methods=["POST"]) #Increase ability
def increase():
    ability = request.json.get("ability")

    char = Character()
    char.__dict__.update(get_character())

    char.increase(ability)
    save_character(char.to_dict())

    return jsonify(char.to_dict())

@app.route("/decrease", methods=["POST"]) #Decrease ability
def decrease():
    ability = request.json.get("ability")

    char = Character()
    char.__dict__.update(get_character())

    char.decrease(ability)
    save_character(char.to_dict())

    return jsonify(char.to_dict())

@app.route("/select_race", methods=["POST"]) #Select and store race
def select_race():
    race = request.json.get("race")

    char = Character()
    char.__dict__.update(get_character())

    char.race = race
    save_character(char.to_dict())

    race_data = RACES.get(race, {})

    return jsonify({
        "race": race,
        "description": race_data.get("description", ""),
        "traits": race_data.get("traits", []),
        "modifiers": race_data.get("modifiers", {})
    })

@app.route("/select_class", methods=["POST"]) #Select and store class
def select_class():
    class_name = request.json.get("class")

    char = Character()
    char.__dict__.update(get_character())

    char.char_class = class_name
    save_character(char.to_dict())

    class_data = CLASSES.get(class_name, {})

    return jsonify({
        "class": class_name,
        "description": class_data.get("description", ""),
        "primary_abilities": class_data.get("primary_abilities", []),
        "saving_throws": class_data.get("saving_throws", []),
        "hit_die": class_data.get("hit_die", None),
        "spellcaster": class_data.get("spellcaster", False),
        "spellbook": class_data.get("spellbook", None)
    })

#Check first page is ready to proceed
@app.route("/is_ready", methods=["GET"])
def is_ready():
    char = get_character()

    race_ok = bool(char.get("race"))
    class_ok = bool(char.get("char_class"))
    points_ok = char.get("points_pool", 0) == 0

    return jsonify({
        "ready": race_ok and class_ok and points_ok,
        "race_ok": race_ok,
        "class_ok": class_ok,
        "points_ok": points_ok
    })

#Build complete character sheet
def build_character_sheet():
    char_data = get_character()
    if not char_data:
        return None

    character = Character.from_dict(char_data)

    # Apply race modifiers
    race_data = RACES.get(character.race, {})
    race_mods = race_data.get("modifiers", {})

    final_abilities = {}
    for ability, score in character.abilities.items():
        final_abilities[ability] = score + race_mods.get(ability, 0)

    character.abilities = final_abilities
    character.calculate_modifiers()

    # Background
    background_key = character.background
    background_data = BACKGROUNDS.get(background_key, {})
    character.apply_background(background_data)

    # Skills
    skill_bonuses = character.calculate_skill_bonuses()

    # Class
    class_data = CLASSES.get(character.char_class, {})

    # Calculate hit points
    hit_die = class_data.get("hit_die", 0)
    con_mod = character.modifiers.get("constitution", 0)
    max_hp = hit_die + con_mod

    # Spellcasting stats, if any
    if class_data.get("spellcaster"):
        spell_ability = class_data["primary_abilities"][0]  # e.g. "intelligence"
        spell_mod = character.modifiers.get(spell_ability, 0)

        spell_save_dc = 8 + character.proficiency + spell_mod
        spell_attack_bonus = character.proficiency + spell_mod
    else:
        spell_ability = None
        spell_mod = None
        spell_save_dc = None
        spell_attack_bonus = None

    character_sheet = {
        "race": character.race,
        "race_name": race_data.get("name", ""),
        "class": character.char_class,
        "class_name": class_data.get("name", ""),
        "spellcaster": class_data.get("spellcaster", False),
        "spellbook": class_data.get("spellbook", None),
        "spell_slots_used": 0,
        "max_spell_slots": class_data.get("spell_slots", None),
        "spellcasting_ability": spell_ability,
        "spell_save_dc": spell_save_dc,
        "spell_attack_bonus": spell_attack_bonus,
        "abilities": final_abilities,
        "ability_modifiers": character.modifiers,
        "skill_proficiencies": character.skills,
        "skills": skill_bonuses,
        "hit_die": class_data.get("hit_die"),
        "hit_dice_used": 0,
        "death_rolls": 0,
        "max_hp": max_hp,
        "current_hp": max_hp,
        "primary_abilities": class_data.get("primary_abilities", []),
        "saving_throws": class_data.get("saving_throws", []),
        "traits": race_data.get("traits", []),
        "description": {
            "race": race_data.get("description", ""),
            "class": class_data.get("description", "")
        },
        "background": background_key,
        "background_name": background_data.get("name", ""),
        "background_description": background_data.get("description", ""),
        "background_proficiencies": background_data.get("proficiencies", []),
    }

    session["character_sheet"] = character_sheet
    return character_sheet


#Commit abilities.html to character
@app.route("/commit_character", methods=["POST"])
def commit_character():
    sheet = build_character_sheet()
    if sheet is None:
        return jsonify({"success": False, "error": "No character in session"})
    return jsonify({"success": True})


# Add the skills to the character sheet
@app.route("/set_skills", methods=["POST"])
def set_skills():
    data = request.json
    selected_skills = data.get("skills", [])

    character = session.get("character")
    if not character:
        return {"success": False, "error": "No character in session"}

    # Ensure skills dict exists
    skills = character.get("skills", {})

    # Reset all skills
    for skill in skills:
        skills[skill] = False

    # Apply selected skills
    for skill in selected_skills:
        if skill in skills:
            skills[skill] = True

    character["skills"] = skills
    session["character"] = character

    print("DEBUG SET_SKILLS:", character["skills"])  # TEMP DEBUG
    print("RECEIVED FROM FRONTEND:", selected_skills)

    return {"success": True}



@app.route("/background_ready")
def background_ready():
    char = get_character()
    if not char:
        return jsonify({"ready": False})

    background = char["background"] if isinstance(char, dict) else char.background

    return jsonify({"ready": bool(background)})



@app.route("/set_background", methods=["POST"])
def set_background():
    data = request.get_json()
    selected = data.get("background")

    if not selected or selected not in BACKGROUNDS:
        return jsonify({"success": False, "error": "Invalid background"})

    char = get_character()
    if not char:
        return jsonify({"success": False, "error": "No character in session"})

    # Handle both dict and Character object
    if isinstance(char, dict):
        char["background"] = selected
    else:
        char.background = selected
        char = char.to_dict()  # normalize for session storage

    session["character"] = char

    print("SET_BACKGROUND:", get_character())

    return jsonify({"success": True})

# Adjust character health
@app.route("/hp/<action>", methods=["POST"])
def modify_hp(action):
    sheet = session.get("character_sheet", {})

    current = sheet.get("current_hp", 0)
    max_hp = sheet.get("max_hp", 0)

    if action == "up":
        current = min(current + 1, max_hp)
    elif action == "down":
        current = max(current - 1, 0)

    sheet["current_hp"] = current
    session["character_sheet"] = sheet

    return {"current_hp": current, "max_hp": max_hp}

# Track the character's hit dice useage.
@app.route("/hitdice/update", methods=["POST"])
def update_hitdice():
    sheet = session.get("character_sheet", {})

    count = int(request.json.get("count", 0))
    # clamp between 0 and 3 for now — can be scaled for levels
    count = max(0, min(count, 3))

    sheet["hit_dice_used"] = count
    session["character_sheet"] = sheet

    return {"hit_dice_used": count}

# Track the character's death rolls.
@app.route("/deathroll/update", methods=["POST"])
def update_deathroll():
    sheet = session.get("character_sheet", {})

    count = int(request.json.get("count", 0))
    count = max(0, min(count, 3))  # clamp 0–3 - max amount of death rolls is always 3.

    sheet["death_rolls"] = count
    session["character_sheet"] = sheet

    return {"death_rolls": count}

# Track spellcaster's spell slots
@app.route("/spellslots/update", methods=["POST"])
def update_spellslots():
    sheet = session.get("character_sheet", {})

    max_slots = sheet.get("max_spell_slots")
    if max_slots is None:
        return {"error": "Class has no spell slots"}, 400

    try:
        count = int(request.json.get("count"))
    except (TypeError, ValueError):
        return {"error": "Invalid count"}, 400

    # clamp
    count = max(0, min(count, max_slots))

    sheet["spell_slots_used"] = count
    session["character_sheet"] = sheet

    return {"spell_slots_used": count}




if __name__ == "__main__":
    app.run()