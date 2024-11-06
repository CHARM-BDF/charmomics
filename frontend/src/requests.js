export default {
    async get(url) {
        
        console.log(url)
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            },
            mode: 'cors'
        });

        console.log(response)
        //console.log(await response)

        if ( response.ok != true )
            throw new Error('Status Code: ' + response.status +' '+ response.statusText);

        return await response.json();
    }
}
