from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "dev-key"

# app code

class Character:
    def __init__(self):
        self.points_pool = 27
        self.proficiency = 2 #Proficiency modifier, starts at +2
        
        self.abilities = {
            "strenght": 0,
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




def get_character():
    if "character" not in session:
        session["character"] = Character().to_dict()
    return session["character"]

def save_character(char_dict):
    session["character"] = char_dict




# =======================
# Render pages
# =======================

@app.route("/")
def index():
    character = get_character()
    return render_template("abilities.html", character=character)

@app.route("/increase", methods=["POST"])
def increase():
    ability = request.json.get("ability")

    char = Character()
    char.__dict__.update(get_character())

    char.increase(ability)
    save_character(char.to_dict())

    return jsonify(char.to_dict())

@app.route("/decrease", methods=["POST"])
def decrease():
    ability = request.json.get("ability")

    char = Character()
    char.__dict__.update(get_character())

    char.decrease(ability)
    save_character(char.to_dict())

    return jsonify(char.to_dict())


if __name__ == "__main__":
    app.run()