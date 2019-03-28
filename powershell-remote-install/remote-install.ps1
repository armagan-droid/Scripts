$file = 'C:\salt-agents\Salt-Minion-Py3-AMD64-Setup.exe'

$computers = @("10.1.0.10", "10.1.0.11", "10.1.0.12")

$user = ""administrator"
$password = ConvertTo-SecureString "coksikretbirzifre" -AsPlainText -Force

$cred = New-Object System.Management.Automation.PSCredential ($user,$password)

foreach ($computerName in $computers) {
    Set-Item WSMan:\localhost\Client\TrustedHosts -Value $computerName -Force
    $session = New-PSSession -ComputerName $computerName -Credential $cred
    Copy-Item -Path $file -ToSession $session -Destination 'c:\windows\temp\Salt-Minion-Py3-AMD64-Setup.exe'
    
    $hostname=hostname
    Invoke-Command -Session $session -ScriptBlock {
        Start-Process c:\windows\temp\Salt-Minion-Py3-AMD64-Setup.exe -ArgumentList "/S /minion-name=`"$hostname`"  /master=10.57.0.56 /start-service=1" -Wait
    }
    Invoke-Command -Session $session -ScriptBlock {
        Get-Service "salt*"
    }
    Remove-PSSession $session
    
}
