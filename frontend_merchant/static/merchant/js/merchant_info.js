function populateMerchantInfo(base_url, merchant_id) {
    var MerchantNameInput = document.getElementById("MerchantName");
    var MerchantOpenInput = document.getElementById("MerchantOpen");
    var MerchantDescriptionInput = document.getElementById("MerchantDescription");
    var MerchantRegistrationNumberInput = document.getElementById("MerchantRegistrationNumber");
    var MerchantVatNumberInput = document.getElementById("MerchantVatNumber");
    var MerchantAddressStreetInput = document.getElementById("MerchantAddressStreet");
    var MerchantAddressCityInput = document.getElementById("MerchantAddressCity");
    var MerchantAddressZipInput = document.getElementById("MerchantAddressZip");
    var MerchantServiceBarInput = document.getElementById("MerchantServiceBar");
    var MerchantServiceTableInput = document.getElementById("MerchantServiceTable");
    var MerchantPaymentInput = document.getElementById("MerchantPayment");
    var MerchantOwnerNameInput = document.getElementById("MerchantOwnerName");
    var MerchantEmailInput = document.getElementById("MerchantEmail");
    var MerchantPhoneInput = document.getElementById("MerchantPhone");

    // API call for retrievin merchant info
    fetch(base_url + "/api/merchants/" + merchant_id + "/retrieve_self/", {
        method: 'GET',
        headers: {'Content-type': 'application/json; charset=UTF-8'}
        })
        .then(response => response.json())
          .then(result => {
                var MerchantNameValue = result["name"];
                var MerchantOpenValue = result["open"];
                var MerchantDescriptionValue = result["shop_description"];
                var MerchantRegistrationNumberValue = result["registration_number"];
                var MerchantVatNumberValue = result["vat_number"];
                var MerchantAddressStreetValue = result["address_street"];
                var MerchantAddressCityValue = result["address_city"];
                var MerchantAddressZipValue = result["address_zip"];
                var MerchantServiceBarValue = result["accept_service_bar"];
                var MerchantServiceTableValue = result["accept_service_table"];
                var MerchantPaymentValue = result["accept_cash"];
                var MerchantOwnerNameValue = result["owner_name"];
                var MerchantEmailValue = result["email"];
                var MerchantPhoneValue = result["phone"];

                MerchantNameInput.value = MerchantNameValue;
                MerchantDescriptionInput.value = MerchantDescriptionValue;
                MerchantRegistrationNumberInput.value = MerchantRegistrationNumberValue;
                MerchantVatNumberInput.value = MerchantVatNumberValue;
                MerchantAddressStreetInput.value = MerchantAddressStreetValue;
                MerchantAddressCityInput.value = MerchantAddressCityValue;
                MerchantAddressZipInput.value = MerchantAddressZipValue;
                MerchantOwnerNameInput.value = MerchantOwnerNameValue;
                MerchantEmailInput.value = MerchantEmailValue;
                MerchantPhoneInput.value = MerchantPhoneValue;

                if (MerchantOpenValue === true) {
                    MerchantOpenInput.checked = 'checked';
                }

                if (MerchantServiceBarValue === true) {
                    MerchantServiceBarInput.checked = 'checked';
                }

                if (MerchantServiceTableValue === true) {
                    MerchantServiceTableInput.checked = 'checked';
                }

                if (MerchantPaymentValue === true) {
                    MerchantPaymentInput.checked = 'checked';
                }


          })
            .catch(error => console.log('error', error));

}


function updateInfoGeneral(base_url, merchant_id) {
    var MerchantNameInput = document.getElementById("MerchantName");
    var MerchantOpenInput = document.getElementById("MerchantOpen");
    var MerchantDescriptionInput = document.getElementById("MerchantDescription");
    var MerchantRegistrationNumberInput = document.getElementById("MerchantRegistrationNumber");
    var MerchantVatNumberInput = document.getElementById("MerchantVatNumber");
    var MerchantAddressStreetInput = document.getElementById("MerchantAddressStreet");
    var MerchantAddressCityInput = document.getElementById("MerchantAddressCity");
    var MerchantAddressZipInput = document.getElementById("MerchantAddressZip");

    var MerchantNameValue = MerchantNameInput.value;
    var MerchantDescriptionValue = MerchantDescriptionInput.value;
    var MerchantRegistrationNumberValue = MerchantRegistrationNumberInput.value;
    var MerchantVatNumberValue = MerchantVatNumberInput.value;
    var MerchantAddressStreetValue = MerchantAddressStreetInput.value;
    var MerchantAddressCityValue = MerchantAddressCityInput.value;
    var MerchantAddressZipValue = MerchantAddressZipInput.value;
    var MerchantOpenValue = MerchantOpenInput.checked;


    // API call for Merchant Update
    var csrftoken = getCookie('csrftoken');
    fetch(base_url + "/api/merchants/" + merchant_id + "/partial_update_self/", {
        method: 'PATCH',
        body: JSON.stringify({
            "name": MerchantNameValue,
            "open": MerchantOpenValue,
            "registration_number": MerchantRegistrationNumberValue,
            "vat_number": MerchantVatNumberValue,
            "address_street": MerchantAddressStreetValue,
            "address_city": MerchantAddressCityValue,
            "address_zip": MerchantAddressZipValue,
            "shop_description": MerchantDescriptionValue,
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
      .then(result => {

          Swal.fire(
              'Succès !',
              'Bravo 👏👏👏',
              'success'
          )

      })
        .catch(error => console.log('error', error));



}


function updateInfoService(base_url, merchant_id) {
    var MerchantServiceBarInput = document.getElementById("MerchantServiceBar");
    var MerchantPaymentInput = document.getElementById("MerchantPayment");
    var MerchantServiceTableInput = document.getElementById("MerchantServiceTable");

    var MerchantServiceTableValue = MerchantServiceTableInput.checked;
    var MerchantServiceBarValue = MerchantServiceBarInput.checked;
    var MerchantPaymentValue = MerchantPaymentInput.checked;


    // API call for Merchant Update
    var csrftoken = getCookie('csrftoken');
    fetch(base_url + "/api/merchants/" + merchant_id + "/partial_update_self/", {
        method: 'PATCH',
        body: JSON.stringify({
            "accept_cash": MerchantPaymentValue,
            "accept_service_bar": MerchantServiceBarValue,
            "accept_service_table": MerchantServiceTableValue,
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
      .then(result => {

          Swal.fire(
              'Succès !',
              'Bravo 👏👏👏',
              'success'
          )

      })
        .catch(error => console.log('error', error));

}


function updateInfoOwner(base_url, merchant_id) {
    var MerchantOwnerNameInput = document.getElementById("MerchantOwnerName");
    var MerchantEmailInput = document.getElementById("MerchantEmail");
    var MerchantPhoneInput = document.getElementById("MerchantPhone");

    var MerchantOwnerNameValue = MerchantOwnerNameInput.value;
    var MerchantEmailValue = MerchantEmailInput.value;
    var MerchantPhoneValue = MerchantPhoneInput.value;

    // API call for Merchant Update
    var csrftoken = getCookie('csrftoken');
    fetch(base_url + "/api/merchants/" + merchant_id + "/partial_update_self/", {
        method: 'PATCH',
        body: JSON.stringify({
            "email": MerchantEmailValue,
            "phone": MerchantPhoneValue,
            "owner_name": MerchantOwnerNameValue,
        }),
            headers: {
            'Content-type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
      .then(result => {

          Swal.fire(
              'Succès !',
              'Bravo 👏👏👏',
              'success'
          )

      })
        .catch(error => console.log('error', error));



}