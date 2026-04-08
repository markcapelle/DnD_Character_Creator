from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "dev-key"

# app code

class Character:
    def __init__(self):
        self.points_pool = 27
        self.proficiency = 2 #Proficiency modifier, starts at +2
        
        self.abilities = {
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0
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
            "proficiency": self.proficiency
        }
#============ End Character Class ============

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




def get_character():
    if "character" not in session:
        session["character"] = Character().to_dict()
    return session["character"]

def save_character(char_dict):
    session["character"] = char_dict




# =======================
# ROUTES
# =======================

@app.route("/") #Render the landing page
def index():
    character = get_character()
    return render_template("abilities.html", character=character)

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

@app.route("/select_race", methods=["POST"])
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


if __name__ == "__main__":
    app.run()