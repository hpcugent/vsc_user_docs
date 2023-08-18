
function populate_overview() {
    fetch('../data/json_data.json')
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

// only populate table on correct page
document$.subscribe(function() {
    if (document.getElementById("overview_table")) {
        populate_overview()
    }
})
