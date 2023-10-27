
        document.getElementById('convertBtn').addEventListener('click', function() {
            let yamlData = document.getElementById('yamlInput').value;
            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'yaml_input=' + encodeURIComponent(yamlData)
            })
            .then(response => response.json())
            .then(data => {
                let resultDiv = document.getElementById('result');
                if(data.status === 'success') {
                    resultDiv.innerHTML = `<div class="alert alert-success"><pre>${data.data}</pre></div>`;
                } else if (data.status === 'odd') {
                    resultDiv.innerHTML = `<div class="alert alert-warning"><pre>${data.data}</pre></div>`;
                } else {
                    resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${data.message}</div>`;
                }
            });
        });
    