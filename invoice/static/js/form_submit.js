$('#company-form').on('submit', function(event){
    event.preventDefault();
    updateCompany();

    return false;
});
