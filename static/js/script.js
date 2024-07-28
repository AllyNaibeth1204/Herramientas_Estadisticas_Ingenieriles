document.addEventListener('DOMContentLoaded', function() {

    const botonInicio = document.getElementById('miBotoninicial');
    //function 
       if(botonInicio) {
        botonInicio.addEventListener('click', function() {
             window.location.href = 'http://127.0.0.1:5000/seleccion'; // Redirigir al archivo seleccion.htm
       });
}




const inputField = document.getElementById('inputDato');
const dropdownList = document.getElementById('listaDatos');
const dropdownContainer = document.querySelector('.dropdown-container');
const btnAgregar = document.getElementById('btnAgregar');
const btnEnviar = document.getElementById('btnEnviar');
const dataForm = document.getElementById('dataForm');
const resultadoMedia = document.getElementById('resultadoMedia');
const resultadoModa = document.getElementById('resultadoModa');
const resultadoMediana = document.getElementById('resultadoMediana');

let data = [];
const maxVisibleItems = 15; // Número máximo de elementos visibles en la lista

inputField.addEventListener('input', () => {
  // No hacer nada en este evento, solo se agregará el dato al hacer clic en el botón "Agregar"
});

function add_data(){
  const inputValue = inputField.value.trim();
  if (inputValue !== '') {
    data.push(inputValue);
    updateDropdownList();
    showDropdown();
    inputField.value = '';
  }
}

if (btnAgregar){ 
btnAgregar.addEventListener('click', add_data);
}

inputField.addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault(); // Evita que se envíe el formulario si existe
    add_data();
}
});

if(btnEnviar){
   btnEnviar.addEventListener('click', function() {
       if (data.length === 0) {
            alert('Por favor, agrega algunos datos antes de enviar.');
            return;
        }
        fetch('/submit_data', {
            method: 'POST',
            headers: {
                  'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(responseData => {
          if (responseData.status === 'success') {
            console.log('Datos recibidos por el servidor:', responseData);
                alert('Datos enviados con éxito');
                //mostrar la media y moda
                resultadoMedia.textContent = `Media: ${data.mean}`;
                resultadoModa.textContent = `Moda: ${Array.isArray(data.mode) ? data.mode.join(', ') : data.mode}`;
                resultadoMediana.textContent = `Mediana: ${data.median}`;
                
            } else {
                console.error('Error en la respuesta del servidor:', responseData);
            }
         })
         .catch(error => console.error('Error al enviar los datos:', error));
      });

    }
  
function updateDropdownList() {
  dropdownList.innerHTML = '';
  const startIndex = Math.max(data.length - maxVisibleItems, 0);
  for (let i = startIndex; i < data.length; i++) {
    const listItem = document.createElement('li');
    listItem.textContent = data[i];
    dropdownList.appendChild(listItem);
  }
}

function showDropdown() {
  dropdownContainer.style.display = 'block';
}

function hideDropdown() {
  dropdownContainer.style.display = 'none';
}

//Seccion de las imagenes
  const image = document.getElementById('histo');
  if(image){
     let isEnlarged = false;

     image.addEventListener('click', () => {
        image.classList.toggle('enlarged-size');
        image.classList.toggle('original-size');
        isEnlarged = !isEnlarged;
      });
   }

});


document.addEventListener('DOMContentLoaded', function() {
  const image = document.getElementById('histo');
  if(image){
     let isEnlarged = false;

     image.addEventListener('click', () => {
        image.classList.toggle('enlarged-size');
        image.classList.toggle('original-size');
        image.classList.toggle('centered');
        isEnlarged = !isEnlarged;
      });
   }
});

document.addEventListener('DOMContentLoaded', function() {
  const image = document.getElementById('poli');
  if(image){
     let isEnlarged = false;

     image.addEventListener('click', () => {
        image.classList.toggle('enlarged-size');
        image.classList.toggle('original-size');
        image.classList.toggle('centered');
        isEnlarged = !isEnlarged;
      });
   }
});

document.addEventListener('DOMContentLoaded', function() {
  const image = document.getElementById('asc');
  if(image){
     let isEnlarged = false;

     image.addEventListener('click', () => {
        image.classList.toggle('enlarged-size');
        image.classList.toggle('original-size');
        image.classList.toggle('centered');
        isEnlarged = !isEnlarged;
      });
   }
});

document.addEventListener('DOMContentLoaded', function() {
  const image = document.getElementById('des');
  if(image){
     let isEnlarged = false;

     image.addEventListener('click', () => {
        image.classList.toggle('enlarged-size');
        image.classList.toggle('original-size');
        image.classList.toggle('centered');
        isEnlarged = !isEnlarged;
      });
   }
});