import json
import os
import shutil
import sys

import requests


class MaterialBuilder:
    def __init__(self):
        self.clean = []

        self.config: dict | None = None
        self.i18n: dict | None = None
        self.materials: list[list[str]] = []

        self.raw_url = "https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/$minecraft/$i18n"
        self.api_url = "https://api.github.com/repos/InventivetalentDev/minecraft-assets/git/trees/$minecraft?recursive=1"

    def run_tasks(self):
        print("> Building...")
        self.prepare()
        self.load_config()
        self.download_i18n()
        self.map_materials()
        self.build_file()
        self.cleanup()
        print("> Finished")

    def load_config(self):
        print("> Loading configuration...")
        self.config = json.load(open("configuration.json", "r"))
        self.config_has_key("minecraft")
        self.config_has_key("i18n")
        self.config_has_key("i18n_start")
        self.config_has_key("package")
        self.config_has_key("class")

        print(f"Minecraft: {self.config['minecraft']}")

    def config_has_key(self, key: str):
        if self.config.get(key) is None:
            print(f"Failed to load configuration: missing key '{key}'")
            sys.exit()

    def config_replace(self, replace: str):
        for key in self.config:
            if not isinstance(self.config[key], str):
                continue

            replace = replace.replace(f"${key}", self.config[key])
        return replace

    def prepare(self):
        print("> Preparing...")
        os.mkdir("temp")

        self.clean.append("temp")

    def download_i18n(self):
        print("> Downloading i18n...")

        url = self.config_replace(self.raw_url)
        print(f"Downloading from '{url}'")

        req = requests.get(url)
        open("temp/lang.json", "wb").write(req.content)

        self.load_i18n()

    def load_i18n(self):
        print("Loading i18n...")
        self.i18n = json.load(open("temp/lang.json", "r"))

    def map_materials(self):
        print(f"> Mapping materials")

        for key in self.i18n.keys():
            for starter in self.config["i18n_start"]:
                if key.startswith(starter):
                    material_lone = key.replace(starter, "")

                    # If the name isn't purely the item, skip
                    if "." in material_lone:
                        continue

                    self.materials.append([material_lone, key])

    def build_file(self):
        print("> Building file...")

        if os.path.exists("out"):
            print("Deleting 'out'")
            shutil.rmtree("out")

        os.mkdir("out")
        preset = open("preset.java", "r").read()
        preset = self.config_replace(preset)

        print("Creating material enums")

        materials = []
        for material in self.materials:
            materials.append(
                f"{material[0].upper()}(Material.create(Identifier.minecraft(\"{material[0]}\")), \"{self.i18n.get(material[1])}\")")

        materials_str = ",\n\t".join(materials)
        with open(f"out/{self.config['class']}.java", "w") as file:
            file.write(preset.replace("$materials", materials_str))

    def cleanup(self):
        print("> Cleaning...")
        for rm in self.clean:
            print(f"Deleting '{rm}'")
            shutil.rmtree(rm)


if __name__ == "__main__":
    builder = MaterialBuilder()
    builder.run_tasks()
