<?php
include("db.php");
$sql = "SELECT * FROM chamber_data";
$result = $conn->query($sql);
$id = [];
$temp = [];
$ph = [];
$ADCRaw = [];
$ADCVolt = [];
$DOX = [];
$export = [];
$i= 0;
if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    // print_r($arras);
    $export = array_merge($export,      ["chmb_id".$i => $row["chmb_id"],
    'temp'.$i => $row['temp'],
    'ph'.$i => $row['ph'], 
    'ADCRaw'.$i => $row['ADCRaw'],
    'ADCVolt'.$i => $row['ADCVolt'], 
    'DOX'.$i => $row['DOX']]);
    // $export = array_merge($export, $arras);
    $i++;
  }
}
    // print_r($export);

    // print_r($export);
echo json_encode($export);
?>