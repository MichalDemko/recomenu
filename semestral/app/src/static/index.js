function deleteFood(foodId){
    fetch('/delete-food', {
        method: 'POST',
        body: JSON.stringify({ foodId: foodId})
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteCategory(categoryId){
    fetch('/delete-category', {
        method: 'POST',
        body: JSON.stringify({ categoryId: categoryId})
    }).then((_res) => {
        window.location.href = "/settings";
    });
}

function updateCategory(categoryId, updateparameter){
    fetch('/update-category', {
        method: 'POST',
        body: JSON.stringify({ categoryId: categoryId, value: updateparameter.value})
    }).then((_res) => {
        window.location.href = "/settings";
    });
}

function addToMenu(foodId){
    date = document.querySelector('input[name="weekday"]:checked').value;
    console.log(date);
    fetch('/add-to-menu', {
        method: 'POST',
        body: JSON.stringify({ foodId: foodId, date: date})
    }).then((_res) => {
        window.location.href = "/menu";
    });
}