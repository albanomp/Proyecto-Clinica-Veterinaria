## VETERINARIA

### Mascota
- nombre: string
- especie: string
- raza: string
- fecha_nacimiento: int
- chip: booleano
- cliente_id: int

### Cliente
- nombre: string
- telefono: string
- email: string
- direccion: string

### Veterinario
- nombre: string
- numero_colegiado: string
- especialidad: string
- telefono: string

### Cita
- fecha_hora: datetime
- motivo: string
- veterinario_id: int
- mascota_id: int

### Tratamiento
- costo: float
- tipo: string/enum
- descripcion: string
- duracion: string
- ingreso: boolean
- cita_id: int

