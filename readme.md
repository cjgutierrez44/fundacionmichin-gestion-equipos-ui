# MichinTechCare 

MichinTechCare es una aplicación para hacer mantenimiento preventivo de equipos windows de forma remota en entornos donde no existe un directorio activo con el que se pueda hacer administración remota y automatizada de los equipos de la red.
## Autores ✒️
* **Cristhian Gutierrez** - *Desarrollo* - [CjGutierrez44](https://github.com/cjgutierrez44)
* **Javier Garay Morales** - *Desarrollo* - [GarayJavier](https://github.com/GarayJavier)
* **Acuña**
* **Lee**
* **Alejandro Pineda**- *Desarrollo* - [Snikrs](https://github.com/snikrs)
* **Brayan**
* **Santiago**
### Versiones📋
_Esta versión solo ha sido probada y certificada para sistemas operativos:_

```
Microsoft Windows 10
Microsoft Windows 11
```

## Restricciones para su funcionamiento 🚀
_Para el correcto funcionamiento de este software se debe tener las siguientes consideraciones_
*_Los equipos a intervenir deben estar dentro del mismo segmento de red, (compartir la misma mascara de red)_

*_Los equipos ha intervenir deben contar con un usuario local con privilegios de administrador y agregarlo al grupo de administradores, se sugiere crear uno con los comandos siguientes_
```PowerShell
New-LocalUser -Name support -Password (ConvertTo-SecureString -AsPlainText "supportpassword" -Force) -AccountNeverExpires -UserMayNotChangePassword -PasswordNeverExpires
Add-LocalGroupMember -Group "Administrators" -Member support
Add-LocalGroupMember -Group "Administradores" -Member support
```

*_Se debe agregar la ip de la máquina desde donde se ejecuta a la lista blanca del firewall de cada equipo ha intervenir_
```PowerShell
New-NetFirewallRule -DisplayName "Permitir IP Mantenimiento" -Direction Inbound -Action Allow -Protocol Any -RemoteAddress 192.168.1.100
```
*_Se debe habilitar en cada equipo a intervenir PowerShell Remoting (WinRM) para poderlos controlar de forma remota._
_Además se debe configurar los metodos de autenticación, y agregar a la lista de confianza la ip del host que ejecuta_
```PowerShell
Enable-PSRemoting -Force
set-netconnectionprofile -networkcategory private
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set winrm/config/service/auth '@{Basic="true"}'
Set-Item WSMan:\localhost\Client\TrustedHosts -Value 192.168.1.100
```
*_Es recomendable activar el máximo nivel de protección de cuentas de usuario para que notifique siempre que se quiera instalar alguna aplicación_
```PowerShell
Set-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Value 2
```
# Funcionalidades

+ ## Listar equipos en la red

Hace un escaneo de la red en busca de equipos con sitema operativo Windows, cuando se ejecuta por primera vez utiliza [nmap](https://pypi.org/project/python-nmap/) para recorrer todo el segmento de red, al finalizar guarda dentro de la carpeta database en un archivo cuyo nombre es la primer ip del segmento; la ip y el hostname de cada equipo encontrado. De ahí en adelante cualquier otro llamado y de existir el archivo creado en el primer llamado devolverá la lista de equipos que se encuentre en el, por lo tanto para actualizar o realizar nuevos escaneos es necesario eliminar este fichero.

+ ## Listar aplicaciones por equipo

Por cada equipo identificado con la funcionalidad anterior lista todas las aplicaciones instaladas en él excluyendo las que contengan la palabra Microsoft. Si se llama por primera vez, hara el escaneo con el uso de [pywinrm](https://pypi.org/project/pywinrm/) al finalizar guardará en la carpeta database un archivo cuyo nombre es la primer ip del segmento más 'app' el nombre y el id de la aplicación. De ahí en adelante cualquier otro llamado y de existir el archivo creado en el primer llamado devolverá la lista de equipos que se encuentre en el, por lo tanto para actualizar o realizar nuevos escaneos es necesario eliminar este fichero.
