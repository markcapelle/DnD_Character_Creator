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

    def to_dict(self):
        return {
            "abilities": self.abilities,
            "points_pool": self.points_pool,
            "proficiency": self.proficiency,
            "race": self.race,
            "char_class": self.char_class
        }
#============ End Character Class ============



#============ Libraries ============
RACES = {
    "human": {
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
        "description": "Masters of martial combat, skilled with weapons and armor.",
        "primary_abilities": ["strength", "constitution"],
        "saving_throws": ["strength", "constitution"],
        "hit_die": 10,
        "skill_choices": 2,
        "skill_list": [
            "acrobatics",
            "athletics",
            "history",
            "insight",
            "intimidation",
            "perception",
            "survival"
        ]
    },

    "rogue": {
        "description": "Stealthy experts who excel at precision, agility, and cunning.",
        "primary_abilities": ["dexterity", "intelligence"],
        "saving_throws": ["dexterity", "intelligence"],
        "hit_die": 8
    },

    "wizard": {
        "description": "Scholars of arcane magic who rely on intellect and study.",
        "primary_abilities": ["intelligence"],
        "saving_throws": ["intelligence", "wisdom"],
        "hit_die": 6
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
    return render_template("abilities.html", character=character)

@app.route("/skills")
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


@app.route("/index") #Render the finished character sheet
def home():
    sheet = session.get("character_sheet", {})
    return render_template("index.html", sheet=sheet)


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
        "hit_die": class_data.get("hit_die", None)
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

#Commit abilities.html to character
@app.route("/commit_character", methods=["POST"])
def commit_character():
    char = get_character()

    race = char.get("race")
    char_class = char.get("char_class")
    abilities = char.get("abilities", {})

    # Apply race modifiers
    race_data = RACES.get(race, {})
    race_mods = race_data.get("modifiers", {})

    final_abilities = {}
    for ability, score in abilities.items():
        final_abilities[ability] = score + race_mods.get(ability, 0)

    # Calculate ability modifiers
    ability_mods = {}
    for ability, score in final_abilities.items():
        ability_mods[ability] = (score - 10) // 2

    # Class data
    class_data = CLASSES.get(char_class, {})

    # --- Build character sheet ---
    character_sheet = {
        "race": race,
        "class": char_class,
        "abilities": final_abilities,
        "ability_modifiers": ability_mods,
        "hit_die": class_data.get("hit_die"),
        "primary_abilities": class_data.get("primary_abilities", []),
        "saving_throws": class_data.get("saving_throws", []),
        "traits": race_data.get("traits", []),
        "description": {
            "race": race_data.get("description", ""),
            "class": class_data.get("description", "")
        }
    }

    session["character_sheet"] = character_sheet

    return jsonify({"success": True})




if __name__ == "__main__":
    app.run()