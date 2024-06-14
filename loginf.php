<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the data from the POST request
    $data = $_POST['data'];

    // Append the new data to the CSV file
    file_put_contents('policedata.csv', $data . PHP_EOL, FILE_APPEND);
}
?>
