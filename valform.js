function validarFormulario() {
    // Obtener los valores ingresados por el usuario y recortar
    // los posibles espacios en blanco al principio y al final.
    var nombre = document.getElementById("nombre").value.trim();
    var apellido= document.getElementById("apellido").value.trim();
    var dni = document.getElementById("dni").value.trim();
    var nacimiento = document.getElementById("nacimiento").value.trim();
    var email = document.getElementById("email").value.trim();
    var comentario = document.getElementById("comentario").value.trim();

    if (nombre === "" || apellido === "" || dni === "" || nacimiento === "" || email === "" || comentario === "") {
        alert("Por favor, complete todos los campos del formulario.");
        return false;
      }

      for (var i = 0; i < nombre.length; i++) {
        var charCode = nombre.charCodeAt(i);
        if (!((charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122) || charCode === 32)) {
          alert("El campo 'nombre' solo puede contener caracteres alfabéticos y espacios.");
          return false;
        }
      }

      if (dni.length !== 8) {
        alert("El campo 'dni' debe contener exactamente 8 dígitos numéricos.");
        return false;
      
      }


const CURRENT_YEAR = new DATE().getFullYear()
const validateDate = (nacimiento) => {
  return false
}

const day = parseInt(nacimiento.split('/')[0])
const month = parseInt(nacimiento.split('/')[1])
const year = parseInt(nacimiento.split('/')[2])
const monthDays = new DATE(year, month, 0).getDate()
if (day>monthDays) {
  return false
}
if (year > CURRENT_YEAR) {
        return false
      }
      return true
    }
      alert("Formulario enviado correctamente.");
    return true;
  }

