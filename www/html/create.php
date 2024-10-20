<?php
// Check if the form has been submitted with a POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Retrieve and sanitize form inputs
    $region = isset($_POST['region']) ? htmlspecialchars(trim($_POST['region'])) : null;
    $label = isset($_POST['Label']) ? htmlspecialchars(trim($_POST['Label'])) : null;
    $number = isset($_POST['number']) ? intval($_POST['number']) : null;

    // Validate inputs
    $errors = [];

    // Check if region is not empty
    if (empty($region)) {
        $errors[] = 'Region is required.';
    }

    // Check if label is not empty and meets your criteria
    if (empty($label) || strlen($label) < 3 || strlen($label) > 50) {
        $errors[] = 'Label is required and must be between 3 and 50 characters.';
    }

    // Validate the number field to ensure it is between 1 and 50
    if ($number < 1 || $number > 50) {
        $errors[] = 'Number must be between 1 and 50.';
    }

    // Check if there are any errors
    if (count($errors) > 0) {
        // Display errors to the user
        echo '<div class="alert alert-danger">';
        foreach ($errors as $error) {
            echo '<p>' . $error . '</p>';
        }
        echo '</div>';
    } else {
        // If no errors, process the data
        // Here, you would typically send a request to the Linode API or save the data to your database

        // Example: Sending data to the Linode API
        $apiUrl = "http://134.209.160.169:5000/linodeApi?context=create&label=$label&region=$region&number=$number";

        $response = file_get_contents($apiUrl);

        // Check the response from the API
        if ($response === FALSE) {
            echo "Failed to create item";
            // header('Location: linode.php?message=failed_to_create');
        } else {
            $data = json_decode($response, true);
            echo "has been successfully created.";
            header('Location: linode.php?message=successfuly_created,_failed_at_'.$data['fails']);
        }


        // // Check for cURL errors
        // if (curl_errno($ch)) {
        //     echo 'Error communicating with the API: ' . curl_error($ch);
        // } else {
        //     // Process the API response
        //     $responseData = json_decode($response, true);
        //     if (isset($responseData['success']) && $responseData['success']) {
        //         echo '<div class="alert alert-success">Linode created successfully.</div>';
        //     } else {
        //         echo '<div class="alert alert-danger">Error creating Linode: ' . htmlspecialchars($responseData['message'] ?? 'Unknown error') . '</div>';
        //     }
        // }

        // Close cURL session
        curl_close($ch);
    }
} else {
    echo '<div class="alert alert-danger">Invalid request method.</div>';
}
?>
