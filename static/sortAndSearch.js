<script>
        const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

        const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
        v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2))
        (getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

        document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
        const table = th.closest('table');
        const tbody = table.querySelector('tbody');
        Array.from(tbody.querySelectorAll('tr'))
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => tbody.appendChild(tr) );})));


        var input = document.getElementById("searchbar");
        input.addEventListener("keyup", search);
        input.addEventListener("search", search);
        var rows = Array.prototype.slice.call(table.querySelectorAll("tr"));
        function search(){
            var filter = input.value.trim().toUpperCase();
            rows.forEach(function(row) {
                var data = "";
                Array.prototype.slice.call(row.getElementsByTagName("td")).forEach(function(r){
                    data += r.textContent;
                    });
                if(data.toUpperCase().indexOf(filter) > -1){
                    row.classList.remove("hidden");
                    } else {
                        row.classList.add("hidden");
                            }
            });

        }
    </script>
