function updateInvoice() {
  $.ajax({
    url : "/invoice/update/", // the endpoint
    type : "POST", // http method
    data : {
        invoice_pk: $('#invoice_pk').val(),
        company: $('#company-select').val(),
        person: $('#person').val(),
        phone: $('#phone-no').val(),
        paid: $('#is-paid').is(':checked'),
        utr: $('#utr').is(':checked')
    },
    traditional: true,

    success : function(data) {
        console.log(data);
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

function getItemsForModal(itemPk) {
  $.ajax({
      url: "/api/get_items_for_table/", // the endpoint
      type: "POST", // http method
      data: {
          item_pk: itemPk
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          if (data['item_pk'] != 0) {
              $('#editStatus').text('Edit Item');
          } else {
             $('#editStatus').text('Add Item');
          }
          $('#item_pk').val(data['item_pk']);

          $('#descriptionInput').val(data['description']);
          $('#descriptionInputLabel').addClass('active');
          $('#costInput').val(data['cost']);
          $('#costInputLabel').addClass('active');
          console.log(data);
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}
  });
}

function updateCompany(companyPk) {
  $.ajax({
      url: "/company/update/", // the endpoint
      type: "POST", // http method
      data: {
          company_pk: $('#companyPk').val(),
          name: $('#nameInput').val(),
          address: $('#addressInput').val(),
          email: $('#emailInput').val()
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          console.log(data);
          window.location.href = data['url']
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}

function deleteInvoice() {
  $.ajax({
      url: "/invoice/delete", // the endpoint
      type: "POST", // http method
      data: {
          invoice_pk: $('#invoice_pk').val()
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          console.log(data);
          window.location.href = data['url']
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}
