function showLoader() {
    var myLoader = document.getElementById('my-loader');
    myLoader.style.display = 'block';
}


function hideLoader() {
    var myLoader = document.getElementById('my-loader');
    myLoader.style.display = 'none';
}


function scrollToHeader(categoryId) {
    var categoryDiv = document.getElementById(categoryId);

    scrollTo({
        top: categoryDiv.offsetTop - 80,
        left: 0,
        behavior: 'smooth'
    })
}


function redirectToPaymentPage(stripe_pk, base_url, table_merchant_id, customer_id) {
    showLoader();
    var stripe = Stripe(stripe_pk);
    var csrftoken = getCookie('csrftoken');
    var myBasketLocal = JSON.parse(sessionStorage.getItem('basket'));

    fetch(base_url + "/api/endpoints/orders/create_order_from_basket/", {
        method: 'POST',
        body: JSON.stringify({
            'table_merchant_id': table_merchant_id,
            'customer_id': customer_id,
            'basket': myBasketLocal
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
      .then(result => {
          var checkout_session_id = result["checkout_session_id"];
          stripe.redirectToCheckout({
              sessionId: checkout_session_id
          }).then(function (result) {
              console.log(result);
          });

      })
        .catch(error => console.log('error', error));
}


function addItemBasket(itemObject, quantity) {
        var myBasketJson = JSON.parse(sessionStorage.getItem('basket'));

        // Session storage has already basket in it
        if (myBasketJson && myBasketJson.length > 0) {
            itemObject["options"] = [];

            // Push new item to create new order line if it has option in it
            if (itemObject["options"].length > 0) {
                itemObject["quantity"] = quantity;
                myBasketJson.push(itemObject);

                // Push new item to update new order line with new quantity
            } else {
                for (i in myBasketJson) {

                    if (myBasketJson[i]['id'] === itemObject['id']) {
                        myBasketJson[i]["quantity"] = myBasketJson[i]["quantity"] + quantity;
                        var modifier = "OK";
                        break;
                    }
                }

                // Push new item to create new order line
                if (modifier !== "OK") {
                    modifier = "NOK";
                    itemObject["quantity"] = quantity;
                    myBasketJson.push(itemObject);
                }

            }
            // Update session storage
            sessionStorage.removeItem('basket');
            sessionStorage.setItem('basket', JSON.stringify(myBasketJson));

        } else {
            // Session storage has no basket in it, we can push a new order line
            sessionStorage.clear();
            itemObject["quantity"] = quantity;
            itemObject["options"] = [];
            sessionStorage.setItem('basket', JSON.stringify([itemObject]));
        }

        calculateBasketAmount();
}


function removeItemBasket(itemObject, quantity) {
    var myBasketJson = JSON.parse(sessionStorage.getItem('basket'));


    calculateBasketAmount();
}


function clearBasket() {
    sessionStorage.removeItem('basket');
}


function populateMenu(base_url, table_merchant_id, cloudinary_cloud_name) {
    var itemClUrl = 'https://res.cloudinary.com/' + cloudinary_cloud_name + '/image/upload/w_400,h_400,c_fit/';
    var divItemContainer = document.getElementsByClassName('merchant-item-container')[0];
    divItemContainer.innerHTML = '';

    // API call for retrieving merchant active item categories
    fetch(base_url + "/api/merchant-item-categories/list_public_with_items/?merchant_table_id=" + table_merchant_id, {
        method: 'GET',
        headers: {'Content-type': 'application/json; charset=UTF-8'}
        })
        .then(response => response.json())
          .then(result => {

              for (c in result){
                  var mainCategory = result[c];
                  var mainCategoryId = mainCategory["id"];
                  var myScrollMenu = document.getElementById('category-scrollmenu');
                  var myCategoryElement = document.createElement('a');

                  myCategoryElement.textContent = mainCategory["name"];
                  myCategoryElement.id = "header-category-" + mainCategoryId;
                  function getHandler(mainCategoryIdBis) {
                      return function () {
                            scrollToHeader(mainCategoryIdBis);
                      }
                  }
                  myCategoryElement.onclick = getHandler(mainCategoryId);
                  myScrollMenu.appendChild(myCategoryElement);
              }

              for (i in result) {
                  var category = result[i];
                  var merchant_item_category_id = category['id'];
                  var items_list = category["merchant_items"];

                  var myTitleCategory = document.createElement('h4');
                  myTitleCategory.className = "merchant-category-title";
                  myTitleCategory.textContent = category["name"];

                  var myDivCategory = document.createElement('div');
                  myDivCategory.className = "merchant-category vw-100";
                  myDivCategory.id = merchant_item_category_id;

                  myDivCategory.appendChild(myTitleCategory);

                  for (j in items_list) {
                              var item = items_list[j];

                              var myDivItem = document.createElement('div');
                              myDivItem.className = "merchant-item col-xs-12 col-sm-12 col-md-12 col-lg-12 pt-1";
                              myDivItem.id = "item-div-" + item['id'];

                              var myItemPrice = String(Intl.NumberFormat('fr-FR', {
                                  style: 'currency',
                                  currency: 'EUR'
                              }).format(item['price_vat_included']));

                              myDivItem.innerHTML = "<div class=\"row mt-3\">\n" +
                                  "\n" +
                                  "            <div class=\"col-9\">\n" +
                                  "                <h6 class=\"merchant-item-title\">"+ item['name'] + "</h6>\n" +
                                  "                <p class=\"merchant-item-description\">" + item['description'].substring(0, 100) +"</p>\n" +
                                  "            </div>\n" +
                                  "\n" +
                                  "            <div class=\"col-3 menu-product__img\" style=\"background-image: url(" + itemClUrl + item['article_image'].replace('image/upload/', '').replace(".png", ".jpg") + ");\">\n" +
                                  "            </div>\n" +
                                  "\n" +
                                  "        </div>\n" +
                                  "            <div class=\"row mt-3\">\n" +
                                  "\n" +
                                  "            <div class=\"col-5\">\n" +
                                  "                <div class=\"row pl-3 mb-2\">\n" +
                                  "\n" +
                                  "                    <div class=\"col-4 pl-0 pr-0 \">\n" +
                                  "                        <button id='" + "item-remove-" + item['id'] + "' class=\"btn btn-success\">-</button>\n" +
                                  "                    </div>\n" +
                                  "\n" +
                                  "                    <div class=\"col-4 pl-0 pr-0\">\n" +
                                  "                        <h6 id='" + "item-counter-" + item['id'] + "' class=\"counter-item\">0</h6>\n" +
                                  "                    </div>\n" +
                                  "\n" +
                                  "                    <div class=\"col-4 pl-0 pr-0\">\n" +
                                  "                        <button id='" + "item-add-" + item['id'] + "' onclick='populateDetailItemModal(\""+ base_url + "\", \"" + item['id'] + "\", \"" + cloudinary_cloud_name + "\")' data-toggle=\"modal\" data-target=\"#itemModal\" class=\"btn btn-success\">+</button>\n" +
                                  "                    </div>\n" +
                                  "\n" +
                                  "                </div>\n" +
                                  "\n" +
                                  "            </div>\n" +
                                  "\n" +
                                  "            <div class=\"col-7 pl-3\">\n" +
                                  "                        <p id='" + "item-total-price-" + item['id'] + "' class=\"menu-product__price\">" + myItemPrice + "</p>\n" +
                                  "            </div>\n" +
                                  "\n" +
                                  "        </div>";

                              myDivCategory.appendChild(myDivItem)

                          }
                  divItemContainer.appendChild(myDivCategory)
              }

          })
            .catch(error => console.log('error', error));



}


function populateDetailItemModal(base_url, item_id, cloudinary_cloud_name){
    var itemClUrl = 'https://res.cloudinary.com/' + cloudinary_cloud_name + '/image/upload/w_800,h_800,c_fit/';
    var myItemModalTitle = document.getElementsByClassName('product-popup__name')[0];
    var myItemDetailAddButtonContainer = document.getElementById('add-to-cart-button-container');
    var myItemDetailHeaderImage= document.getElementsByClassName('modal-item-detail-header-img')[0];
    var myItemDetailDescription = document.getElementsByClassName('product-popup__description')[0];
    // var myItemDetailCustomContainer = document.getElementById('modal-item-detail-custom-container');

    // Reinit image to avoid transition
    myItemDetailHeaderImage.style = '';

    // Reinit Customization container
    // myItemDetailCustomContainer.innerHTML = '';

    // API call for retrieving Item details
    fetch(base_url + "/api/merchant-items/" + item_id + "/retrieve_public/", {
        method: 'GET',
        headers: {'Content-type': 'application/json; charset=UTF-8'}
        })
        .then(response => response.json())
          .then(result => {
              var item = result;

              // Detail & price & description
              myItemDetailHeaderImage.style = 'background-image: url(' + itemClUrl + item['article_image'].replace('image/upload/', '').replace(".png", ".jpg") + ');';
              myItemModalTitle.textContent = item["name"];
              myItemDetailDescription.textContent = item["description"];

              // Add to cart Button
              var myButtonContent = "Ajouter au panier (" + String(Intl.NumberFormat('fr-FR', {
                                  style: 'currency',
                                  currency: 'EUR'
                              }).format(item['price_vat_included'])) + ")";
              myItemDetailAddButtonContainer.innerHTML = "<button data-dismiss=\"modal\" id=\"add-to-cart-button\" class=\"green-btn--md basket-button--toggle is-fill add-to-cart-button\" type=\"button\">" + myButtonContent + "</button>\n";
              var myButtonAddToCart = document.getElementById('add-to-cart-button');
              myButtonAddToCart.onclick = function () {
                  addItemBasket(item, 1)
              };

              // Display for Customizations & Options
              for (i in item["merchant_item_customizations"]){
                   var myCustom = item["merchant_item_customizations"][i];

                  for (j in myCustom["merchant_item_customization_options"]) {
                      var myCustomOption = myCustom["merchant_item_customization_options"][j];

                  }
              }

          })
            .catch(error => console.log('error', error));

}


function populateBasket(base_url, cloudinary_cloud_name) {
    var itemClUrl = 'https://res.cloudinary.com/' + cloudinary_cloud_name + '/image/upload/w_400,h_400,c_fit/';
    var divBasketContainer = document.getElementsByClassName('merchant-basket-container')[0];
    divBasketContainer.innerHTML = '';

    // Get Local Storage for retrieving item added to cart
    var myBasket = JSON.parse(sessionStorage.getItem('basket'));

    for (j in myBasket) {
        var item = myBasket[j];

        var myDivItem = document.createElement('div');
        myDivItem.className = "basket-item col-xs-12 col-sm-12 col-md-12 col-lg-12 pt-1 mb-2";
        myDivItem.id = item["id"];

        var myItemPrice = String(Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(item['price_vat_included']));

        myDivItem.innerHTML = "<div class=\"row mt-3\">\n" +
                                  "\n" +
                                  "            <div class=\"col-9\">\n" +
                                  "                <h6 class=\"merchant-item-title\">"+ item['name'] + "</h6>\n" +
                                  "                <p class=\"merchant-item-description\">" + item['description'].substring(0, 100) +"</p>\n" +
                                  "            </div>\n" +
                                  "\n" +
                                  "            <div class=\"col-3 menu-product__img\" style=\"background-image: url(" + itemClUrl + item['article_image'].replace('image/upload/', '').replace(".png", ".jpg") + ");\">\n" +
                                  "            </div>\n" +
                                  "\n" +
                                  "        </div>\n" +
                                  "            <div class=\"row mt-3\">\n" +
                                  "\n" +
                                  "            <div class=\"col-5\">\n" +
                                  "                <div class=\"row pl-3 mb-2\">\n" +
                                  "\n" +
                                  "                    <div class=\"col-4 pl-0 pr-0 \">\n" +
                                  "                        <button id='" + "remove-" + item['id'] + "' class=\"btn btn-success\">-</button>\n" +
                                  "                    </div>\n" +
                                  "\n" +
                                  "                    <div class=\"col-4 pl-0 pr-0\">\n" +
                                  "                        <h6 id='" + "counter-" + item['id'] + "' class=\"counter-item\">0</h6>\n" +
                                  "                    </div>\n" +
                                  "\n" +
                                  "                    <div class=\"col-4 pl-0 pr-0\">\n" +
                                  "                        <button id='" + "add-" + item['id'] + "' onclick='populateDetailItemModal(\""+ base_url + "\", \"" + item['id'] + "\", \"" + cloudinary_cloud_name + "\")' data-toggle=\"modal\" data-target=\"#itemModal\" class=\"btn btn-success\">+</button>\n" +
                                  "                    </div>\n" +
                                  "\n" +
                                  "                </div>\n" +
                                  "\n" +
                                  "            </div>\n" +
                                  "\n" +
                                  "            <div class=\"col-7 pl-3\">\n" +
                                  "                        <p id=\"\" class=\"menu-product__price\">" + myItemPrice + "</p>\n" +
                                  "            </div>\n" +
                                  "\n" +
                                  "        </div>";

                              divBasketContainer.appendChild(myDivItem)

                          }
              }


function calculateBasketAmount() {
    var myBasketButtonValue = document.getElementById('see-basket-button-amount');
    var validateBasketButton = document.getElementById('validate-cart-button');

        var sessionStorageBasket = JSON.parse(sessionStorage.getItem('basket'));
        var myTotalAmount = 0;

        for (j in sessionStorageBasket) {
            var orderLine = sessionStorageBasket[j];
            myTotalAmount += orderLine["quantity"] * orderLine["price_vat_included"];
        }

        // Update View Cart Button
        myBasketButtonValue.textContent = String(Intl.NumberFormat('fr-FR', {
                                  style: 'currency',
                                  currency: 'EUR'
                              }).format(myTotalAmount));


        // Update Validate Cart Button
        validateBasketButton.textContent = "Valider mon panier (" + String(Intl.NumberFormat('fr-FR', {
                                  style: 'currency',
                                  currency: 'EUR'
                              }).format(myTotalAmount)) + ")";
    }


function archive() {
        var myItemCounter = document.getElementById("item-counter-" + itemObject['id']);
        var myItemDiv = document.getElementById("item-div-" + itemObject['id']);
        var myItemTotalPrice = document.getElementById("item-total-price-" + itemObject['id']);
        var myItemCounterValue;

        if (myItemCounter.textContent === '0') {
            myItemCounterValue = 0 + quantity;
            myItemDiv.classList.add('item-chosen');

        } else {
            myItemCounterValue = parseInt(myItemCounter.textContent) + quantity;
        }

        myItemCounter.textContent = myItemCounterValue.toString();
        myItemTotalPrice.textContent = String(Intl.NumberFormat('fr-FR', {
                                  style: 'currency',
                                  currency: 'EUR'
                              }).format(itemObject['price_vat_included'] * myItemCounterValue));
}