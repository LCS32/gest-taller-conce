

const btnDelete = document.querySelectorAll('.btn-delete')

if (btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if (!confirm('¿Estas seguro de querer eliminar el registro?')) {
                e.preventDefault();
            }
        });

    });

};

$(function () {
    $('#table').searchable({
        striped: false,
        oddRow: { 'background-color': '#f5f5f5' },
        evenRow: { 'background-color': '#fff' },
        searchType: 'fuzzy'
    });

    $('#searchable-container').searchable({
        searchField: '#container-search',
        selector: '.row',
        childSelector: '.col-xs-4',
        show: function (elem) {
            elem.slideDown(100);
        },
        hide: function (elem) {
            elem.slideUp(100);
        }
    })
});

function totalIt() {
    var input = document.getElementsByName("product");
    var total = 0;
    for (var i = 0; i < input.length; i++) {
        if (input[i].checked) {
            total += parseInt(input[i].value);
        }
    }
    document.getElementsByName("total")[0].value = total.toFixed(0);
};



function calculate() {
    var myBox1 = document.getElementById('box1').value; 
    var myBox2 = document.getElementById('box2').value;
    var result = document.getElementById('result'); 
    var myResult = myBox1 * myBox2;
      document.getElementById('result').value = myResult;

}

function onblur() {
    
}