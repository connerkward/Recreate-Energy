<?php
include("db.php");
$sql = "SELECT * FROM chamber_data";
$result = $conn->query($sql);
$i = 1;
$id = [];
$temp = [];
$ph = [];
$ADCRaw = [];
$ADCVolt = [];
$DOX = [];
$sub_date = [];

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    //   echo $row['chmb_id'];
    $temp = array_merge($temp, [$row['temp'] => $row['temp']]);

    $i++;
  }
}
    // print_r($temp);
echo json_encode($temp);
?>