<?php
function getReverseDNS($ip) {
    // Validate the IP address
    if (!filter_var($ip, FILTER_VALIDATE_IP)) {
        return "Invalid IP";
    }

    // Perform the reverse DNS lookup
    $hostname = gethostbyaddr($ip);

    // Check if the lookup was successful
    if ($hostname === $ip) {
        return "No rDNS";
    }

    return $hostname;
}
function getServerRow($server) {
    $id =  $server['id'];
    $ip = $server['ip'];
    $image = $server['image'];
    $region = $server['region'];
    $status = $server['status'];
    $label = $server['label'];

    // // Split the domain string into domain and IP
    // list($domain, $ip) = explode(': ', $domainString, 2);

    // // Escape the values to prevent XSS attacks
    // $domain = htmlspecialchars(trim($domain));
    // $ip = htmlspecialchars(trim($ip));

    // // Return formatted HTML
    return "<tr>
            <td><input type=\"checkbox\"></td>
            <td>$ip</td>
            <td>$image</td>
            <td>$region</td>
            <td><a href=\"rdns.php?id=$id\">".getReverseDNS($ip)."</a></td>
            <td>$status</td>
            <td>$label</td>
            <td><a style=\"color:red;\" href=\"delete.php?id=$id\">Delete</a></td>
        </tr>";
}

$apiUrl = 'http://134.209.160.169:5000/linodeApi?context=getAll' ;
$response = file_get_contents($apiUrl);
$servers = [];
$regions = [];
if ($response !== false) {
    $data = json_decode($response, true);

    // Check if decoding was successful and data is in the expected format
    if (json_last_error() === JSON_ERROR_NONE && isset($data['data'])) {
        $servers = $data['data'];
        $regions = $data['regions'];
        
    } else {
        // Handle JSON parsing error or invalid data
        $servers = [];
    }
} else {
    // Handle the error if the API request fails
    $servers = [];
}
// print_r($regions);
// echo 'hey';
// echo "<script>alert('hey')</script>";
// return
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linode API</title>
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="images/icons/css/font-awesome.css">
    <link href="http://fonts.googleapis.com/css?family=Open+Sans:400,600" rel="stylesheet">
    <script src="scripts/jquery-1.9.1.min.js"></script>
    <script src="bootstrap/js/bootstrap.min.js"></script>
    <style>
        body {
            font-family: 'Open Sans', sans-serif;
            background-color: #f4f6f8; /* Softer light background */
            color: #2c3e50; /* Darker text for better readability */
            line-height: 1.6; 
            margin: 0;
            padding: 20px;
        }
        
        .container {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Slightly smaller shadow */
            padding: 40px;
            margin: 20px auto;
            max-width: 80%;
        }
        
        h2 {
            color: #34495e; /* Darker blue-gray for headings */
            margin-bottom: 30px;
            font-weight: 600;
            text-align: center;
        }
        
        .form-inline {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        
        .form-inline input,
        .form-inline select {
            flex: 1;
            margin-right: 10px;
            border: 1px solid #bdc3c7; /* Softer gray borders */
            border-radius: 4px;
            padding: 10px;
            transition: border-color 0.3s ease;
        }
        
        .form-inline input:focus,
        .form-inline select:focus {
            border-color: #3498db; /* Bright blue focus for input fields */
            outline: none;
        }
        
        .btn {
            border-radius: 4px;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        
        .btn:hover {
            transform: scale(1.05);
        }
        
        .btn-success {
            background-color: #27ae60; /* Softer green */
            border: none;
        }
        
        .btn-success:hover {
            background-color: #229954; /* Slightly darker hover effect */
        }
        
        .btn-primary {
            background-color: #2980b9; /* Strong blue for primary buttons */
            border: none;
        }
        
        .btn-primary:hover {
            background-color: #2471a3; /* Darker blue on hover */
        }
        
        .btn-info {
            background-color: #16a085; /* Teal color for info buttons */
            border: none;
        }
        
        .btn-info:hover {
            background-color: #138d75;
        }
        
        .table {
            margin-top: 20px;
            border-collapse: collapse;
            width: 100%;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .table th,
        .table td {
            vertical-align: middle;
            text-align: center;
            padding: 12px;
            border: 1px solid #ecf0f1; /* Light borders for better separation */
        }
        
        .table th {
            background-color: #f2f3f5; /* Soft gray background for headers */
            color: #34495e; /* Darker text for contrast */
            font-weight: 600;
        }
        
        .table-striped tbody tr:nth-of-type(odd) {
            background-color: #f9f9f9; /* Light row background for stripes */
        }
        
        .table-hover tbody tr:hover {
            background-color: #eaf2f8; /* Soft blue for hover effect */
        }
        
        .modal-header {
            border-bottom: 2px solid #2980b9; /* Consistent blue for modal header */
        }
        
        .modal-body {
            font-size: 16px;
        }
        
        .text-center {
            margin-top: 20px;
        }
        
        .textarea {
            border-radius: 4px;
            border: 1px solid #bdc3c7;
            padding: 10px;
            width: 100%;
            resize: none;
        }
        
        .textarea:focus {
            border-color: #2980b9;
            outline: none;
        }
        
        @media (max-width: 600px) {
            .form-inline {
                flex-direction: column;
            }
            .form-inline input,
            .form-inline select {
                margin-right: 0;
                margin-bottom: 10px;
            }
        }
        
        
        
    </style>
</head>
<body>
    <div class="container mt-4">
        <h2 class="text-center">Linode API, <?php echo count($servers)?> ips</h2>
        <!-- <form class="form-inline mb-4">
            <input required name="api" class="form-control" placeholder="API Key" type="text">
            <button name="action" value="api" class="btn btn-success" type="submit"><i class="icon-play icon-white"></i> Make Change</button>
        </form> -->

        <form class="form-group" action="create.php" method="POST">
            <label for="region" class="control-label"><b>Create Linode</b></label>
            <select class="form-control" id="region" name="region">
                <option style="color:green;" value="random">Random</option>
                <?php foreach ($regions as $region): ?>
                        <?php echo '<option value="'.$region['id'].'">'.$region['label'].'</option>'?>
                    <?php endforeach; ?>
            </select>
            <input required name="Label" class="form-control" placeholder="Label" style="width: 130px;" type="text">
            <input type="number" pattern="[0-9]*" required name="number" class="form-control" placeholder="number" min="1" max="50"  style="width: 60px;" value="1">
            <button class="btn btn-primary" name="action" value="create" type="submit"><i class="icon-bookmark icon-pencil icon-white"></i> Create</button>
            <button class="btn btn-info" type="button" onclick="copy()"><i class="icon-copy icon-white"></i> Copy IPs</button>
            
        </form>

        <div class="table-responsive mt-4">
            <table id="show" class="table table-bordered table-striped">
                <thead>
                    <tr>
                        <th><input type="checkbox"></th>
                        <th>IP</th>
                        <th>OS</th>
                        <th>Region</th>
                        <th>RDNS</th>
                        <th>Status</th>
                        <th>Label</th>
                        <th>Destroy</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($servers as $server): ?>
                        <?php echo getServerRow($server);?>
                    <?php endforeach; ?>

                    <!-- <tr>
                        <td><input type="checkbox"></td>
                        <td>172.105.7.212</td>
                        <td>ok</td>
                        <td>Toronto, CA</td>
                        <td><a href="rdns.php?ip=172.105.7.212">lffdzax.iceage.com.my</a></td>
                        <td>running</td>
                        <td>ToRo-YS_0</td>
                        <td><a style="color:red;" href="?action=delete&id=61220170">Delete</a></td>
                    </tr> -->
                    <!-- add tr rows with js -->
                </tbody>
                <tfoot>
                    <tr>
                        <th><button type="button" class="btn btn-danger">X</button></th>
                        <th>IP</th>
                        <th></th>
                        <th>Region</th>
                        <th>RDNS</th>
                        <th>Status</th>
                        <th>Label</th>
                        <th>Destroy</th>
                    </tr>
                </tfoot>
            </table>
        </div>

        <div class="text-center mt-4">
            <textarea class="form-control" rows="5" placeholder="Additional notes..."></textarea>
            <br>
            <button type="button" class="btn btn-primary">Select</button>
            <button type="button" class="btn btn-secondary">Check Score</button>
        </div>
    </div>


    
</body>
<script></script>
</html>
