
document.getElementById('translateForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const text = document.getElementById('text').value;
    const dest_lang = document.getElementById('dest_lang').value;

    const response = await fetch('http://127.0.0.1:5000/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: text,
            dest_lang: dest_lang
        })
    })

    const data = await response.json();
    document.getElementById('translation').textContent = data.translated_text})
