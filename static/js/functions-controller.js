const TEMPS_CLEANING_BTN = document.getElementById('temps_cleaning_btn');

TEMPS_CLEANING_BTN.addEventListener('click', function(e){
	execBackFunction(e, functions.TEMPS_CLEANING)
});

functions = {
	'TEMPS_CLEANING': '/temps_cleaning'
}

function execBackFunction(e, url){
	const ORIGINAL_TEXT = e.target.innerText
	setLoaderOnButton(e.target, "Limpiando temporales");
	fetch(url).then(response => {
		if (response.ok) {
			
			const contentType = response.headers.get('content-type');
			if (contentType && contentType.includes('application/json')) {
				return response.json();
			} else {
				mostrarToast('OK', 'Trabajo terminado. (pensar algo mejor)');
			}
		} else {
			mostrarToast('ERR', 'Ha ocurrido un error durante el proceso, intentelo mas tarde.');
		}
		resetButtonText(e.target, ORIGINAL_TEXT);
	})
	.then(data => {
		console.log('Datos obtenidos:', data);
	})
	.catch(error => {
		console.error('Error:', error.message);
	});
}

function setLoaderOnButton(button, text){
	button.innerHTML = text + ' <span id="loader" class="spinner-border spinner-border-sm" ></span>';
	button.disabled = true;
}

function resetButtonText(button, text){
	button.innerText = text;
	button.disabled = false;
}


function mostrarToast(type, text) {
	var toast = document.getElementById('miToast');
	toast.innerHTML = text;
	toast.classList.add('show');
	if (type == 'OK') {
		toast.classList.add('alert-success');
	}else if (type == 'ERR'){
		toast.classList.add('alert-danger');
	}else{
		toast.classList.add('alert-info');
	}
	
	setTimeout(function() {
		toast.classList.remove('show');
	}, 2500);
}
