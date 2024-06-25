document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");
 
    const translateForm = document.getElementById("translateForm");
    if (translateForm) {
        translateForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            console.log("Form submitted!");
 
            const text = document.getElementById('text').value;
            const dest_lang = document.getElementById('dest_lang').value;
            console.log("Text:", text);
            console.log("Destination Language:", dest_lang);
 
            try {
                const response = await fetch('http://127.0.0.1:5000/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: text,
                        dest_lang: dest_lang
                    })
                });
 
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
 
                const data = await response.json();
                console.log("Response Data:", data);
                document.getElementById('translation').textContent = data.translated_text;
            } catch (error) {
                console.error("Error:", error);
            }
        });
    } else {
        console.error("Form not found!");
    }
 });
 
