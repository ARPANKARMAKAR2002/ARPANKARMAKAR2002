document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('contactForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way
        
        const formData = new FormData(this);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch('http://localhost:3000/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.text())
        .then(result => {
            document.getElementById('responseMessage').textContent = result;
            document.getElementById('contactForm').reset(); // Reset form fields
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('responseMessage').textContent = 'There was a problem sending your message. Please try again.';
        });
    });
});
