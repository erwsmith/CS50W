let counter = 0;
function count() {
    counter++;
    document.querySelector('h1').innerHTML = counter;

    if (counter % 10 === 0) {
        alert(`Counter is now ${counter}`)
    }
}

// addEventListener(event, function)
document.addEventListener('DOMContentLoaded', function() {
    // set equal to count function (not to count function's output)
    document.querySelector('button').onclick = count;  
})