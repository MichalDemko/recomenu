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