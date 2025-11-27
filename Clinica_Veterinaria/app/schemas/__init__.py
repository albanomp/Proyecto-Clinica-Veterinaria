from app.schemas.mascota import RespuestaMascota, CrearMascota, ParcheMascota, ActualizarMascota
from app.schemas.veterinario import RespuestaVeterinario, CrearVeterinario, ParcheVeterinario, ActualizarVeterinario
from app.schemas.Duenyo import DuenyoResponse, DuenyoCreate, DuenyoUpdate, DuenyoPatch
from app.schemas.Tratamiento import TipoTratamiento, TratamientoCreate, TratamientoUpdate, TratamientoPatch, TratamientoResponse

__all__=["RespuestaMascota", "CrearMascota", "ParcheMascota", "ActualizarMascota", "RespuestaVeterinario", "CrearVeterinario", "ParcheVeterinario",
        "ActualizarVeterinario", "DuenyoResponse", "DuenyoCreate", "DuenyoUpdate", "DuenyoPatch", "TipoTratamiento", "TratamientoCreate",
        "TratamientoUpdate", "TratamientoPatch", "TratamientoResponse"]

