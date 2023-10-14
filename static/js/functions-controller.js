const TEMPS_CLEANING_BTN = document.getElementById('temps_cleaning_btn');
const UPDATES_INSTALLER_BTN = document.getElementById('updates_installer_btn');

TEMPS_CLEANING_BTN.addEventListener('click', function(e){
	execBackFunction(e, functions.TEMPS_CLEANING, 'Limpiando temporales');
});

UPDATES_INSTALLER_BTN.addEventListener('click', function(e){
	execBackFunction(e, functions.UPDATES_INSTALLER, 'Instalando actualizaciones');
});

functions = {
	'TEMPS_CLEANING': '/temps_cleaning',
	'UPDATES_INSTALLER': '/updates_installer'
}

function execBackFunction(e, url, btnText){
	const ORIGINAL_TEXT = e.target.innerText
	setLoaderOnButton(e.target, btnText);
	fetch(url).then(response => {
		return response.json();
	})
	.then(data => {
		mostrarToast(data['status_code'], data['response']);
	}).finally(()=>{
		resetButtonText(e.target, ORIGINAL_TEXT);
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
	toast.classList.remove('alert-success');
	toast.classList.remove('alert-danger');
	toast.classList.remove('alert-info');
	toast.classList.add('show');
	if (type == 200) {
		toast.classList.add('alert-success');
	}else if (type == 500){
		toast.classList.add('alert-danger');
	}else{
		toast.classList.add('alert-info');
	}
	
	setTimeout(function() {
		toast.classList.remove('show');
	}, 2500);
}
