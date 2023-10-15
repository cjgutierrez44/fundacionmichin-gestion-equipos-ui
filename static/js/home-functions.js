import {functions, execBackFunction} from './functions-controller.js';

const TEMPS_CLEANING_BTN = document.getElementById('temps_cleaning_btn');
const UPDATES_INSTALLER_BTN = document.getElementById('updates_installer_btn');
const SITES_BLOCKER_BTN = document.getElementById('sites_blocker_btn');

TEMPS_CLEANING_BTN.addEventListener('click', async function(e){
	await execBackFunction(e, functions.TEMPS_CLEANING, 'Limpiando temporales');
});

UPDATES_INSTALLER_BTN.addEventListener('click', async function(e){
	await execBackFunction(e, functions.UPDATES_INSTALLER, 'Instalando actualizaciones');
});

SITES_BLOCKER_BTN.addEventListener('click', async function(e){
	await execBackFunction(e, functions.SITE_BLOCKER, 'Bloqueando sitios');
});