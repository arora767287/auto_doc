document.getElementById('generateDoc').addEventListener('click', async () => {
    try {
        const response = await fetch('/generate_documentation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            document.getElementById('documentation-output').innerHTML = data.documentation;
        } else {
            alert('Error generating documentation: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating documentation');
    }
});
