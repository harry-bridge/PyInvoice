function updateInvoice() {
  $.ajax({
    url : "/invoice/update/", // the endpoint
    type : "POST", // http method
    data : {
        invoice_form: $('#invoice-form').serialize()
    },
    traditional: true,

    success : function(data) {
        // console.log(data);
        window.location.href = data['url'];
    }
  });
}

function updateItem() {
  $.ajax({
    url : "/invoice/item/update/", // the endpoint
    type : "POST", // http method
    data : {
        invoice_pk: $('#invoice_pk').val(),
        item_pk : $('#item_pk').val(),
        description : $('#descriptionInput').val(),
        cost: $('#costInput').val()
    }, // data sent with the post request

    success : function(data) {
        $('.item_table').html(data);
        // console.log(data);
    },
    error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}
  });
}

function deleteItem(item_pk) {
  $.ajax({
    url : "/invoice/item/delete/", // the endpoint
    type : "POST", // http method
    data : {
        invoice_pk: $('#invoice_pk').val(),
        item_pk : item_pk
    }, // data sent with the post request

    success : function(data) {
        $('.item_table').html(data);
        // console.log(data);
    },
    error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}
  });
}

function getItemsForModal(item_pk) {
  $.ajax({
      url: "/api/get_items_for_table/", // the endpoint
      type: "POST", // http method
      data: {
          item_pk: item_pk
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          if (data['item_pk'] != 0) {
              $('#editStatus').text('Edit Item');
          } else {
             $('#editStatus').text('Add Item');
          }
          $('#item_pk').val(data['item_pk']);

          $('#descriptionInput').val(data['description']).removeClass('valid');
          $('#descriptionInputLabel').addClass('active');
          $('#costInput').val(data['cost']).removeClass('valid');
          $('#costInputLabel').addClass('active');
          // console.log(data);
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}
  });
}

function getCompanyForModal(company_pk) {
  $.ajax({
      url: "/api/get_company_for_modal/", // the endpoint
      type: "POST", // http method
      data: {
          company_pk: company_pk
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          $('#editStatusCompany').text('Edit Company');
          $('#nameInput').val(data['name']);
          $('#nameInputLabel').addClass('active');
          $('#addressInput').val(data['address']);
          $('#addressInputLabel').addClass('active');
          $('#emailInput').val(data['email']);
          $('#emailInputLabel').addClass('active');
          $('#company_pk').val(data['company_pk']);
          $('#redirect_on_save').val('0');
          console.log(data);
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}
  });
}

function updateCompany() {
  $.ajax({
      url: "/company/update/", // the endpoint
      type: "POST", // http method
      data: {
          company_pk: $('#company_pk').val(),
          name: $('#nameInput').val(),
          address: $('#addressInput').val(),
          email: $('#emailInput').val(),
          redirect_on_save: $('#redirect_on_save').val()
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          console.log(data);
          if (data['redirect']) {
                window.location.href = data['url'];
          } else {
              $('#company-select').append($('<option>', {
                    value: data['company_pk'],
                    text: data['company_name']
                })).val(data['company_pk']).material_select();
          }
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}

function deleteInvoice() {
  $.ajax({
      url: "/invoice/delete/", // the endpoint
      type: "POST", // http method
      data: {
          invoice_pk: $('#invoice_pk').val()
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          // console.log(data);
          window.location.href = data['url']
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}

function deleteCompany() {
  $.ajax({
      url: "/company/delete/", // the endpoint
      type: "POST", // http method
      data: {
          company_pk: $('#company_pk').val()
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          // console.log(data);
          window.location.href = data['url']
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}

function updateProfile() {
  $.ajax({
      url: "/accounts/update/", // the endpoint
      type: "POST", // http method
      data: {
          profile_form: $('#profile-form').serialize()
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          // console.log(data);
          window.location.href = data['url']
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}
