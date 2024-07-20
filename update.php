<?php

    require_once './conf.php';

    // Create connection
    $conn = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Get the ID from the form
    $code = $_POST["id"];

    // Update SQL statement
    $sql = "UPDATE `discord` SET termination = 1 WHERE keycode = '$code'";

    // Update the database
    if ($conn->query($sql) === TRUE) {
        echo "Termination updated successfully";
    } else {
        echo "Error updating termination: " . $conn->error;
    }

    $conn->close();

    header("location: .");
    exit;