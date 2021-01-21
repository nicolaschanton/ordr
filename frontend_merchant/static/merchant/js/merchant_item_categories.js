function getArticleCategory(base_url) {
    var myHeaders = new Headers();
    var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    };

    var myTableBody = document.getElementById('articleCategoryTable');
    myTableBody.innerHTML = '';

    fetch(base_url + "/api/merchant-item-categories/list_self/", requestOptions)
      .then(response => response.json())
      .then(result => {
            for(i in result){
                var category = result[i];

                    var categoryId = category['id'];
                    var categoryDisplayOrder = category['display_order'];
                    var categoryName = category['name'];
                    var categoryStatus = category['status'];
                    var cleanCategoryStatus = '';

                    if (categoryStatus === 'ac') {
                        cleanCategoryStatus = 'Disponible'
                    } else {
                        cleanCategoryStatus = 'Indisponible'
                    }

                    var myTr = document.createElement('tr');
                    var myTd1 = document.createElement('td');
                    var myTd2 = document.createElement('td');
                    var myTd3 = document.createElement('td');
                    var myTd4 = document.createElement('td');

                    myTd1.textContent = categoryDisplayOrder;
                    myTd2.textContent = categoryName;
                    myTd3.textContent = cleanCategoryStatus;
                    myTd4.innerHTML = "<button onclick='populateArticleCategoryModal(\""+ categoryId + "\", \"" + base_url + "\")' data-toggle=\"modal\" data-target=\"#articleCategoryDetailsModal\" class=\"btn btn-success\">Voir</button>\n";

                    myTr.appendChild(myTd1);
                    myTr.appendChild(myTd2);
                    myTr.appendChild(myTd3);
                    myTr.appendChild(myTd4);
                    myTableBody.appendChild(myTr);
            }
      }
            )
      .catch(error => console.log('error', error));

}


function updateArticleCategory(base_url) {
    var csrftoken = getCookie('csrftoken');
    var articleCategoryDetailsModal = document.getElementById('articleCategoryDetailsModal');
    var articleCategoryId = articleCategoryDetailsModal.dataset.categoryid;
    var acdmInputStatusAvailable = document.getElementById('acdmInputStatusAvailable');
    var acdmInputStatusUnavailable = document.getElementById('acdmInputStatusUnavailable');
    var articleCategoryState = '';

    console.log(acdmInputStatusAvailable.selected);

    if (acdmInputStatusAvailable.selected === true) {
        articleCategoryState = 'ac';
    }
    else {
        articleCategoryState = 'uv';
    }


    fetch(base_url + "/api/merchant-item-categories/" + articleCategoryId + "/partial_update_self/", {
        method: 'PATCH',
        body: JSON.stringify({
            'status': articleCategoryState
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
      .then(result => {

          getArticleCategory(base_url);

          Swal.fire(
              'Succès !',
              'Bravo 👏👏👏',
              'success'
          )
      })
        .catch(error => console.log('error', error));
}


function populateArticleCategoryModal(articleCategoryId, base_url) {
    var itemClUrl = 'https://res.cloudinary.com/hzhwp1933/image/upload/w_100,h_100,c_fit/';

     var myHeaders = new Headers();
     var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
     };

    fetch(base_url + "/api/merchant-item-categories/" + articleCategoryId + "/retrieve_self/", requestOptions)
      .then(response => response.json())
      .then(result => {
          var targetCategory = result;

          var articleCategoryDetailsModal = document.getElementById('articleCategoryDetailsModal');
          articleCategoryDetailsModal.dataset.categoryid = '';
          articleCategoryDetailsModal.dataset.categoryid  = targetCategory["id"];

          var acdmInputName = document.getElementById('acdmInputName');
          acdmInputName.value = '';
          acdmInputName.value = targetCategory["name"];

          var acdmInputDisplayOrder = document.getElementById('acdmInputDisplayOrder');
          acdmInputDisplayOrder.value = '';
          acdmInputDisplayOrder.value = targetCategory["display_order"];

          var acdmInputStatusAvailable = document.getElementById('acdmInputStatusAvailable');
          var acdmInputStatusUnavailable = document.getElementById('acdmInputStatusUnavailable');
          acdmInputStatusAvailable.selected = '';
          acdmInputStatusUnavailable.selected = '';

          if (targetCategory['status'] === 'ac') {
              acdmInputStatusAvailable.selected = 'selected';
          }
          else {
              acdmInputStatusUnavailable.selected = 'selected';
          }

      })
        .catch(error => console.log('error', error));
}



