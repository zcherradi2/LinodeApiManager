<?php
// Check if the 'id' parameter is set in the URL
if (isset($_GET['id']) && !empty($_GET['id'])) {
    // Retrieve the 'id' from the request
    $id = $_GET['id'];
    echo $id;
    // The base API URL
    $apiUrl = "http://134.209.160.169:5000/linodeApi?context=delete&id=$id";

    // // Create the URL with the necessary query parameters to delete the item
    // $apiUrlWithParams = $apiUrl . '?' . http_build_query([
    //     'context' => 'delete',
    //     'id' => $id
    // ]);

    // Send a GET request to the API to delete the item
    $response = file_get_contents($apiUrl);

    // Check the response from the API
    if ($response == FALSE) {
        echo "Failed to delete item with ID: $id";
        header('Location: linode.php?message=failed_to_delete');
    } else {
        echo "Item with ID: $id has been successfully deleted.";
        header('Location: linode.php?message=successfuly_deleted');
    }
} else {
    echo "No ID provided. Please specify an ID to delete.";
    header('Location: linode.php?message=no_ip_provided');
}
