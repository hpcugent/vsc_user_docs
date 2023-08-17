
function populate_overview() {
    fetch('../json_data.json')
        .then((response) => response.json())
        .then((json) => {
            // Add HEADER
            let columns = [{"title": "name"}].concat(json.clusters.map(x => {
                    return ({"title": x.split("/")[1]})
                }));
            const table = new DataTable('#overview_table', {
                columns: columns,
                paging: false,
            });


            // ADD BODY
            let new_rows = [];
            for (const [key, value] of Object.entries(json.modules)) {
                let new_row = [key];
                value.forEach(bool => new_row.push(bool ? "x" : "-"));
                new_rows.push(new_row);
            }
            table.rows.add(new_rows).draw();
        })
}
//TODO: remove
//
// function populate_js(){
//     fetch('../json_data.json')
//         .then((response) => response.json())
//         .then((json) => {
//             // Add HEADER
//             const my_table_head = document.getElementById("thead_table");
//             let row = my_table_head.insertRow(0);
//             let cell = row.insertCell(-1);
//             cell.outerHTML = "<th></th>";
//             for (const cluster of json.clusters) {
//               let cell = row.insertCell(-1);
//               cell.outerHTML = "<th>" + cluster.split("/")[1] + "</th>";
//             }
//
//             // ADD BODY
//             const my_table_body = document.getElementById("tbody_table");
//             for (const [key, value] of Object.entries(json.modules)) {
//                 let row = my_table_body.insertRow(-1);
//                 // Add package name
//                 let cell = row.insertCell(-1);
//                 cell.innerHTML = key;
//
//                 //add rest
//                 for (const b of value) {
//                     let cell = row.insertCell(-1);
//                     if (b) {
//                         cell.innerHTML = "X";
//                     }
//                 }
//               }
//         });
// }

// populate_dt()
// populate_js()