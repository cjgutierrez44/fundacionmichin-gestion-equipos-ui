let functions = {
	'TEMPS_CLEANING': '/temps_cleaning',
	'UPDATES_INSTALLER': '/updates_installer',
	'UPDATE_PC': '/updates_installer/',
	'LOAD_UPDATES': '/updates_inventory/re_scan',
	'UNINSTALL_APP': '/app_uninstaller',
	'SITE_BLOCKER': '/site_blocker'
}

function setHostUpdate(host){
	functions.UPDATE_PC = "/updates_installer/pc/" + host;
}

function setAppUninstall(host, appId){
	functions.UNINSTALL_APP = "/app_uninstaller/host/" + host + "/app_id/" + appId;
}

async function execBackFunction(e, url, btnText) {
    const ORIGINAL_TEXT = e.target.innerHTML;
    if(e.target.tagName == 'I'){
    	setLoaderOnButton(e.target.parentElement, btnText);
    }else {
    	setLoaderOnButton(e.target, btnText);
    }
    try {
        const response = await fetch(url);
        const data = await response.json();
        mostrarToast(data['status_code'], data['response']);
    } catch (error) {
        console.error('Error:', error);
    } finally {
        resetButtonText(e.target, ORIGINAL_TEXT);
    }
}

function setLoaderOnButton(button, text){
	button.innerHTML = text + ' <span id="loader" class="spinner-border spinner-border-sm" ></span>';
	button.disabled = true;
}

function resetButtonText(button, text){
	button.innerHTML = text;
	button.disabled = false;
}


function mostrarToast(type, text) {
	var toast = document.getElementById('miToast');
	toast.innerHTML = text;
	toast.classList.remove('alert-success', 'alert-danger', 'alert-info');
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


export {setHostUpdate, setAppUninstall, functions, execBackFunction};

