export default class APIService{
    static InsertQuery(body){
        return fetch('http://localhost:5000/data', {
            'method': 'POST',
            headers : {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .catch(error => console.log(error))
    }
}