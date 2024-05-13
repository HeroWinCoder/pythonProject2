import classes.field as field
import classes.dispenser as dispenser

field = field.Field(5, 5, 3)
field.add_dispenser(dispenser.Dispenser([1, 1, 1], 5, 10, [1, 0, 0]))
field.add_dispenser(dispenser.Dispenser([1, 3, 1], 5, 10, [1, 1, 1]))
field.add_dispenser(dispenser.Dispenser([3, 1, 0], 5, 10, [0, 1, 0]))
field.add_dispenser(dispenser.Dispenser([3, 3, 1], 5, 10, [1, 0, 0]))
field.set_field_settings(100, 1, 2, 500)
field.show_field()