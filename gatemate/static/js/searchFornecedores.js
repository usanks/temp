const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const paginatorContainer = document.querySelector('.pagination-container');
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tBody = document.querySelector('.table-body');

searchField.addEventListener('keyup', (e) =>{
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0) {        
        paginatorContainer.style.display = "none";
        tBody.innerHTML = "";
        fetch("/fornecedor/search_fornecedor", {
            body: JSON.stringify({ searchText: searchValue }), 
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
               console.log("data", data);
               tableOutput.style.display = "block";
               appTable.style.display = "none";

               if(data.length === 0){
                noResults.style.display = "block";
                tableOutput.style.display = "none";
               } else {
                noResults.style.display = "none";
                data.forEach((item) => {
                    tBody.innerHTML +=
                        `<tr>
                            <td>${item.nome}</td>
                            <td>${item.cpf}</td>
                            <td>${item.categoria}</td>
                            <td>${item.empresa}</td>
                            <td>${item.placa}</td>
                            <td>${item.hora}</td>
                            <td>${item.data}</td>
                            <td>${item.status}</td>
                        </tr>`;                  
                });                
               }
            });
    } else {
        paginatorContainer.style.display = "block";
        appTable.style.display = "block";
        tableOutput.style.display = "none";
    }
});