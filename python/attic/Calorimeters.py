import Units

class Calorimeter:
    # Working volume of cell.
    cell_volume = None

# Define the VP-ITC calorimeter.
VPITC = Calorimeter()
VPITC.cell_volume = 1.4301 * Units.ml

