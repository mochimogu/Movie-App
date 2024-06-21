
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


window.addEventListener('DOMContentLoaded', () => {

    const button = document.getElementById('button');
    if(button) {
        button.addEventListener('click', async () => {
            
            const imageURL = document.getElementById('imageSrc').src;
            const title = document.getElementById('title').innerText;
            const releaseDate = document.getElementById('infoTable').children[0].children[1].children[1].innerHTML;
            const buttonID = document.getElementById('button').children[0].id
            const type = document.getElementById('imageSrc').alt;

            if(type == 'movie_poster') {
                sending = {
                    'title' : title,
                    'id' : buttonID,
                    'imageURL' : imageURL,
                    'release' : releaseDate,
                    'type' : 'movie'
                }
            } else {
                sending = {
                    'title' : title,
                    'id' : buttonID,
                    'imageURL' : imageURL,
                    'release' : releaseDate,
                    'type' : 'show'
                }
            }

            console.log(sending)

            const response = await fetch('/api/saveCinema', {
                method : "POST",
                headers : {'Content-type' : "application/json"},
                body : JSON.stringify(sending)
            })

            if(response.ok) {
                const result = await response.json();
                console.log(result);
            } else {
                console.log("STATUS CODE : " + response.status)
            }
        })
    }
})


async function deleteFromCollection(e) {

    console.log('hello world')
    console.log(e.id)

    sending = {
        'cinemaID' : e.id
    }

    const response = await fetch('/api/deleteCinema', {
        method : "UPDATE",
        headers : {'Content-type' : "application/json"},
        body : JSON.stringify(sending)
    })

    if(response.ok) {
        console.log('okay');
    } else {
        console.log('bad');
    }


}


