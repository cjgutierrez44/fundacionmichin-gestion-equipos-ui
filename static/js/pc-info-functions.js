import {setHostUpdate, setAppUninstall, functions, execBackFunction} from './functions-controller.js';

const UPDATE_PC_BTN = document.getElementById('update_pc_btn');
const LOAD_UPDATES_BTN = document.getElementById('load_updates_btn');
const UNINSTALL_APPS_BTNS = document.getElementsByClassName('uninstall-app-btn');

UPDATE_PC_BTN.addEventListener('click', async function (e) {
    setHostUpdate(e.target.classList[0]);
    await execBackFunction(e, functions.UPDATE_PC, 'Actualizando equipo');
});

LOAD_UPDATES_BTN.addEventListener('click', async function (e) {
    await execBackFunction(e, functions.LOAD_UPDATES, '');
    window.location.reload();
});


Array.from(UNINSTALL_APPS_BTNS).forEach(btn =>{
	btn.addEventListener('click', async function(e) {
			if(e.target.tagName == 'I'){
				setAppUninstall(e.target.parentElement.classList[1], e.target.parentElement.classList[2].replace('{', '').replace('}', ''));
			}else {
				setAppUninstall(e.target.classList[1], e.target.classList[2].replace('{', '').replace('}', ''));
			}
			await execBackFunction(e, functions.UNINSTALL_APP, '');
		});
});

