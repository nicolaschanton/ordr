function getCategoryHeader(base_url, cloudinary_cloud_name) {
    var myHeaders = new Headers();
    var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    };

    var myCategoryHeader = document.getElementById('categoryHeader');
    myCategoryHeader.innerHTML = '';

    var categoryHeader = document.getElementById('categoryHeader');


    fetch(base_url + "/api/merchant-item-categories/list_self/", requestOptions)
      .then(response => response.json())
      .then(result => {
            for(i in result){
                var category = result[i];
                var categoryId = category['id'];

                if ('0' === i) {
                    if (categoryHeader.dataset.focusedcategoryid) {
                        getArticles(base_url, categoryHeader.dataset.focusedcategoryid, cloudinary_cloud_name);
                    } else {
                        categoryHeader.dataset.focusedcategoryid = categoryId;
                    }
                }

                    var categoryName = category['name'];
                    var myCol = document.createElement('div');
                    myCol.className = 'col-lg-3 mb-2';

                    var myColInside = document.createElement('div');
                    myColInside.id = categoryId;
                    myColInside.className = "category-header card bg-primary text-white shadow";

                    var myButton = document.createElement('button');
                    myButton.className = "text-white";

                    myColInside.innerHTML = "<a onclick='getArticles(\""+ base_url + "\", \"" + categoryId + "\", \"" + cloudinary_cloud_name + "\")' class=\"text-white\">\n" +
                        "                       <div id='title' class=\"card-body\">\n" + categoryName + "</div>\n" +
                        "                    </a>\n";
                    myCol.appendChild(myColInside);
                    myCategoryHeader.appendChild(myCol);
            }

            getArticles(base_url, categoryHeader.dataset.focusedcategoryid, cloudinary_cloud_name)

      }
            )
      .catch(error => console.log('error', error));

}


function getArticles(base_url, categoryId, cloudinary_cloud_name) {
    var myTableBody = document.getElementById('articleTable');
    myTableBody.innerHTML = '';

    var myFocusedButton = document.getElementById(categoryId);
    var myButtons = document.getElementsByClassName('category-header');

    for(i in myButtons) {
        var myButton = myButtons[i];
        myButton.className = 'category-header card bg-primary text-white shadow'
    }

    if (myFocusedButton) {
        myFocusedButton.className = 'category-header card bg-success text-white shadow';
    }

    var tableCategoryId = document.getElementById('articleTable');
    tableCategoryId.dataset.categoryid = categoryId;

    var categoryHeader = document.getElementById('categoryHeader');
    categoryHeader.dataset.focusedcategoryid = categoryId;

    fetch(base_url + "/api/merchant-items/list_self/?merchant_item_category_id=" + categoryId, {
        method: 'GET',
        headers: {'Content-type': 'application/json; charset=UTF-8',}
    })
    .then(response => response.json())
      .then(result => {
            for(i in result){
                var article = result[i];

                    var articleId = article['id'];
                    var articleDisplayOrder = article['display_order'];
                    // var articleSubCategory = article['sub_category']['name'];
                    var articleName = article['name'];
                    var articleDescription = article['description'].substring(0, 25) + "...";
                    var articlePriceVatIncluded = String(Intl.NumberFormat('fr-FR', {
                        style: 'currency',
                        currency: 'EUR'
                    }).format(article['price_vat_included']));
                    var cleanArticleStatus = '';

                    if (article['status'] === 'ac') {
                        cleanArticleStatus = 'Disponible'
                    } else {
                        cleanArticleStatus = 'Indisponible'
                    }

                    var myTr = document.createElement('tr');
                    var myTd1 = document.createElement('td');
                    var myTd3 = document.createElement('td');
                    var myTd4 = document.createElement('td');
                    var myTd5 = document.createElement('td');
                    var myTd6 = document.createElement('td');
                    var myTd7 = document.createElement('td');

                    myTd1.textContent = articleDisplayOrder;
                    myTd3.textContent = articleName;
                    myTd4.textContent = articleDescription;
                    myTd5.textContent = articlePriceVatIncluded;
                    myTd6.textContent = cleanArticleStatus;
                    myTd7.innerHTML = "<button onclick='populateArticleModal(\""+ articleId + "\", \"" + base_url + "\", \"" + cloudinary_cloud_name + "\")' data-toggle=\"modal\" data-target=\"#articleDetailsModal\" class=\"btn btn-success\">Voir</button>\n";

                    myTr.appendChild(myTd1);
                    myTr.appendChild(myTd3);
                    myTr.appendChild(myTd4);
                    myTr.appendChild(myTd5);
                    myTr.appendChild(myTd6);
                    myTr.appendChild(myTd7);
                    myTableBody.appendChild(myTr);
            }
      }
            )
      .catch(error => console.log('error', error));
}


function updateArticle(base_url, cloudinary_cloud_name) {
    var categoryHeader = document.getElementById('categoryHeader');
    var categoryId = categoryHeader.dataset.focusedcategoryid;
    var csrftoken = getCookie('csrftoken');
    var articleDetailsModal = document.getElementById('articleDetailsModal');
    var articleId = articleDetailsModal.dataset.articleid;
    var admInputStatusAvailable = document.getElementById('admInputStatusAvailable');
    var articleState = '';

    // Item Update
    if (admInputStatusAvailable.selected === true) {
        articleState = 'ac';
    }
    else {
        articleState = 'uv';
    }

    // API call for Item Update
    fetch(base_url + "/api/merchant-items/" + articleId + "/partial_update_self/", {
        method: 'PATCH',
        body: JSON.stringify({
            'status': articleState
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
      .then(result => {
          getArticles(base_url, categoryId, cloudinary_cloud_name);
      })
        .catch(error => console.log('error', error));


    // Customization Update
    var myCustomizations = document.getElementsByClassName('my-options-div');

    for (i in myCustomizations) {
        var customizationId = myCustomizations[i].id;

        var availableInput = document.getElementById("option-available-" + customizationId);

        if (availableInput) {
            var customizationStatus = '';
            if (availableInput.selected === true) {
                customizationStatus = 'ac'
            } else {
                customizationStatus = 'uv'
            }
        }

        // API call for Item Customization Update

        if (customizationId) {
        fetch(base_url + "/api/merchant-item-customizations/" + customizationId + "/partial_update_self/", {
        method: 'PATCH',
        body: JSON.stringify({
            'status': customizationStatus
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
        })
        .then(response => response.json())
          .then(result => {})
            .catch(error => console.log('error', error));
        }
    }

    // Customization Option Update
        var myCustomizationOptions = document.getElementsByClassName('item-customization-option-item');
        for (j in myCustomizationOptions) {

            var customizationOptionId = myCustomizationOptions[j].id;
            var availableOptionInput = document.getElementById("option-customization-available-" + customizationOptionId);

            if (availableOptionInput) {
                var customizationOptionStatus = '';
                if (availableOptionInput.selected === true) {
                    customizationOptionStatus = 'ac'
                } else {
                    customizationOptionStatus = 'uv'
                }
            }


            // API call for Item Customization Update
            if (customizationOptionId) {
            fetch(base_url + "/api/merchant-item-customization-options/" + customizationOptionId + "/partial_update_self/", {
            method: 'PATCH',
            body: JSON.stringify({
                'status': customizationOptionStatus
            }),
                headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken,
            }
            })
            .then(response => response.json())
              .then(result => {})
                .catch(error => console.log('error', error));
        }
        }

        Swal.fire(
              'Succès !',
              'Bravo 👏👏👏',
              'success'
          )

}


function populateArticleModal(articleId, base_url, cloudinary_cloud_name) {
    var itemClUrl = 'https://res.cloudinary.com/' + cloudinary_cloud_name + '/image/upload/w_150,h_150,c_fit/';
    var itemClUrlFull = 'https://res.cloudinary.com/' + cloudinary_cloud_name + '/image/upload/';
    var myHeaders = new Headers();
     var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
     };

    fetch(base_url + "/api/merchant-items/" + articleId + "/retrieve_self/", requestOptions)
      .then(response => response.json())
      .then(result => {
          var targetArticle = result;

          // Populate Item Section
          var articleDetailsModal = document.getElementById('articleDetailsModal');
          articleDetailsModal.dataset.articleid = '';
          articleDetailsModal.dataset.articleid  = targetArticle["id"];

          var admInputName = document.getElementById('admInputName');
          admInputName.value = '';
          admInputName.value = targetArticle["name"];

          var admInputDescription = document.getElementById('admInputDescription');
          admInputDescription.value = '';
          admInputDescription.value = targetArticle["description"];

          var admInputDisplayOrder = document.getElementById('admInputDisplayOrder');
          admInputDisplayOrder.value = '';
          admInputDisplayOrder.value = targetArticle["display_order"];

          var admInputStatusAvailable = document.getElementById('admInputStatusAvailable');
          var admInputStatusUnavailable = document.getElementById('admInputStatusUnavailable');
          admInputStatusAvailable.selected = '';
          admInputStatusUnavailable.selected = '';

          if (targetArticle['status'] === 'ac') {
              admInputStatusAvailable.selected = 'selected';
          }
          else {
              admInputStatusUnavailable.selected = 'selected';
          }

          var admInputImage = document.getElementById('admInputImage');
          admInputImage.innerHTML = '';
          admInputImage.innerHTML = "<a href='" + itemClUrlFull + targetArticle['article_image'].replace('image/upload/', '') + "' target='_blank'><img style='max-width: 100%' src='" + itemClUrl + targetArticle['article_image'].replace('image/upload/', '') + "' /> </a>";


          // Populate Item Customization Section
          var myOptionsContainer = document.getElementById("optionsContainer");
          myOptionsContainer.innerHTML = '';

          for (i in targetArticle['merchant_item_customizations']) {

              var targetMerchCustom = targetArticle['merchant_item_customizations'][i];
              var targetMerchCustomId = targetMerchCustom['id'];

              var myOptionDiv = document.createElement('div');
              myOptionDiv.className = "my-options-div";
              myOptionDiv.id = targetMerchCustomId;
              myOptionDiv.innerHTML = "<!-- Item Option Name -->\n" +
                  "                        <div class=\"form-group row\">\n" +
                  "                            <div class=\"col-sm-8\">\n" +
                  "                                <input id='option-name-" + targetMerchCustomId + "' disabled type=\"text\" value='Option - " + targetMerchCustom['name'] + "' class=\"form-control form-control-user\" placeholder=\"Nom de l'option\">\n" +
                  "                            </div>\n" +
                  "                            \n" +
                  "                            <div class=\"col-sm-4\">\n" +
                  "                                <select type=\"text\" class=\"form-control form-control-user custom-select\">\n" +
                  "                                    <option id='option-available-" + targetMerchCustomId + "' value=\"ac\">Disponible</option>\n" +
                  "                                    <option id='option-unavailable-" + targetMerchCustomId + "' value=\"uv\">Indisponible</option>\n" +
                  "                                </select>\n" +
                  "                            </div>\n" +
                  "                        </div>";

              myOptionsContainer.appendChild(myOptionDiv);

              var optionAvailable = document.getElementById('option-available-' + targetMerchCustomId);
              var optionUnavailable = document.getElementById('option-unavailable-' + targetMerchCustomId);
              optionAvailable.selected = '';
              optionUnavailable.selected = '';

              if (targetMerchCustom['status'] === 'ac') {
                  optionAvailable.selected = 'selected';
              }
              else {
                  optionUnavailable.selected = 'selected';
              }

              // Populate Item Customization Option Section
              var myItemCustomizationListDiv = document.createElement("div");
                  myItemCustomizationListDiv.className = 'item-customization-options-list';

              for (n in targetMerchCustom['merchant_item_customization_options']) {
                  var targetMerchCustomOption = targetMerchCustom['merchant_item_customization_options'][n]['item'];
                  var targetMerchCustomOptionId = targetMerchCustomOption['id'];
                  var targetMerchCustomOptionName = targetMerchCustomOption['name'];

                  var myItemCustomizationDiv = document.createElement("div");
                  myItemCustomizationDiv.className = 'item-customization-option-item';
                  myItemCustomizationDiv.id = targetMerchCustomOptionId;

                  var targetMerchCustomOptionPrice = String(Intl.NumberFormat('fr-FR', {
                              style: 'currency',
                              currency: 'EUR'
                          }).format(targetMerchCustomOption['price_vat_included']));

                  myItemCustomizationDiv.innerHTML = "<div class=\"form-group row\">\n" +
                      "                                <div class=\"col-sm-1\">\n" +
                      "                                    <p class=\"form-control form-control-options\" style=\"margin-bottom: 0; border: none\">➡️️</p>\n" +
                      "                                </div>\n" +
                      "\n" +
                      "                                <div class=\"col-sm-7\">\n" +
                      "                                    <input id='option-customization-name-" + targetMerchCustomOptionId + "' disabled type=\"text\" value='" + targetMerchCustomOptionName + " (+" + targetMerchCustomOptionPrice + ")' class=\"form-control form-control-options\" placeholder=\"\">\n" +
                      "                                </div>\n" +
                      "\n" +
                      "                                <div class=\"col-sm-4\">\n" +
                      "                                    <select type=\"text\" class=\"form-control form-control-options custom-select\">\n" +
                      "                                        <option id='option-customization-available-" + targetMerchCustomOptionId + "' value=\"ac\">Disponible</option>\n" +
                      "                                        <option id='option-customization-unavailable-" + targetMerchCustomOptionId + "' value=\"uv\">Indisponible</option>\n" +
                      "                                    </select>\n" +
                      "                                </div>\n" +
                      "                            </div>";


                  myItemCustomizationListDiv.appendChild(myItemCustomizationDiv);
                  myOptionsContainer.appendChild(myItemCustomizationListDiv);

                  var optionCustomizationAvailable = document.getElementById('option-customization-available-' + targetMerchCustomOptionId);
                  var optionCustomizationUnavailable = document.getElementById('option-customization-unavailable-' + targetMerchCustomOptionId);
                  optionCustomizationAvailable.selected = '';
                  optionCustomizationUnavailable.selected = '';

                   if (targetMerchCustomOption['status'] === 'ac') {
                       optionCustomizationAvailable.selected = 'selected';
                   }
                   else {
                       optionCustomizationUnavailable.selected = 'selected';
                   }
              }

          }

      })
        .catch(error => console.log('error', error));
}



