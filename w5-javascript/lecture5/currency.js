var myHeaders = new Headers();
myHeaders.append("apikey", "wIYV2pO6EzqKDOUi5VV4HVbWQc1brHzX");

var requestOptions = {
method: 'GET',
redirect: 'follow',
headers: myHeaders
};

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').onsubmit = function() {
    fetch("https://api.apilayer.com/exchangerates_data/latest?base=USD", requestOptions)
        .then(response => response.json())
        .then(data => {
            const currency = document.querySelector('#currency').value.toUpperCase();
            const rate = data.rates[currency];
            if (rate !== undefined) {
                document.querySelector('#result').innerHTML = `1 USD = ${rate.toFixed(3)} ${currency}.`;
            } else {
                document.querySelector('#result').innerHTML = 'Invalid currency.';
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });
        return false;
    }
});