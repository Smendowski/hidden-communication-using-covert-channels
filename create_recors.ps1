$out = '"'; $i = 1; get-content .\ships_64.txt | foreach { [char[]] $_ | foreach { if ($i -le 255){$out = $out + "$_"} else{$i=1; $out = $out + '" "'};  $i =$i+1} }; $out = $out + '"'

Write-Output $out