Papa.parse(file, {
    complete: function(results) {
        console.log("Finished:", results.data);
    }
});
