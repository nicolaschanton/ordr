function updateOrder(base_url, order_state, orderId) {
    var csrftoken = getCookie('csrftoken');

    fetch(base_url + "/api/customer-orders/" + orderId + "/partial_update_self/", {
        method: 'PATCH',
        body: JSON.stringify({
            'order_state': order_state
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
      .then(result => {
          getTBVOrders(base_url);
          getTBTOrders(base_url);

          Swal.fire(
              'Succès !',
              'Bravo 👏👏👏',
              'success'
          )
      })
        .catch(error => console.log('error', error));
}


function getTBVOrders(base_url, cloudinary_cloud_name) {
    var myHeaders = new Headers();
    var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    };

    var myTableBody = document.getElementById('tbvOrdersTable');
    myTableBody.innerHTML = '';
    localStorage.removeItem('tbv_orders');


    fetch(base_url + "/api/customer-orders/list_self/?order_state=pa", requestOptions)
      .then(response => response.json())
      .then(result => {
          var dataToStore = JSON.stringify(result);
          localStorage.setItem('tbv_orders', dataToStore);

            for(i in result){
                var order = result[i];

                    var merchantTable = order['merchant_table'];
                    var customer = order['customer'];
                    var orderLines = order['customer_order_lines'];
                    var countOrderLines = Object.keys(orderLines).length;
                    var myTr = document.createElement('tr');
                    var myTd1 = document.createElement('td');
                    var myTd2 = document.createElement('td');
                    var myTd3 = document.createElement('td');
                    var myTd4 = document.createElement('td');
                    var myTd5 = document.createElement('td');
                    var myTd6 = document.createElement('td');
                    var orderId = order['id'];

                    myTd1.textContent = order['id'].substring(0, 5);
                    myTd2.textContent = merchantTable['table_number'];
                    myTd3.textContent = customer['first_name'];
                    myTd4.textContent = String(countOrderLines);
                    myTd5.textContent = String(Intl.NumberFormat('fr-FR', {
                        style: 'currency',
                        currency: 'EUR'
                    }).format(order['total_amount_vat_included']));
                    myTd6.innerHTML = "<a href='' onclick='populateOrderModal(\""+ orderId + "\", \"" + base_url + "\", \"" + cloudinary_cloud_name + "\")' data-toggle='modal' data-target='#viewOrderModal' class='btn btn-danger'>Annuler</a>\n" +
                        "<a href='' onclick='populateOrderModal(\""+ orderId + "\", \"" + base_url + "\", \"" + cloudinary_cloud_name + "\")' data-toggle='modal' data-target='#viewOrderModal' class='btn btn-success'>Accepter</a>\n";
                    myTr.appendChild(myTd1);
                    myTr.appendChild(myTd2);
                    myTr.appendChild(myTd3);
                    myTr.appendChild(myTd4);
                    myTr.appendChild(myTd5);
                    myTr.appendChild(myTd6);
                    myTableBody.appendChild(myTr);
            }
      }
            )
      .catch(error => console.log('error', error));

}


function getTBTOrders(base_url, cloudinary_cloud_name) {
    var myHeaders = new Headers();
    var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
    };

    var myTableBody = document.getElementById('tbtOrdersTable');
    myTableBody.innerHTML = '';
    localStorage.removeItem('tbt_orders');

    fetch(base_url + "/api/customer-orders/list_self/?order_state=pr", requestOptions)
      .then(response => response.json())
      .then(result => {
          var dataToStore = JSON.stringify(result);
          localStorage.setItem('tbt_orders', dataToStore);

            for(i in result){
                var order = result[i];

                    var merchantTable = order['merchant_table'];
                    var customer = order['customer'];
                    var orderLines = order['customer_order_lines'];
                    var countOrderLines = Object.keys(orderLines).length;
                    var myTr = document.createElement('tr');
                    var myTd1 = document.createElement('td');
                    var myTd2 = document.createElement('td');
                    var myTd3 = document.createElement('td');
                    var myTd4 = document.createElement('td');
                    var myTd5 = document.createElement('td');
                    var myTd6 = document.createElement('td');
                    var orderId = order['id'];

                    myTd1.textContent = order['id'].substring(0, 5);
                    myTd2.textContent = merchantTable['table_number'];
                    myTd3.textContent = customer['first_name'];
                    myTd4.textContent = String(countOrderLines);
                    myTd5.textContent = String(Intl.NumberFormat('fr-FR', {
                        style: 'currency',
                        currency: 'EUR'
                    }).format(order['total_amount_vat_included']));
                    myTd6.innerHTML = "<a href='' onclick='populateOrderModal(\""+ orderId + "\", \"" + base_url + "\", \"" + cloudinary_cloud_name + "\")' data-toggle='modal' data-target='#viewOrderModal' class='btn btn-success'>Prête ?</a>\n" +
                        "<a href='' onclick='populateOrderModal(\""+ orderId + "\", \"" + base_url + "\")' data-toggle='modal' data-target='#viewOrderModal' class='btn btn-primary'>Voir</a>\n";
                    myTr.appendChild(myTd1);
                    myTr.appendChild(myTd2);
                    myTr.appendChild(myTd3);
                    myTr.appendChild(myTd4);
                    myTr.appendChild(myTd5);
                    myTr.appendChild(myTd6);
                    myTableBody.appendChild(myTr);
            }
      }
            )
      .catch(error => console.log('error', error));

}


function populateOrderModal(orderId, base_url, cloudinary_cloud_name) {
    var itemClUrl = 'https://res.cloudinary.com/' + cloudinary_cloud_name + '/image/upload/w_100,h_100,c_fit/';

     var myHeaders = new Headers();
     var requestOptions = {
      method: 'GET',
      headers: myHeaders,
      redirect: 'follow'
     };

    fetch(base_url + "/api/customer-orders/" + orderId + "/retrieve_self/", requestOptions)
      .then(response => response.json())
      .then(result => {
          var targetOrder = result;
          var customer_order_lines = targetOrder['customer_order_lines'];

          var InputTableNumber = document.getElementById('InputTableNumber');
          InputTableNumber.textContent = '';
          InputTableNumber.textContent = 'Table n°' + targetOrder['merchant_table']['table_number'];

          var InputOrderNumber = document.getElementById('InputOrderNumber');
          InputOrderNumber.textContent = targetOrder['id'].substring(0, 5);

          var InputCustomerName = document.getElementById('InputCustomerName');
          InputCustomerName.textContent = targetOrder['customer']['first_name'];

          var myTableBody = document.getElementById('detailsOrderModalTable');
          myTableBody.textContent = '';

          for (i in customer_order_lines) {
              var order_line = customer_order_lines[i];

              var myTr = document.createElement('tr');
              var myTd1 = document.createElement('td');
              var myTd2 = document.createElement('td');
              var myTd3 = document.createElement('td');
              var myTd4 = document.createElement('td');


              myTd1.innerHTML = "<img height='50px' src='" + itemClUrl + order_line['item']['article_image'].replace('image/upload/', '') + "' />";
              myTd2.textContent = order_line['item']['name'] + ' - ' + order_line['item']['description'].substring(0, 25) + "...";
              myTd3.textContent = order_line['quantity'];
              myTd4.textContent = String(Intl.NumberFormat('fr-FR', {
                  style: 'currency',
                  currency: 'EUR'
              }).format(order_line['total_amount_vat_included']));

              myTr.appendChild(myTd1);
              myTr.appendChild(myTd2);
              myTr.appendChild(myTd3);
              myTr.appendChild(myTd4);
              myTableBody.appendChild(myTr);

          }

          // Total HT
          var myTotalHtTr = document.createElement('tr');
          var myTotalHtTd1 = document.createElement('td');
          var myTotalHtTd2 = document.createElement('td');
          var myTotalHtTd3 = document.createElement('td');
          var myTotalHtTd4 = document.createElement('td');

          myTotalHtTd1.textContent = '';
          myTotalHtTd2.textContent = '';
          myTotalHtTd3.textContent = 'Total HT';
          myTotalHtTd4.textContent = String(Intl.NumberFormat('fr-FR', {
              style: 'currency',
              currency: 'EUR'
          }).format(targetOrder['total_amount_vat_excluded']));

          myTotalHtTr.appendChild(myTotalHtTd1);
          myTotalHtTr.appendChild(myTotalHtTd2);
          myTotalHtTr.appendChild(myTotalHtTd3);
          myTotalHtTr.appendChild(myTotalHtTd4);
          myTableBody.appendChild(myTotalHtTr);

          // Total VAT
          var vatAmount = targetOrder['vat_amount_1'] + targetOrder['vat_amount_2'] + targetOrder['vat_amount_3'];
          var myTotalVatTr = document.createElement('tr');
          var myTotalVatTd1 = document.createElement('td');
          var myTotalVatTd2 = document.createElement('td');
          var myTotalVatTd3 = document.createElement('td');
          var myTotalVatTd4 = document.createElement('td');

          myTotalVatTd1.textContent = '';
          myTotalVatTd2.textContent = '';
          myTotalVatTd3.textContent = 'Total TVA';
          myTotalVatTd4.textContent = String(Intl.NumberFormat('fr-FR', {
              style: 'currency',
              currency: 'EUR'
          }).format(vatAmount));

          myTotalVatTr.appendChild(myTotalVatTd1);
          myTotalVatTr.appendChild(myTotalVatTd2);
          myTotalVatTr.appendChild(myTotalVatTd3);
          myTotalVatTr.appendChild(myTotalVatTd4);
          myTableBody.appendChild(myTotalVatTr);

          // Total TTC
          var myTotalTtcTr = document.createElement('tr');
          var myTotalTtcTd1 = document.createElement('td');
          var myTotalTtcTd2 = document.createElement('td');
          var myTotalTtcTd3 = document.createElement('td');
          var myTotalTtcTd4 = document.createElement('td');

          myTotalTtcTd1.textContent = '';
          myTotalTtcTd2.textContent = '';
          myTotalTtcTd3.textContent = 'Total TTC';
          myTotalTtcTd4.textContent = String(Intl.NumberFormat('fr-FR', {
              style: 'currency',
              currency: 'EUR'
          }).format(targetOrder['total_amount_vat_included']));

          myTotalTtcTr.appendChild(myTotalTtcTd1);
          myTotalTtcTr.appendChild(myTotalTtcTd2);
          myTotalTtcTr.appendChild(myTotalTtcTd3);
          myTotalTtcTr.appendChild(myTotalTtcTd4);
          myTableBody.appendChild(myTotalTtcTr);

          var myButtonGroup = document.getElementById('detailsOrderModalButtons');
          myButtonGroup.innerHTML = '';
          var orderState = targetOrder['order_state'];

          if (orderState === 'pa') {
              myButtonGroup.innerHTML = "<button onclick='updateOrder(\""+ base_url + "\", \"" + "re" + "\", \"" + orderId + "\")' class=\"btn btn-danger\" type=\"button\" data-dismiss=\"modal\">Annuler</button>\n" +
                  "                <button class=\"btn btn-outline-primary\" type=\"button\" data-dismiss=\"modal\">Retour</button>\n" +
                  "                <button onclick='updateOrder(\""+ base_url + "\", \"" + "pr" + "\", \"" + orderId + "\")' class=\"btn btn-success\" type=\"button\" data-dismiss=\"modal\">Accepter</button>";
          } else if (orderState === 'pr') {
              myButtonGroup.innerHTML = "<button class=\"btn btn-outline-primary\" type=\"button\" data-dismiss=\"modal\">Retour</button>\n" +
                  "                <button onclick='updateOrder(\""+ base_url + "\", \"" + "do" + "\", \"" + orderId + "\")' class=\"btn btn-success\" type=\"button\" data-dismiss=\"modal\">Terminer</button>";
                }
          else if (["er", "re", "rf", "de"].includes(orderState)) {
              myButtonGroup.innerHTML = "<button class=\"btn btn-outline-primary\" type=\"button\" data-dismiss=\"modal\">Retour</button>\n"
          }

          else if (orderState === 'do') {
              myButtonGroup.innerHTML = "<button class=\"btn btn-outline-primary\" type=\"button\" data-dismiss=\"modal\">Retour</button>\n"
          }

      })
        .catch(error => console.log('error', error));
}
