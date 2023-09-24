# MichinTechCare 

MichinTechCare es una aplicación para hacer mantenimiento preventivo de equipos windows de forma remota en entornos donde no existe un directorio activo con el que se pueda hacer administración remota y automatizada de los equipos de la red.

Fue desarrollado para uso exclusivo de la fundación Michin por:

## Restricciones para su funcionamiento 🚀
_Para el correcto funcionamiento de este software se debe tener las siguientes consideraciones_

### Versiones📋
_Esta versión solo ha sido probada y certificada para sistemas operativos:_

```
Microsoft Windows 10
Microsoft Windows 11
```

Comando para ejecutar en powershell como administrador en las máquinas destino
New-NetFirewallRule -DisplayName "Permitir IP Mantenimiento" -Direction Inbound -Action Allow -Protocol Any -RemoteAddress 192.168.1.100

New-LocalUser -Name support -Password (ConvertTo-SecureString -AsPlainText "support12345" -Force) -AccountNeverExpires -UserMayNotChangePassword

Add-LocalGroupMember -Group "Administrators" -Member support


set-netconnectionprofile -networkcategory private
winrm set winrm/config/service '@{AllowUnencrypted="true"}'