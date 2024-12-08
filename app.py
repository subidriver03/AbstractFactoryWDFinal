"""
Which structure/algorithm/pattern have I chosen?
------------------------------------------------
I have chosen the Abstract Factory design pattern.

What does this project aim to demonstrate or solve?
---------------------------------------------------
This project demonstrates how the Abstract Factory design pattern can be used to create families 
of related objects—in this case, different types of game characters (enemies) and their respective 
weapons—without specifying their concrete classes directly.

When would this design fail to meet expectations?
--------------------------------------------------
1. If the variety of products becomes too large and complex, it might be cumbersome to maintain.
2. If dynamic addition/removal of products at runtime is needed, this pattern may be too rigid.
3. If performance and memory are critical, overhead from object hierarchies may be too high.

When would this design exceed expectations?
-------------------------------------------
1. In modular systems where different teams work on separate families of related objects.
2. When the set of products is known and can benefit from clean decoupled code.
3. In scenarios with multiple "themes" or "worlds" each needing a unique set of related objects.
"""

from abc import ABC, abstractmethod
from flask import Flask, jsonify, request, render_template_string
import random

app = Flask(__name__)

class Enemy(ABC):
    @abstractmethod
    def attack(self):
        pass

class Weapon(ABC):
    @abstractmethod
    def use(self):
        pass

class Orc(Enemy):
    def attack(self):
        return "Orc attacks with brute force!"

class Troll(Enemy):
    def attack(self):
        return "Troll smashes its club down on you!"

class Elf(Enemy):
    def attack(self):
        return "Elf shoots a volley of arrows!"

class Dwarf(Enemy):
    def attack(self):
        return "Dwarf swings a mighty hammer, striking with solid precision!"

class Dragon(Enemy):
    def attack(self):
        return "Dragon unleashes a torrent of fire from its maw!"

class Goblin(Enemy):
    def attack(self):
        return "Goblin darts forward, slashing quickly with a rusty blade!"

class OrcWeapon(Weapon):
    def use(self):
        return "You swing a crude but heavy axe!"

class TrollWeapon(Weapon):
    def use(self):
        return "You lift a massive club overhead!"

class ElfWeapon(Weapon):
    def use(self):
        return "You draw a slender longbow!"

class DwarfWeapon(Weapon):
    def use(self):
        return "You heft a finely forged hammer, perfect for crushing skulls!"

class DragonWeapon(Weapon):
    def use(self):
        return "You channel fiery breath, scorching all in your path!"

class GoblinWeapon(Weapon):
    def use(self):
        return "You brandish a jagged dagger, small but deadly!"

class EnemyFactory(ABC):
    @abstractmethod
    def create_enemy(self) -> Enemy:
        pass

    @abstractmethod
    def create_weapon(self) -> Weapon:
        pass

class OrcFactory(EnemyFactory):
    def create_enemy(self) -> Enemy:
        return Orc()
    def create_weapon(self) -> Weapon:
        return OrcWeapon()

class TrollFactory(EnemyFactory):
    def create_enemy(self) -> Enemy:
        return Troll()
    def create_weapon(self) -> Weapon:
        return TrollWeapon()

class ElfFactory(EnemyFactory):
    def create_enemy(self) -> Enemy:
        return Elf()
    def create_weapon(self) -> Weapon:
        return ElfWeapon()

class DwarfFactory(EnemyFactory):
    def create_enemy(self) -> Enemy:
        return Dwarf()
    def create_weapon(self) -> Weapon:
        return DwarfWeapon()

class DragonFactory(EnemyFactory):
    def create_enemy(self) -> Enemy:
        return Dragon()
    def create_weapon(self) -> Weapon:
        return DragonWeapon()

class GoblinFactory(EnemyFactory):
    def create_enemy(self) -> Enemy:
        return Goblin()
    def create_weapon(self) -> Weapon:
        return GoblinWeapon()

factories = [
    OrcFactory(), 
    TrollFactory(), 
    ElfFactory(), 
    DwarfFactory(),
    DragonFactory(),
    GoblinFactory()
]

page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/> 
    <title>Abstract Factory Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        #results { margin-top: 20px; }
        button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Abstract Factory Demo</h1>
    <p>This page demonstrates the Abstract Factory pattern by randomly selecting an enemy and weapon from a broader selection when you click the button below.</p>
    <button id="roll-button">Roll for Enemy and Weapon</button>
    <div id="results"></div>

    <script>
        const button = document.getElementById('roll-button');
        const resultsDiv = document.getElementById('results');

        button.addEventListener('click', () => {
            fetch('/random_enemy')
                .then(response => response.json())
                .then(data => {
                    resultsDiv.innerHTML = `
                        <h2>Results</h2>
                        <p><strong>Enemy Attack:</strong> ${data.enemy_attack}</p>
                        <p><strong>Weapon Use:</strong> ${data.weapon_use}</p>
                    `;
                })
                .catch(err => {
                    resultsDiv.innerHTML = '<p style="color:red;">An error occurred.</p>';
                    console.error(err);
                });
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(page_html)

@app.route("/random_enemy")
def random_enemy():
    factory = random.choice(factories)
    enemy = factory.create_enemy()
    weapon = factory.create_weapon()

    return jsonify({
        "enemy_attack": enemy.attack(),
        "weapon_use": weapon.use()
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
