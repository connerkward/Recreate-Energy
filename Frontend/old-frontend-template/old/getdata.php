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
    $sub_date = array_merge($sub_date, [$row['sub_date'] => $row['sub_date']]);
    $i++;
  }
}
    // print_r($temp);
echo json_encode($sub_date);
?>