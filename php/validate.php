<?php

$domain =parse_url($_REQUEST["domain"],PHP_URL_HOST);

include "config.php";
$sql = "SELECT * FROM `blacklist` WHERE `url` LIKE '%$domain%'";
// echo $sql;
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {


    }
    $myObj=new \stdClass();
    $myObj->success =false;
    $myObj->error = 'The Domain is blacklisted';
    $myJSON = json_encode($myObj);
    echo $myJSON;

    

} else {

    $myObj=new \stdClass();
    $myObj->success =true;
    $myObj->error = '';
    $myJSON = json_encode($myObj);
    echo $myJSON;
  
}
// $conn->close();



?>