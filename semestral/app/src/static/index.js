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
    fetch('/add-to-menu', {
        method: 'POST',
        body: JSON.stringify({ foodId: foodId, date: date})
    }).then((_res) => {
        window.location.href = "/menu";
    });
}

function deleteMenuFood( menu_id, food_id ){
    fetch('/delete-from-menu', {
        method: 'POST',
        body: JSON.stringify({ menu_id: menu_id, food_id: food_id})
    }).then((_res) => {
        window.location.href = "/menu";
    });
}

function changeToPage(date){
    console.log(date);
    var url = new URL("http://localhost:5000/menu");
    url.searchParams.set('date',date);
    window.location.href = url;
    
}