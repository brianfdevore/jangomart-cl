<html>
<title> JangoMart Customer Loyalty Portal </title>
<body style="margin-top: 100px;">
<h1 style="color: orange;">
<center>
JangoMart Customer Loyalty Portal V3
</center>
</h1>
<h2>
<center>
    Server IP:&nbsp;
<?php
$eip = file_get_contents('http://169.254.169.254/latest/meta-data/local-ipv4');
echo $eip;
?>
<br />
   Region:&nbsp;
<?php
$region = file_get_contents('http://169.254.169.254/latest/meta-data/placement/availability-zone');
echo $region;
?>
</center>
</h2>
</body>
</html>