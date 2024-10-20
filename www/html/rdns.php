<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update rDNS</title>
    <style>
        /* Basic CSS to center the form and improve styling */
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }

        .form-container {
            background-color: #fff;
            padding: 20px 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            width: 350px;
            text-align: center;
        }

        .form-container h2 {
            margin-bottom: 20px;
            color: #333;
        }

        .form-control {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        .btn {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }

        .btn:disabled {
            background-color: #aaa;
            cursor: not-allowed;
        }

        .loading-indicator {
            margin-top: 15px;
            display: none;
        }

        .loading-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            margin: 0 2px;
            background-color: #007bff;
            border-radius: 50%;
            animation: bounce 0.6s infinite alternate;
        }

        @keyframes bounce {
            to {
                opacity: 0.3;
                transform: translateY(-8px);
            }
        }

        .loading-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .loading-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Update rDNS</h2>
        <form id="rdnsForm">
            <input type="text" name="rdns" id="rdns" class="form-control" required placeholder="Enter rDNS domain">
            <button type="submit" class="btn" id="submitBtn">Update rDNS</button>
            <button type="button" class="btn" id="untilDone" onclick="tryUntilDone()">try until Done</button>
        </form>
        <div class="loading-indicator" id="loadingIndicator" >
            <span></span><span></span><span></span>
        </div>
        <div id="responseMessage"></div>
    </div>

    <script>
        function changeRdns(id,rdns){
            const loadingIndicator = document.getElementById('loadingIndicator');
            const responseMessage = document.getElementById('responseMessage');
            const submitBtn = document.getElementById('submitBtn');

                        // Clear previous messages and show loading indicator
            responseMessage.innerHTML = '';
            loadingIndicator.style.display = 'flex';
            submitBtn.disabled = true;
            fetch(`http://134.209.160.169:5000/linodeApi?context=rdns&id=${id}&rdns=${rdns}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    loadingIndicator.style.display = 'none'; // Hide the loading indicator
                    submitBtn.disabled = false;
                    console.log(data)
                    if (data.success) {
                        responseMessage.innerHTML = '<div style="color: green;">rDNS updated successfully.</div>';
                        setTimeout(()=>{
                            window.location = '/linode.php';
                        },2000)
                    } else {
                        responseMessage.innerHTML = '<div style="color: red;">' + (data.message || 'Unknown error')+'</div>';
                    }
                })
                .catch(error => {
                    loadingIndicator.style.display = 'none'; // Hide the loading indicator
                    submitBtn.disabled = false;
                    responseMessage.innerHTML = '<div style="color: red;">Error: ' + error.message + '</div>';
                });
        }
        function tryUntilDone(){
            const rdns = document.getElementById('rdns').value;
            const btn = document.getElementById('untilDone');
            const loadingIndicator = document.getElementById('loadingIndicator');
            const responseMessage = document.getElementById('responseMessage');
            btn.disabled = true
            const id = new URLSearchParams(window.location.search).get('id');
            let i = 0;
            changeRdns(id,rdns);
            let myid =setInterval(()=>{
                i += 3
                if(i>120 || responseMessage.innerText.includes('rDNS updated successfully.')){
                    clearInterval(id);
                    btn.disabled = false
                }else{
                    changeRdns(id,rdns);
                }
            },5000)
        }
        document.getElementById('rdnsForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            const rdns = document.getElementById('rdns').value;
            const id = new URLSearchParams(window.location.search).get('id'); // Get the ID from the URL
            
            changeRdns(id,rdns)
        });
    </script>
</body>
</html>
