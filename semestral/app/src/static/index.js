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
        var url = new URL("http://localhost:5000/menu");
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
    
        if (urlParams.has('categories')) {
            url.searchParams.set('categories',urlParams.get('categories'));
        }

        if (urlParams.has('date')) {
            url.searchParams.set('date',urlParams.get('date'));
        }
        
        window.location.href = url;
    });
}

function deleteMenuFood( menu_id, food_id ){
    fetch('/delete-from-menu', {
        method: 'POST',
        body: JSON.stringify({ menu_id: menu_id, food_id: food_id})
    }).then((_res) => {
        var url = new URL("http://localhost:5000/menu");
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
    
        if (urlParams.has('categories')) {
            url.searchParams.set('categories',urlParams.get('categories'));
        }

        if (urlParams.has('date')) {
            url.searchParams.set('date',urlParams.get('date'));
        }

        window.location.href = url;
    });
}

function changeToPage(date){
    var url = new URL("http://localhost:5000/menu");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    
    if (urlParams.has('categories')) {
        url.searchParams.set('categories',urlParams.get('categories'));
    }
    url.searchParams.set('date',date);
    window.location.href = url;


}

var mycheckboxes = document.querySelectorAll('input[name="categoryfilter"]');
console.log("categories");
console.log(mycheckboxes);

mycheckboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        console.log("event");
        selectCategories();
      });
});

function selectCategories(){
    var mycheckedboxes = document.querySelectorAll('input[name="categoryfilter"]:checked').values();
    var values = [];
    for (let val of mycheckedboxes) {
        console.log(val.value);
        values.push(val.value);
    }
    //mycheckedboxes.forEach(function(value) {console.log(value);});
    console.log(mycheckedboxes);
    var url = new URL("http://localhost:5000/menu");
    url.searchParams.set('categories',values);
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    
    if (urlParams.has('date')) {
        url.searchParams.set('date',urlParams.get('date'));
    }
    console.log(url);
    window.location.href = url;
}