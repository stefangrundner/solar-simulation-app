class Grid:
    def __init__(self):
        self.total_import = 0
        self.total_export = 0

    def import_energy(self, kwh):
        self.total_import += kwh

    def export_energy(self, kwh):
        self.total_export += kwh