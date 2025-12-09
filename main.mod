main {
    var src = new IloOplModelSource("project.mod");
    var def = new IloOplModelDefinition(src);

    for (var k = 0; k < 10; k++) {

        var cplex = new IloCplex();
        var model = new IloOplModel(def, cplex);

        var filename = "big_" + k + ".dat";
        var data = new IloOplDataSource(filename);
        model.addDataSource(data);
        model.generate();

        cplex.epgap = 0.01;
        cplex.tilim = 1800;

        writeln("---- Execution ", k, " with file ", filename, " ----");
        var start = cplex.getCplexTime();

        if (cplex.solve()) {
            var end = cplex.getCplexTime();
            var solveTime = end - start;

            //writeln(model.printSolution());
            writeln("Solution value = ", cplex.getObjValue());
            writeln("Final GAP = ", cplex.getMIPRelativeGap());
            writeln("Solve execution time = ", formatFloat_prec4(solveTime));
        } else {
            writeln("No solution found");
        }

        model.end();
        data.end();
        cplex.end();
    }

    def.end();
    src.end();
}

execute {
  function formatFloat_prec4 (f) {
    f = Math.round(f*10000);
    var fs = f.toString();
    fs = fs.substring(0,fs.length-4)+','+fs.substring(fs.length-4,fs.length);
    return fs;
  }
};