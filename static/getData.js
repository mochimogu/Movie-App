
const input = document.getElementById('searchInput')
if(input) {
    document.getElementById('searchInput').addEventListener('keydown', async (e) => {
    const options = document.getElementById('entertainment').value;
        
        if(e.key === 'Enter' && options !== "") {
            console.log(e.target.value);
            const response = await fetch("/search", {
                method : "POST",
                headers : {'Content-type' : 'application/json'},
                body : JSON.stringify({search : e.target.value, option : options})
            });
    
            if(response.ok) {
                const result = await response.json();
                console.log(result);
                window.location.href = result.url;
            } else {
                console.log(response.status);
            }
        }
    
    } )
}



