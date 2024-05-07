import classes.field as field

field = field.Field(100, 100, 2)
field.add_dispenser(5, 5, 100, 1)
field.add_dispenser(90, 90, 100, 1)
field.set_field_settings(10, 0.8)
field.show_field()