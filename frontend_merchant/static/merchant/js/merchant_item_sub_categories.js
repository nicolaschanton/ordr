function getArticleSubCategory(base_url) {
    var myHeaders = new Headers();
    var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    };

    var myTableBody = document.getElementById('articleSubCategoryTable');
    myTableBody.innerHTML = '';

    fetch(base_url + "/api/merchant-item-sub-categories/list_self/", requestOptions)
      .then(response => response.json())
      .then(result => {
            for(i in result){
                    var subCategory = result[i];

                    var subCategoryId = subCategory['id'];
                    var subCategoryDisplayOrder = subCategory['display_order'];
                    var categoryName = subCategory['category']['name'];
                    var subCategoryName = subCategory['name'];
                    var subCategoryStatus = subCategory['status'];
                    var subCleanCategoryStatus = '';

                    if (subCategoryStatus === 'ac') {
                        subCleanCategoryStatus = 'Disponible'
                    } else {
                        subCleanCategoryStatus = 'Indisponible'
                    }

                    var myTr = document.createElement('tr');
                    var myTd1 = document.createElement('td');
                    var myTd2 = document.createElement('td');
                    var myTd3 = document.createElement('td');
                    var myTd4 = document.createElement('td');
                    var myTd5 = document.createElement('td');

                    myTd1.textContent = subCategoryDisplayOrder;
                    myTd2.textContent = categoryName;
                    myTd3.textContent = subCategoryName;
                    myTd4.textContent = subCleanCategoryStatus;
                    myTd5.innerHTML = "<button onclick='populateArticleSubCategoryModal(\""+ subCategoryId + "\", \"" + base_url + "\")' data-toggle=\"modal\" data-target=\"#articleSubCategoryDetailsModal\" class=\"btn btn-success\">Voir</button>\n";

                    myTr.appendChild(myTd1);
                    myTr.appendChild(myTd2);
                    myTr.appendChild(myTd3);
                    myTr.appendChild(myTd4);
                    myTr.appendChild(myTd5);
                    myTableBody.appendChild(myTr);
            }
      }
            )
      .catch(error => console.log('error', error));

}


function updateArticleSubCategory(base_url) {
    var csrftoken = getCookie('csrftoken');
    var articleSubCategoryDetailsModal = document.getElementById('articleSubCategoryDetailsModal');
    var articleSubCategoryId = articleSubCategoryDetailsModal.dataset.subcategoryid;
    var ascdmInputStatusAvailable = document.getElementById('ascdmInputStatusAvailable');
    var ascdmInputStatusUnavailable = document.getElementById('ascdmInputStatusUnavailable');
    var articleSubCategoryState = '';

    if (ascdmInputStatusAvailable.selected === true) {
        articleSubCategoryState = 'ac';
    }
    else {
        articleSubCategoryState = 'uv';
    }

    fetch(base_url + "/api/merchant-item-sub-categories/" + articleSubCategoryId + "/partial_update_self/", {
        method: 'PATCH',
        body: JSON.stringify({
            'status': articleSubCategoryState
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
      .then(result => {

          getArticleSubCategory(base_url);

          Swal.fire(
              'Succès !',
              'Bravo 👏👏👏',
              'success'
          )
      })
        .catch(error => console.log('error', error));
}


function populateArticleSubCategoryModal(articleSubCategoryId, base_url) {
     var myHeaders = new Headers();
     var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
     };

    fetch(base_url + "/api/merchant-item-sub-categories/" + articleSubCategoryId + "/retrieve_self/", requestOptions)
      .then(response => response.json())
      .then(result => {
          var targetSubCategory = result;

          var articleSubCategoryDetailsModal = document.getElementById('articleSubCategoryDetailsModal');
          articleSubCategoryDetailsModal.dataset.subcategoryid = '';
          articleSubCategoryDetailsModal.dataset.subcategoryid  = targetSubCategory["id"];

          var ascdmInputName = document.getElementById('ascdmInputName');
          ascdmInputName.value = '';
          ascdmInputName.value = targetSubCategory["name"];

          var ascdmInputDisplayOrder = document.getElementById('ascdmInputDisplayOrder');
          ascdmInputDisplayOrder.value = '';
          ascdmInputDisplayOrder.value = targetSubCategory["display_order"];

          var ascdmInputStatusAvailable = document.getElementById('ascdmInputStatusAvailable');
          var ascdmInputStatusUnavailable = document.getElementById('ascdmInputStatusUnavailable');
          ascdmInputStatusAvailable.selected = '';
          ascdmInputStatusUnavailable.selected = '';

          if (targetSubCategory['status'] === 'ac') {
              ascdmInputStatusAvailable.selected = 'selected';
          }
          else {
              ascdmInputStatusUnavailable.selected = 'selected';
          }

      })
        .catch(error => console.log('error', error));
}



