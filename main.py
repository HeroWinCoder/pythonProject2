import classes.field as field
import classes.dispenser as dispenser

field = field.Field(20, 10)
field.add_dispenser(dispenser.Dispenser([5, 5], 300, 30, [3, 0]))
field.add_dispenser(dispenser.Dispenser([0, 9], 100, 30, [0, -1]))
# field.add_dispenser(dispenser.Dispenser([9, 0], 30, 1, [0, 1]))
# field.add_dispenser(dispenser.Dispenser([9, 9], 30, 1, [-1, 0]))
field.set_field_settings(10000, 0.8, 2)
field.simulate()
# field.show_field()
