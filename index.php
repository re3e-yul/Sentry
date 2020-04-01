<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<meta http-equiv='refresh' content='1'>
<body>
<?php

$hostname = "localhost";
$username = "pi";
$password = "a-51d41e";
$db = "Sentry";

$dbconnect=mysqli_connect($hostname,$username,$password,$db);

if ($dbconnect->connect_error) {
  die("Database connection failed: " . $dbconnect->connect_error);
}

?>
<table border="1" align="center">
<tr>
	<td>date</td>
	<td>ChargeLevel</td>
	<td>ChargeStatus</td>
	<td>Vbat</td>
	<td>IBat</td>
	<td>Vio</td>
	<td>Iio</td>
</tr>

<?php

$query = mysqli_query($dbconnect, "SELECT * FROM BattDATA order by date desc limit 5")
   or die (mysqli_error($dbconnect));

while ($row = mysqli_fetch_array($query)) {
  echo
   "<tr>
    <td>{$row['date']}</td>
    <td>{$row['ChargeLevel']}</td>
    <td>{$row['ChargeStatus']}</td>
    <td>{$row['Vbat']}</td>
    <td>{$row['IBat']}</td>
    <td>{$row['Vio']}</td>
    <td>{$row['Iio']}</td>
   </tr>\n";

}

?>
</table>
</body>
</html>
