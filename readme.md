Comando para ejecutar en powershell como administrador en las máquinas destino
New-NetFirewallRule -DisplayName "Permitir IP Mantenimiento" -Direction Inbound -Action Allow -Protocol Any -RemoteAddress 192.168.1.100

New-LocalUser -Name support -Password (ConvertTo-SecureString -AsPlainText "support12345" -Force) -AccountNeverExpires -UserMayNotChangePassword

Add-LocalGroupMember -Group "Administrators" -Member support


set-netconnectionprofile -networkcategory private
winrm set winrm/config/service '@{AllowUnencrypted="true"}'