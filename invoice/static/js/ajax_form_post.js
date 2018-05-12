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

function markInvoiceSent(invoice_pk) {
    $.ajax({
        url : "/api/mark_sent", // the endpoint
        type : "POST", // http method
        data : {
            invoice_pk: invoice_pk
        },
        traditional: true,

        success : function(data) {
            // console.log(data);
            $('#invoice-sent-date').text(data['sent_date']);
            $('#mark_sent_button').addClass('scale-out-button')
        }
    });
}

function updateItem() {
    $.ajax({
        url : "/invoice/item/update/", // the endpoint
        type : "POST", // http method
        data : {
            invoice_pk: $('#invoice_pk').val(),
            invoice_item_form: $('#invoice-item-form').serialize()
        }, // data sent with the post request

        success : function(data) {
            $('#invoice_item_table').html(data);
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
            $('#quantityInput').val(data['quantity']).removeClass('valid');
            $('#quantityInputLabel').addClass('active');
            $('#costInput').val(data['cost']).removeClass('valid');
            $('#costInputLabel').addClass('active');
            // console.log(data);
        },
        error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}
    });
}

function getCompanyForForm(company_name, form_type) {
    $.ajax({
        url: "/api/get_company_for_form/", // the endpoint
        type: "POST", // http method
        data: {
            company_name: company_name,
            form_type: form_type
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            console.log('get company');
            if (data['form_type'] === 'modal') {
                $('#editStatusCompany').html(data['editStatus']);
                $('#div_for_company_form').html(data['html']);
                $('#companyModal').modal('open')
            } else {
                $('#company-person').val(data['company']['person']);
                $('#company-phone').val(data['company']['phone'])
            }

            Materialize.updateTextFields()
        },
        error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}
    });
}

function updateCompany() {
    $.ajax({
        url: "/company/update/", // the endpoint
        type: "POST", // http method
        data: {
            company_form: $('#company-form').serialize()
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            console.log("update");

            if (data['url']) {
                window.location.href = data['url'];
            } else {
                $('#companyModal').modal('close');
                // getCompanyForForm(data['company_name'], 'form');
                $('#company-autocomplete').val(data['company']);
                Materialize.updateTextFields();
            }

        },
        error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

    });
}

// function fillFormFieldsWithCompany(company_name) {
//     $.ajax({
//         url: "/api//", // the endpoint
//         type: "POST", // http method
//         data: {
//             company_name: company_name
//         }, // data sent with the post request
//
//         // handle a successful response
//         success: function (data) {
//             console.log(data);
//         },
//         error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}
//
//     });
// }

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

function getExpenseItemsForModal(pk_array) {
  $.ajax({
      url: "/api/get_expense_items_for_modal/", // the endpoint
      type: "POST", // http method
      data: {
          pk_array: pk_array
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          // console.log(data);
          $('#div_for_expense_form').html(data);
          Materialize.updateTextFields();
          // $('#invoice-select').material_select();
          if (pk_array[0] !== 0) {
            $('#editStatusExpense').html('Edit Expense');
          }
          $('#expenseModal').modal('open')
      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}

function updateExpense() {
  $.ajax({
      url: "/expense/update/", // the endpoint
      type: "POST", // http method
      data: {
          expense_form: $('#expense-form').serialize()
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          // console.log(data);

          if (data['url']) {
              window.location.href = data['url'];
          } else {
            $('#expense-table').html(data['html']);
          }

      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}

// Set dynamically in showDeleteModal function
function deleteItem(item_pk, type) {
  $.ajax({
      url: "/api/delete_item/", // the endpoint
      type: "POST", // http method
      data: {
          item_pk: item_pk,
          type: type
      }, // data sent with the post request

      // handle a successful response
      success: function (data) {
          // console.log(data);

          if (data['url']) {
              window.location.href = data['url'];
          } else {
            $('#' + data['type'] + '_table').html(data['html']);
          }

      },
      error : function(xhr) {console.log(xhr.status + ": " + xhr.responseText)}

  });
}

function showDeleteModal(item, item_pk, type) {
    $('#deleteContent').html(item);
    $('#delete_modal_confirm').attr('onClick', 'deleteItem(' + item_pk + ', ' + '"' + type + '"' + ');');
    $('#deleteStatus').html(type);
    $('#deleteModal').modal('open')
}
