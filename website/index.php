
<html>
<title> JangoMart Customer Loyalty Portal </title>
<body>
<h1 style="color: orange;">
<center>
JangoMart Customer Loyalty Portal V1
</center>
</h1>
<h2>
<center>
    Server IP:&nbsp;
<?php
$eip = file_get_contents('http://169.254.169.254/latest/meta-data/public-ipv4');
echo $eip;
?>
</center>
</h2>
</body>
</html>