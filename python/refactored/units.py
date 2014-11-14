from pint import UnitRegistry
ureg = UnitRegistry()
Quantity = ureg.Quantity

ureg.define('molar = 1 * mole / liter = M')