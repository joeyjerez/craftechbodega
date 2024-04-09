/* Función de hora actual */
function showTime() {
    //Creando objeto Date para obtener la fecha y hora
    var fecha = new Date();

    //Arrays creadas para mostrar el día y mes
    var nombreDias = new Array("Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado");
    var nombreMes = new Array("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre");
    var min = validaTiempo(fecha.getMinutes());
    var seg = validaTiempo(fecha.getSeconds());

    var dia = `${nombreDias[fecha.getDay()]} ${fecha.getDate()} de ${nombreMes[fecha.getMonth()]} del ${fecha.getFullYear()}`;
    var hora = `${validaTiempo(fecha.getHours())}:${min}:${seg}`;
    document.getElementById('tiempo').innerHTML = `${hora}  |  ${dia}`;
    setTimeout(function () { showTime() }, 1000);
};

//Valida la hora para no tener horas y minutos en un solo dígito. Ej: (9:4) => (09:04)
function validaTiempo(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
};
/* Fin Función de hora actual */

/* Switch de Tema Oscuro */
//// Declarando Elementos
// const htmlBody = document.body;
// const htmlCards = document.getElementsByClassName('card');
// const htmlTables = document.getElementById('table');
// const htmlLinks = document.getElementsByClassName('link');
// const themeSwitch = document.querySelector('#themeSwitch');

//Cambiar tema claro a oscuro
// themeSwitch.addEventListener('click', () => {
//     //Para cambiar el tema del fondo y las cards
//     htmlBody.classList.toggle("dark-mode");
//     if (htmlCards != null) {
//         for (let i = 0; i < htmlCards.length; i++) {
//             htmlCards[i].classList.toggle("bg-dark");
//         }
//     }

//     if (htmlLinks != null) {
//         for (let i = 0; i < htmlLinks.length; i++) {
//             htmlLinks[i].classList.toggle("text-white");
//             htmlLinks[i].classList.toggle("text-dark");
//         }
//     }

//     if (htmlTables != null) {
//         htmlTables.classList.toggle("border-white");
//         htmlTables.classList.toggle("table-dark");
//     }

//     //Para guardar el estado de tema entre páginas
//     if (htmlBody.classList.contains('dark-mode')) {
//         localStorage.setItem('dark-mode', 'true');
//     } else {
//         localStorage.setItem('dark-mode', 'false');
//     }
// })

//Verificador de estado de tema
// if (localStorage.getItem('dark-mode') === 'true') {
//     htmlBody.classList.add('dark-mode');

//     if (htmlCards != null) {
//         for (let i = 0; i < htmlCards.length; i++) {
//             htmlCards[i].classList.add("bg-dark");
//         }
//     }

//     if (htmlLinks != null) {
//         for (let i = 0; i < htmlLinks.length; i++) {
//             htmlLinks[i].classList.remove("text-dark");
//             htmlLinks[i].classList.add("text-white");
//         }
//     }

//     if (htmlTables != null) {
//         htmlTables.classList.add("border-white");
//         htmlTables.classList.add("table-dark");
//     }

//     $(themeSwitch).prop('checked', true);
// } else {
//     htmlBody.classList.remove('dark-mode');

//     if (htmlCards != null) {
//         for (let i = 0; i < htmlCards.length; i++) {
//             htmlCards[i].classList.remove("bg-dark");
//         }
//     }

//     if (htmlLinks != null) {
//         for (let i = 0; i < htmlLinks.length; i++) {
//             htmlLinks[i].classList.remove("text-light");
//             htmlLinks[i].classList.add("text-dark");
//         }
//     }

//     if (htmlTables != null) {
//         htmlTables.classList.remove("border-white");
//         htmlTables.classList.remove("table-dark");
//     }

//     $(themeSwitch).prop('checked', false);
// }
/* Fin Switch de Tema Oscuro */

function CharacterCounter() {
    var text_max = 200;
    $('#count_message').html('0 / ' + text_max);

    $('#text').on("keyup", function () {
        var text_length = $('#text').val().length;
        var text_remaining = text_max - text_length;

        $('#count_message').html(text_length + ' / ' + text_max);
    });
}