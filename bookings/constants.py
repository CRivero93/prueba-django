import datetime

select_dates       = "Por favor, primero seleccione una fecha y habitación para la reserva"
phone_format       = "El teléfono debe tener el formato: '655223344'."
no_rooms_available = "No se encontraron habitaciones disponibles"
limit_date         = datetime.datetime(2020, 12, 31).date()
NGUESTS_CHOICES    = [
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
]
ROOM_TYPE_CHOICES  = [
    ('INDIVIDUAL', 'Individual'),
    ('DOBLE', 'Doble'),
    ('TRIPLE', 'Triple'),
    ('CUADRUPLE', 'Cuádruple'),
]