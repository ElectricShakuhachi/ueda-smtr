import os

class UedaSmtrTemplateHandler():
    def __init__(self, path_to_template_dir: str, logger):
        self._path_to_template_dir = path_to_template_dir
        self._logger = logger

    def form_category_to_template_dict(self, categories: list) -> dict:
        """Returns a dict with each sheet music category template mapped to given category name

        Args:
            categories (list): list of sheet music categories being generated

        Returns:
            dict: Category name to a list of tuples (<path to jinja template>, repeats) (0 repeats means as many as needed)
        """
        cat_to_temps = {}
        for category in categories:
            schema_filename = f"{category}_schema.csv"
            schema_file = os.path.join(self._path_to_template_dir, schema_filename)
            with open(schema_file, "r") as f:
                cat_to_temps[category] = []
                for line in f.readlines():
                    templ, repeats = line.split(";") # will consider 0 repeats to mean as many as necessary
                    texfile = templ + "_ol.tex.j2"
                    cat_to_temps[category].append((texfile, repeats))
        return cat_to_temps
