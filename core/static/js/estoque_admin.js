$(document).ready(function(){
    $('.objects-tools').prepend('<li><a href="/produto/import/csv">Importar CSV</li>')
    $('.objects-tools').prepend('<li><a href="/produto/import/excel">Importar Excel</li>')
    $('#changelist-filter').prepend('<h2>Exportar</h2><ul><li><a href="/produto/export/csv">CSV</a></li><li><a href="/produto/export/excel">Excel</a></li></ul>')
})