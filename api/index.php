<?php
require_once '../conf.php';

// Create connection
$conn = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Define the correct passcode
$correct_passcode = CODE; // Change this to your actual passcode

// Extract the passcode from the URL
$passcode = filter_input(INPUT_GET, 'code');

// Extract the keycode from the URL
$keycode = filter_input(INPUT_GET, 'key');

// Check if passcode is correct
if ($passcode === $correct_passcode) {

    $sql = "SELECT * FROM `discord` WHERE `keycode` = '$keycode'";

    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) > 0) {
        // Process the results here (e.g., loop through rows using mysqli_fetch_assoc)
        while ($row = mysqli_fetch_assoc($result)) {
            $id = $row["id"];
            $date = $row["date"];
            $termination = $row["termination"];
        }
 
        if ($termination == 1) {
            $data = array("message" => true);
        } else {
            $data = array("message" => false);
        }
    } else {
        // No record found, insert a new one
        $insert_sql = "INSERT INTO `discord`(`keycode`, `termination`) VALUES ('$keycode', 0)";
        if (mysqli_query($conn, $insert_sql)) {
            echo "New record inserted successfully";
            // Define the data to be returned in JSON format
            $data = array("message" => false,);
        } else {
            echo "Error inserting record: " . mysqli_error($conn);
        }
    }

    // Set the content type header to JSON
    header('Content-Type: application/json');

    // Encode the data to JSON and echo the response
    echo json_encode($data);
} else {
    // Set the status code to unauthorized
    http_response_code(401);

    // Echo an error message
    echo json_encode(array("message" => false));
}

// Close connection (optional, recommended at the end of script)
mysqli_close($conn);