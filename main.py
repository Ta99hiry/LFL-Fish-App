from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from math import ceil

FCR = 1.4
POIDS_SAC = 25

def get_phase(pm):
    if pm <= 4:
        return "Small", 10
    elif pm <= 20:
        return "Big", 6
    else:
        return "Grower", 3


class AppLFL(App):

    def build(self):

        self.cages = []

        layout = BoxLayout(orientation="vertical")

        self.cage = TextInput(hint_text="Numéro cage")
        self.pm = TextInput(hint_text="PM (g)")
        self.nb = TextInput(hint_text="Nombre poissons")
        self.sem = TextInput(hint_text="Semaines")

        self.result = Label(text="Résultat")

        btn_add = Button(text="Ajouter cage")
        btn_add.bind(on_press=self.add)

        btn_calc = Button(text="Calculer")
        btn_calc.bind(on_press=self.calc)

        layout.add_widget(self.cage)
        layout.add_widget(self.pm)
        layout.add_widget(self.nb)
        layout.add_widget(btn_add)
        layout.add_widget(self.sem)
        layout.add_widget(btn_calc)
        layout.add_widget(self.result)

        return layout

    def add(self, instance):

        self.cages.append(
            (self.cage.text, float(self.pm.text), int(self.nb.text))
        )
        self.result.text = "Cage ajoutée ✔"

    def calc(self, instance):

        semaines = int(self.sem.text)
        total = ""

        stock = {}

        for cage, pm, n in self.cages:

            total += f"\nCage {cage}\n"

            poids = pm

            for s in range(semaines):

                type_alim, taux = get_phase(poids)

                ration = (poids * n / 1000) * (taux / 100)
                kg = ration * 7

                stock[type_alim] = stock.get(type_alim, 0) + kg

                total += f"S{s+1} | {poids:.1f}g | {ration:.2f} kg/j\n"

                poids += (kg * FCR * 1000 / n)

        total += "\nSTOCK:\n"

        for k, v in stock.items():
            total += f"{k}: {v:.1f} kg ({ceil(v/POIDS_SAC)} sacs)\n"

        self.result.text = total


AppLFL().run()

