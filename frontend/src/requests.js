export default {
    async get(url) {        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            },
            mode: 'cors'
        });

        if ( response.ok != true )
            throw new Error('Status Code: ' + response.status +' '+ response.statusText);

        return await response.json();
    }
}
