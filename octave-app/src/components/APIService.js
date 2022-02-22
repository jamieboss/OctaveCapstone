export default class APIService{
    static InsertQuery(body){
        return fetch('http://localhost:8080/data', {
            'method': 'POST',
            headers : {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .catch(error => console.log(error))
    }

    static ReceieveQuery(){
        return fetch('http://localhost:3000/res')
    }
}