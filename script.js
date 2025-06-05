function analyzeNews() {
    const newsText = document.getElementById('news-text').value;

    // Check if the input text is empty
    if (newsText.trim() === "") {
        alert("Please enter some text to analyze.");
        return;
    }

    // Send the news text to the Flask API
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ newsText: newsText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.verdict) {
            document.getElementById('verdict').textContent = data.verdict;
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during the analysis.');
    });
}
