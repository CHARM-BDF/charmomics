async function sendFormData(method, url, data) {
  
    const formData = new FormData();
    const fieldEntries = Object.entries(data);
    
    for (const [field, fieldContent] of fieldEntries) {
      formData.append(field, fieldContent);
    }
    
    const response = await fetch(url, {
      method: method,
      mode: 'cors',
      cache: 'no-cache',
      body: formData,
    });
    
    if ( response.ok != true ) {
      throw new Error('Status Code: ' + response.status + ' ' + response.statusText);
    }
    
    return await response.json();
}

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
    },

    async postForm(url, data) {
      return await sendFormData('POST', url, data);
    }
}
