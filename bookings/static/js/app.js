var year = new Date();
year.setFullYear(year.getFullYear() - 70);

$( ".datepicker" ).datepicker({
    changeMonth: true,
    changeYear: true,
    yearRange: year + ':' + year,
    dateFormat: "yy-mm-dd"
});