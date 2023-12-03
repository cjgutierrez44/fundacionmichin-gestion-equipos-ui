import {setList, functions, execBackFunction, execFetch} from './functions-controller.mjs';

const TEMPS_CLEANING_BTN = document.getElementById('temps_cleaning_btn');
const UPDATES_INSTALLER_BTN = document.getElementById('updates_installer_btn');
const SITES_BLOCKER_MODAL_BTN = document.getElementById('sites_blocker_modal_btn');
const SITES_BLOCKER_ADD_BTN = document.getElementById('sites_blocker_add_btn');
const SITES_BLOCKER_BTN = document.getElementById('sites_blocker_btn');
const GENERIC_RADIO_BUTTON = document.getElementById("option1");
const CUSTOM_RADIO_BUTTON = document.getElementById("option2");

TEMPS_CLEANING_BTN.addEventListener('click', async function(e){
	await execBackFunction(e, functions.TEMPS_CLEANING, 'Limpiando temporales');
});

UPDATES_INSTALLER_BTN.addEventListener('click', async function(e){
	await execBackFunction(e, functions.UPDATES_INSTALLER, 'Instalando actualizaciones');
});


SITES_BLOCKER_MODAL_BTN.addEventListener('click', async function(e){
	const list = await execFetch('/site_blocker/custom', 'GET');
	refheshBlockedSitesTable(list)
});

SITES_BLOCKER_ADD_BTN.addEventListener('click', async function(e){
	const BLOCK_URL_INPUT = document.getElementById('siteToBlock');
	const queryParams = {
	    site: BLOCK_URL_INPUT.value
	};
	console.log(queryParams);
	await execFetch('/site_blocker/custom', 'PUT', queryParams);
	const list = await execFetch('/site_blocker/custom', 'GET');
	refheshBlockedSitesTable(list)
	BLOCK_URL_INPUT.value = ''
});


SITES_BLOCKER_BTN.addEventListener('click', async function(e){

	let list = '';

	if(GENERIC_RADIO_BUTTON.checked){
		list = 'GENERIC';
	}

	if(CUSTOM_RADIO_BUTTON.checked){
		list = 'CUSTOM';
	}

	setList(list)

	await execBackFunction(e, functions.SITE_BLOCKER, 'Bloqueando sitios');
});

function refheshBlockedSitesTable(list){
	const BANNED_SITES_TABLE_BODY = document.getElementById('bannedSitesTBody');
	BANNED_SITES_TABLE_BODY.innerHTML = '';
	list.forEach(site =>{
		const newSite = document.createElement('tr');
		newSite.innerHTML = `<td>${site}</td>
		<td><button class="delete-site-btn ${site} btn btn-outline-danger border-0 rounded fs-3"><i class="bi bi-trash"></i></button></td>`;
		BANNED_SITES_TABLE_BODY.appendChild(newSite);
	});
	const SITES_BLOCKER_DELETE_BTNS = document.getElementsByClassName('delete-site-btn');

	Array.from(SITES_BLOCKER_DELETE_BTNS).forEach(btn =>{
		btn.addEventListener('click', async function(e) {
			console.log("HOLA");
			let deleteSite = '';
			if(e.target.tagName == 'I'){
				deleteSite = e.target.parentElement.classList[1], e.target.parentElement.classList[2];
			}else {
				deleteSite = e.target.classList[1], e.target.classList[2];
			}
			const queryParams = {
				site: deleteSite
			};
			await execFetch('/site_blocker/custom', 'DELETE', queryParams);
			const list = await execFetch('/site_blocker/custom', 'GET');
			refheshBlockedSitesTable(list)
		});
	});

}

GENERIC_RADIO_BUTTON.addEventListener("change", function () {
    if (this.checked) {
        document.getElementById('generic-list').classList.remove('d-none');
        document.getElementById('custom-list').classList.add('d-none');
    }
});

CUSTOM_RADIO_BUTTON.addEventListener("change", function () {
    if (this.checked) {
            document.getElementById('generic-list').classList.add('d-none');
        	document.getElementById('custom-list').classList.remove('d-none');
    }
});